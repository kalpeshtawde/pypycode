import asyncio
from typing import List, Literal, Optional

from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from clients import BackendClient
from agent.state import AgentState
from agent.strategies import STRATEGIES
from problem_set_generator import ProblemSetGenerator
from schemas import CreateProjectRequestPayload

from constants import (
    DEFAULT_AUTH_TOKEN,
    DEFAULT_BACKEND_BASE_URL,
    DEFAULT_USER_ID,
    DEFAULT_TOTAL_QUESTIONS,
)


# Initialize our LLM
model = ChatOpenAI(temperature=0)
client = BackendClient(DEFAULT_BACKEND_BASE_URL, DEFAULT_AUTH_TOKEN)


def _client(state: AgentState) -> BackendClient:
    """Return a BackendClient using the per-invocation auth_token from state
    when present, otherwise the module-level default. Lets the Flask endpoint
    pass the calling user's JWT through to Vega's HTTP calls without any
    global mutation."""
    token = state.get("auth_token") if isinstance(state, dict) else None
    if token and token != DEFAULT_AUTH_TOKEN:
        return BackendClient(DEFAULT_BACKEND_BASE_URL, token)
    return client


async def fetch_user_stats(state: AgentState):
    user_id = state.get("user_id")

    if not user_id:
        raise ValueError("user_id is required")

    user_stats = await _client(state).get_user_stat(user_id)

    return {"stats": user_stats, "tags": []}


async def fetch_user_tag_stats(state: AgentState):
    user_id = state.get("user_id")

    user_tag_stats = await _client(state).get_user_tag_stat(user_id)

    sorted_tag_stats = sorted(
        user_tag_stats.items(),
        key=lambda x: x[1]["weakness_score"],
        reverse=True
    )

    tag_stats = {tag: stats for tag, stats in sorted_tag_stats}
    tag_ranking = [tag for tag, _ in sorted_tag_stats]

    return {
        "tag_stats": tag_stats,
        "tag_ranking": tag_ranking,
    }


class StrategyChoice(BaseModel):
    """Structured output schema for the pick_strategy LLM call."""

    strategy: Literal[
        "warmup", "weakness_fix", "topic_focus", "revision", "mixed"
    ] = Field(
        description=(
            "Which problem-selection strategy best fits the user's goal "
            "and recent performance."
        )
    )
    focus_tags: List[str] = Field(
        default_factory=list,
        description=(
            "Tags to focus on. Required when strategy is 'topic_focus'; "
            "otherwise leave empty."
        ),
    )
    reason: str = Field(
        description="One short sentence explaining the choice for logs/UI."
    )


_STRATEGY_GUIDE = """\
You are Vega, a coding-practice planner. Pick exactly ONE strategy:

- warmup: user is new, returning after a break, or explicitly wants easy practice.
  Produces an all-easy set.
- weakness_fix: user has clear weak tags (high weakness_score, low accuracy).
  Heavily weights weakest tags.
- topic_focus: user named specific topics/tags to drill. Requires focus_tags.
- revision: user wants to revisit known-but-rusty material. Balanced over weak
  tags with more exploration.
- mixed: default balanced practice across difficulties and tags.

Rules:
- If the goal mentions specific topics (e.g. "DP", "graphs"), choose topic_focus
  and put those tags in focus_tags (match against the provided tag list).
- If the goal mentions "warm up", "easy", "getting started" → warmup.
- If the goal mentions "interview", "weak areas", "improve" and tag_stats show
  real weaknesses → weakness_fix.
- If the goal mentions "review" or "revise" → revision.
- Otherwise → mixed.
"""


strategy_picker = model.with_structured_output(StrategyChoice)


async def pick_strategy(state: AgentState):
    goal = state.get("goal") or ""
    level = state.get("level")
    tag_ranking = state.get("tag_ranking") or []
    tag_stats = state.get("tag_stats") or {}

    # Compact context: top 10 weakest tags with their scores.
    top_tags_summary = []
    for tag in tag_ranking[:10]:
        s = tag_stats.get(tag, {})
        top_tags_summary.append(
            f"- {tag}: weakness={s.get('weakness_score', 0):.2f} "
            f"accuracy={s.get('accuracy', 0):.2f} "
            f"attempted={s.get('attempted', 0)}"
        )

    user_msg = (
        f"User goal: {goal or '(none provided)'}\n"
        f"User level: {level}\n"
        f"Top weak tags:\n"
        + ("\n".join(top_tags_summary) if top_tags_summary else "(no tag data)")
        + "\n\nPick the best strategy."
    )

    try:
        choice: StrategyChoice = await strategy_picker.ainvoke([
            SystemMessage(content=_STRATEGY_GUIDE),
            HumanMessage(content=user_msg),
        ])
        strategy = choice.strategy
        focus_tags = choice.focus_tags
        reason = choice.reason
    except Exception as e:
        # Fail safe: deterministic fallback so the graph never breaks on LLM error.
        strategy = "mixed"
        focus_tags = []
        reason = f"LLM fallback ({type(e).__name__}): defaulted to mixed."

    # Guardrail: topic_focus requires tags; if LLM forgot, downgrade to mixed.
    if strategy == "topic_focus" and not focus_tags:
        strategy = "mixed"
        reason = (
            "Downgraded topic_focus -> mixed because no focus_tags were chosen."
        )

    print(f"#### pick_strategy -> {strategy} | tags={focus_tags} | {reason}")

    return {
        "strategy": strategy,
        "focus_tags": focus_tags,
        "strategy_reason": reason,
    }


def classify_user_level(state: AgentState):
    gen_level = ProblemSetGenerator(
        state["stats"], DEFAULT_TOTAL_QUESTIONS
    ).determine_level()

    return {"level": gen_level.value}


async def build_distribution(state: AgentState):
    level = state.get("level")
    stats = state.get("stats")

    if not level:
        raise ValueError("level is required")

    # --- Base distributions ---
    if level == "beginner":
        distribution = {"easy": 70, "medium": 25, "hard": 5}

    elif level == "intermediate":
        distribution = {"easy": 30, "medium": 50, "hard": 20}

    elif level == "advanced":
        distribution = {"easy": 10, "medium": 40, "hard": 50}

    else:
        raise ValueError(f"Unknown level: {level}")

    # --- Optional: light adjustment using stats ---
    if stats:
        medium_attempted = stats.get("medium", {}).get("attempted", 0)
        medium_score = stats.get("medium", {}).get("score", 0)

        # If user is struggling with medium → reinforce it
        if medium_attempted >= 5 and medium_score < 0.5:
            distribution["medium"] += 10
            distribution["easy"] -= 5
            distribution["hard"] -= 5

        # If user is strong at medium → push harder problems
        elif medium_attempted >= 5 and medium_score > 0.8:
            distribution["hard"] += 10
            distribution["easy"] -= 5
            distribution["medium"] -= 5

    # --- Ensure total = 100 (safety) ---
    total = sum(distribution.values())
    if total != 100:
        # normalize (simple correction)
        diff = 100 - total
        distribution["medium"] += diff

    return {"difficulty_percent": distribution}


def convert_distribution_to_counts(state: AgentState):
    distribution = state["difficulty_percent"]
    total = state["total"]

    counts = ProblemSetGenerator.allocate_counts(distribution, total)

    return {"difficulty_counts": counts}


async def select_problems(state: AgentState):
    strategy_name = state.get("strategy", "mixed")

    strategy_builder = STRATEGIES.get(
        strategy_name,
        STRATEGIES["mixed"]
    )

    payload = strategy_builder(state)

    payload.metadata = {
        "level": state.get("level"),
        "source": "agent",
        "retry_count": state.get("retry_count", 0),
    }

    print(
        f"#### strategy={strategy_name} "
        f"level={state.get('level')} "
        f"payload={payload.model_dump()}"
    )

    result = await _client(state).problems_selector(payload)

    return {
        "selected_problems": result.get("problems"),
        "selection": result.get("selection"),
        "strategy": strategy_name,
    }


# Terminal transformation node
def assemble_project(state: AgentState):
    level = state.get("level")
    selected_problems = state.get("selected_problems", [])
    selection = state.get("selection", {})

    if not selected_problems:
        raise ValueError("No selected problems found")

    project = {
        "title": f"{level.title()} Interview Problem Set",
        "level": level,
        "problems": selected_problems,
        "selection_meta": selection,
        "total": len(selected_problems),
    }

    return {"project": project}


_EXPLAIN_GUIDE = """\
You are Vega, a coding-practice planner explaining the problem set you just \
created for the user. Write 2-3 short sentences in second person ("you").

- Reference the user's goal if provided.
- Mention the chosen strategy in plain language (don't say "weakness_fix" - say \
"focused on your weakest topics").
- Mention 1-2 specific tags being emphasized if any.
- Briefly justify the difficulty mix (e.g. "leaning medium/hard since you're \
preparing for interviews").
- Be encouraging but not cheesy. No emojis. No marketing fluff.
"""


def _fallback_explanation(state: AgentState) -> str:
    project = state.get("project") or {}
    level = state.get("level") or "intermediate"
    strategy = state.get("strategy") or "mixed"
    focus_tags = state.get("focus_tags") or []
    total = project.get("total", 0)

    pretty_strategy = {
        "warmup": "a warm-up set of easier problems",
        "weakness_fix": "problems focused on your weakest topics",
        "topic_focus": f"problems focused on {', '.join(focus_tags) or 'your chosen topics'}",
        "revision": "a revision set across topics you've worked on",
        "mixed": "a balanced practice set",
    }.get(strategy, "a balanced practice set")

    return (
        f"Built {pretty_strategy} with {total} problems calibrated to your "
        f"{level} level."
    )


async def explain_project(state: AgentState):
    project = dict(state.get("project") or {})
    goal = state.get("goal") or ""
    level = state.get("level")
    strategy = state.get("strategy")
    focus_tags = state.get("focus_tags") or []
    strategy_reason = state.get("strategy_reason") or ""
    selection_meta = project.get("selection_meta") or {}
    total = project.get("total", 0)

    # Lightweight tag emphasis summary (top-3 weighted tags from selection_meta if present).
    tag_weights = selection_meta.get("tagWeights") or {}
    top_weighted = sorted(tag_weights.items(), key=lambda x: x[1], reverse=True)[:3]
    top_tags_str = ", ".join(t for t, _ in top_weighted) or "(no tag emphasis)"

    user_msg = (
        f"Goal: {goal or '(none)'}\n"
        f"User level: {level}\n"
        f"Strategy chosen: {strategy}\n"
        f"Strategy rationale: {strategy_reason}\n"
        f"Focus tags: {focus_tags or '(none)'}\n"
        f"Top weighted tags: {top_tags_str}\n"
        f"Total problems: {total}\n"
        f"Difficulty counts: {selection_meta.get('difficultyCounts') or 'n/a'}\n"
        "\nWrite the explanation now."
    )

    try:
        response = await model.ainvoke([
            SystemMessage(content=_EXPLAIN_GUIDE),
            HumanMessage(content=user_msg),
        ])
        explanation = (response.content or "").strip()
        if not explanation:
            explanation = _fallback_explanation(state)
    except Exception as e:
        explanation = _fallback_explanation(state)
        explanation += f" (LLM unavailable: {type(e).__name__})"

    project["explanation"] = explanation
    print(f"#### explain_project -> {explanation}")

    return {"project": project}


_MAX_PROJECT_NAME_LENGTH = 80


def _build_project_name(project: dict, goal: str = None) -> str:
    """Backend caps project name at 80 chars and requires (user_id, name)
    uniqueness, so we suffix a short timestamp to avoid 409 conflicts on
    repeated runs."""
    from datetime import datetime, timezone

    # Use the user's goal/prompt to generate a concise title
    if goal:
        # Simple heuristic: convert goal to title case, remove common prefixes
        base = goal.strip()
        # Remove common conversational prefixes
        prefixes_to_remove = [
            "i need to",
            "i want to",
            "i would like to",
            "help me",
            "please help me",
            "can you",
        ]
        for prefix in prefixes_to_remove:
            if base.lower().startswith(prefix):
                base = base[len(prefix):].strip()
        # Capitalize first letter of each word
        base = " ".join(word.capitalize() for word in base.split())
    elif project.get("title"):
        base = project.get("title").strip()
    else:
        base = "Vega Problem Set"
    
    suffix = " · " + datetime.now(timezone.utc).strftime("%Y-%m-%d")
    budget = _MAX_PROJECT_NAME_LENGTH - len(suffix)
    if len(base) > budget:
        base = base[: max(1, budget - 1)].rstrip() + "…"
    return (base + suffix)[:_MAX_PROJECT_NAME_LENGTH]


async def persist_project(state: AgentState):
    project = dict(state.get("project") or {})
    selected_problems = state.get("selected_problems") or []
    selection_meta = project.get("selection_meta") or {}

    problem_ids = [
        p.get("id") or p.get("_id")
        for p in selected_problems
        if p.get("id") or p.get("_id")
    ]

    ai_metadata = {
        "focus_tags": state.get("focus_tags") or [],
        "tag_weights": selection_meta.get("tagWeights") or {},
        "difficulty_counts": selection_meta.get("difficultyCounts"),
        "strategy_reason": state.get("strategy_reason"),
        "retry_count": state.get("retry_count", 0),
        "total": project.get("total"),
    }

    payload = CreateProjectRequestPayload(
        name=_build_project_name(project, state.get("goal")),
        problemIds=problem_ids or None,
        goal=state.get("goal") or None,
        strategy=state.get("strategy") or None,
        level=state.get("level") or None,
        explanation=project.get("explanation"),
        aiMetadata=ai_metadata,
    )

    try:
        result = await _client(state).create_project(payload)
        project_id = result.get("id")
        project["id"] = project_id
        project["name"] = result.get("name")
        print(f"#### persist_project -> id={project_id}")
        return {"project": project, "project_id": project_id}
    except Exception as e:
        # Don't break the graph if persistence fails - user still gets the
        # assembled project + explanation in memory.
        print(f"#### persist_project FAILED: {type(e).__name__}: {e}")
        project["persistence_error"] = str(e)
        return {"project": project}


def adjust_inputs(state: AgentState):
    ignore_slugs = state.get("ignore_slugs", [])
    problems = state.get("selected_problems", [])

    # avoid duplicates in next retry
    new_slugs = [p["slug"] for p in problems if "slug" in p]
    updated_ignore = list(set(ignore_slugs + new_slugs))

    return {
        "ignore_slugs": updated_ignore
    }


def should_retry_selection(state: AgentState):
    problems = state.get("selected_problems", [])
    retry_count = state.get("retry_count", 0)

    if not problems or len(problems) < state["total"]:
        if retry_count >= 2:
            return {"route": "give_up"}
        return {
            "route": "retry",
            "retry_count": retry_count + 1
        }

    return {"route": "good"}


builder = StateGraph(AgentState)

builder.add_node("fetch_user_stats", fetch_user_stats)
builder.add_node("classify_user_level", classify_user_level)
builder.add_node("build_distribution", build_distribution)
builder.add_node("convert_distribution_to_counts", convert_distribution_to_counts)
builder.add_node("select_problems", select_problems)
builder.add_node("should_retry_selection", should_retry_selection)
builder.add_node("adjust_inputs", adjust_inputs)
builder.add_node("assemble_project", assemble_project)
builder.add_node("fetch_user_tag_stats", fetch_user_tag_stats)
builder.add_node("pick_strategy", pick_strategy)
builder.add_node("explain_project", explain_project)
builder.add_node("persist_project", persist_project)


builder.add_edge(START, "fetch_user_stats")

builder.add_edge("fetch_user_stats", "classify_user_level")

builder.add_edge("classify_user_level", "fetch_user_tag_stats")

builder.add_edge("fetch_user_tag_stats", "pick_strategy")

builder.add_edge("pick_strategy", "build_distribution")

builder.add_edge("build_distribution", "convert_distribution_to_counts")

builder.add_edge("convert_distribution_to_counts", "select_problems")

builder.add_edge("select_problems", "should_retry_selection")

builder.add_conditional_edges(
    "should_retry_selection",
    lambda state: state["route"],
    {
        "good": "assemble_project",
        "retry": "adjust_inputs",
        "give_up": "assemble_project",
    },
)

builder.add_edge("adjust_inputs", "select_problems")

builder.add_edge("assemble_project", "explain_project")

builder.add_edge("explain_project", "persist_project")

builder.add_edge("persist_project", END)

graph = builder.compile()


async def main():
    input_state = {
        "user_id": "5db77ae5-4bd4-465e-9641-4ba8c511f846",
        "goal": "I have a coding interview in 2 weeks",
        "total": 20,
        "retry_count": 0,
    }

    result = await graph.ainvoke(
        input_state,
        config={
            "run_name": f"pypycode_{input_state['user_id'][:6]}"
        }
    )


if __name__ == "__main__":
    asyncio.run(main())
