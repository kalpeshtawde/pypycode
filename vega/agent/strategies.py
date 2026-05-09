import random
from typing import Dict, Any

from vega.schemas import ProblemSetRequestPayload


def build_tag_weights(
    tag_stats: Dict[str, Dict[str, Any]],
    top_attempted: int = 4,
    explore_unattempted: int = 2,
) -> Dict[str, float]:

    if not tag_stats:
        return {}

    attempted_tags = {}
    unattempted_tags = {}

    for tag, stats in tag_stats.items():
        if stats.get("attempted", 0) > 0:
            attempted_tags[tag] = stats
        else:
            unattempted_tags[tag] = stats

    scored_attempted = []

    for tag, stats in attempted_tags.items():
        attempted = stats.get("attempted", 0)
        submitted = stats.get("submitted", 0)
        weakness = stats.get("weakness_score", 0.0)

        failure_rate = 1 - (submitted / attempted) if attempted else 1.0

        adjusted_score = (
            weakness
            + failure_rate * 0.5
            + min(attempted, 5) * 0.05
        )

        adjusted_score += (hash(tag) % 10) * 0.001

        scored_attempted.append((tag, adjusted_score))

    scored_attempted.sort(key=lambda x: x[1], reverse=True)

    selected_tags = dict(scored_attempted[:top_attempted])

    # Exploration
    if unattempted_tags:
        explore = random.sample(
            list(unattempted_tags.keys()),
            k=min(explore_unattempted, len(unattempted_tags)),
        )

        for tag in explore:
            selected_tags[tag] = 0.3

    if not selected_tags:
        return {}

    max_score = max(selected_tags.values()) or 1.0

    return {
        tag: round(max(score / max_score, 0.1), 3)
        for tag, score in selected_tags.items()
    }


def get_default_distribution(level: str, total: int):

    if level == "beginner":
        easy = int(total * 0.7)
        medium = int(total * 0.25)

    elif level == "advanced":
        easy = int(total * 0.1)
        medium = int(total * 0.4)

    else:
        # intermediate
        easy = int(total * 0.3)
        medium = int(total * 0.5)

    hard = total - easy - medium

    return {
        "easy": easy,
        "medium": medium,
        "hard": hard,
    }


def build_warmup_request(state):

    total = state["total"]

    return ProblemSetRequestPayload(
        mode="practice",
        difficultyCounts={
            "easy": total,
            "medium": 0,
            "hard": 0,
        },
        ignoreSlugs=state.get("ignore_slugs", []),
        tagWeights={},
        total=total,
    )


def build_topic_request(state):

    focus_tags = state.get("focus_tags", [])

    tag_weights = {
        tag: 1.0
        for tag in focus_tags
    }

    return ProblemSetRequestPayload(
        mode="practice",
        difficultyCounts=state["difficulty_counts"],
        ignoreSlugs=state.get("ignore_slugs", []),
        tagWeights=tag_weights,
        total=state["total"],
    )


def build_weakness_request(state):

    total = state["total"]

    tag_weights = build_tag_weights(
        state.get("tag_stats", {}),
        top_attempted=6,
        explore_unattempted=1,
    )

    easy = int(total * 0.35)
    medium = int(total * 0.5)
    hard = total - easy - medium

    return ProblemSetRequestPayload(
        mode="practice",
        difficultyCounts={
            "easy": easy,
            "medium": medium,
            "hard": hard,
        },
        ignoreSlugs=state.get("ignore_slugs", []),
        tagWeights=tag_weights,
        total=total,
    )


def build_revision_request(state):

    total = state["total"]

    tag_weights = build_tag_weights(
        state.get("tag_stats", {}),
        top_attempted=4,
        explore_unattempted=3,
    )

    easy = int(total * 0.25)
    medium = int(total * 0.5)
    hard = total - easy - medium

    return ProblemSetRequestPayload(
        mode="revision",
        difficultyCounts={
            "easy": easy,
            "medium": medium,
            "hard": hard,
        },
        ignoreSlugs=state.get("ignore_slugs", []),
        tagWeights=tag_weights,
        total=total,
    )


def build_balanced_request(state):

    total = state["total"]

    level = state.get("level", "intermediate")

    tag_weights = build_tag_weights(
        state.get("tag_stats", {}),
        top_attempted=3,
        explore_unattempted=2,
    )

    return ProblemSetRequestPayload(
        mode="practice",
        difficultyCounts=get_default_distribution(level, total),
        ignoreSlugs=state.get("ignore_slugs", []),
        tagWeights=tag_weights,
        total=total,
    )


STRATEGIES = {
    "warmup": build_warmup_request,
    "weakness_fix": build_weakness_request,
    "topic_focus": build_topic_request,
    "revision": build_revision_request,
    "mixed": build_balanced_request,
}