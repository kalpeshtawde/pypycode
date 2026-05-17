import os
from typing import TypedDict, List, Dict, Any, Optional


class TagStat(TypedDict):
    accuracy: float
    attempted: int
    submitted: int
    weakness_score: float


class AgentState(TypedDict):
    user_id: Optional[str]
    goal: Optional[str]
    total: Optional[int]
    # Optional per-invocation auth token. When set, Vega's BackendClient uses
    # it instead of the module-level DEFAULT_AUTH_TOKEN. The Flask endpoint
    # supplies a freshly minted JWT for the calling user.
    auth_token: Optional[str]

    stats: Optional[Dict[str, Any]]
    tag_stats: Optional[Dict[str, TagStat]]
    tag_ranking: Optional[List[str]]
    level: Optional[str]  # or UserLevel
    strategy: Optional[str]

    difficulty_percent: Optional[Dict[str, int]]
    difficulty_counts: Optional[Dict[str, int]]

    tag_weights: Optional[Dict[str, float]]
    focus_tags: Optional[List[str]]
    strategy_reason: Optional[str]
    selected_problems: Optional[List[Dict[str, Any]]]
    ignore_slugs: Optional[List[str]]

    project: Optional[Dict[str, Any]]
    project_id: Optional[str]
    selection: Optional[Dict[str, Any]]
    project_problems: Optional[List[Dict[str, Any]]]

    retry_count: Optional[int]
