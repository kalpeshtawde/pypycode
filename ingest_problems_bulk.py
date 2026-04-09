from __future__ import annotations

import argparse
import itertools
import json
import random
import re
import time
from pathlib import Path

try:
    import requests
except ModuleNotFoundError:
    requests = None

BASE_URL = "https://pypycode.com/api/problems/public-ingest"
INGEST_KEY = "EMDgUmg7tzsgdf5r3eFd"
TOTAL_PROBLEMS = 1000
SEED = 20260408

THEMES = [
    "Satellite",
    "Submarine",
    "Firewall",
    "Nebula",
    "Archaeology",
    "Quantum",
    "Ledger",
    "Neural",
    "Drone",
    "Vault",
    "Oracle",
    "CryoLab",
    "Asteroid",
    "Sonar",
    "Cipher",
    "Temple",
    "Comet",
    "Harbor",
    "Atlas",
    "Chronicle",
]

ACTIONS = [
    "Data-Sync",
    "Route-Finder",
    "Signal-Filter",
    "Risk-Scanner",
    "Artifact-Mapper",
    "Pattern-Decoder",
    "Flow-Optimizer",
    "Node-Linker",
    "Path-Rewrite",
    "Load-Balancer",
    "Anomaly-Tracker",
    "Beacon-Aligner",
    "Circuit-Guard",
    "Pulse-Matcher",
    "Depth-Analyzer",
    "Vault-Recovery",
    "Graph-Indexer",
    "Drift-Predictor",
    "Queue-Stabilizer",
    "Shard-Composer",
]

ALGO_TAGS = [
    "bfs",
    "dfs",
    "tree",
    "graph",
    "dynamic-programming",
    "two-pointers",
    "sliding-window",
    "backtracking",
    "math",
    "string",
]

DIFFICULTIES = ["easy", "medium", "hard"]

TEMPLATES = [
    {
        "key": "target-pair-protocol",
        "title_suffix": "Target Pair Protocol",
        "slug_suffix": "target-pair-protocol",
        "function": "target_pair_protocol",
        "signature": "def target_pair_protocol(nums: list[int], target: int) -> list[int]:",
        "description": (
            "In a {theme} {action} scenario, analysts process integer packets. "
            "Find two distinct packet indices whose values add to the control target. "
            "Exactly one valid pair exists, and each index may be used once."
        ),
        "examples": [
            ("nums = [2, 7, 11, 15], target = 9", "[0, 1]", "2 + 7 reaches the target immediately."),
            ("nums = [3, 2, 4], target = 6", "[1, 2]", "Indices 1 and 2 form the required sum."),
            ("nums = [1, 5, 3, 8], target = 11", "[1, 3]", "5 + 6 equivalent pair is tracked as indices [1, 3]."),
        ],
        "tests": [
            ("[2, 7, 11, 15], 9", "[0, 1]"),
            ("[3, 2, 4], 6", "[1, 2]"),
            ("[1, 5, 3, 8], 11", "[1, 3]"),
            ("[0, 4, 3, 0], 0", "[0, 3]"),
            ("[-1, -2, -3, -4], -6", "[1, 3]"),
            ("[5, 1, 9, 7], 8", "[1, 3]"),
            ("[10, 20, 30, 40], 50", "[0, 3]"),
            ("[5, 5], 10", "[0, 1]"),
            ("[4, 6, 1, 3], 7", "[1, 2]"),
            ("[100, 200, 300], 500", "[1, 2]"),
        ],
        "tags": ["two-pointers", "math", "graph"],
    },
    {
        "key": "grid-escape-hops",
        "title_suffix": "Grid Escape Hops",
        "slug_suffix": "grid-escape-hops",
        "function": "grid_escape_hops",
        "signature": "def grid_escape_hops(grid: list[list[int]]) -> int:",
        "description": (
            "A {theme} {action} map uses 0 for open cells and 1 for blocked cells. "
            "Return the shortest number of moves from the top-left corner to the bottom-right corner "
            "using four-direction movement, or -1 if no route exists."
        ),
        "examples": [
            ("grid = [[0,0,1],[1,0,1],[1,0,0]]", "4", "Shortest valid route uses four moves."),
            ("grid = [[0,1],[1,0]]", "-1", "Both possible entries are blocked by walls."),
            ("grid = [[0]]", "0", "Start already equals destination."),
        ],
        "tests": [
            ("[[0,0,1],[1,0,1],[1,0,0]]", "4"),
            ("[[0,1],[1,0]]", "-1"),
            ("[[0]]", "0"),
            ("[[0,0],[0,0]]", "2"),
            ("[[0,1,0],[0,1,0],[0,0,0]]", "4"),
            ("[[0,0,0],[1,1,0],[1,1,0]]", "4"),
            ("[[1]]", "-1"),
            ("[[0,0,0],[0,1,1],[0,0,0]]", "4"),
            ("[[0,1,0],[0,1,0],[0,1,0]]", "-1"),
            ("[[0,0,0,0]]", "3"),
        ],
        "tags": ["bfs", "graph", "dfs"],
    },
    {
        "key": "distinct-signal-window",
        "title_suffix": "Distinct Signal Window",
        "slug_suffix": "distinct-signal-window",
        "function": "distinct_signal_window",
        "signature": "def distinct_signal_window(stream: str) -> int:",
        "description": (
            "The {theme} {action} system receives a character stream. "
            "Compute the length of the longest contiguous segment with no repeated characters."
        ),
        "examples": [
            ("stream = \"abcabcbb\"", "3", "\"abc\" is the longest unique segment."),
            ("stream = \"bbbbb\"", "1", "Only one unique character can remain in-window."),
            ("stream = \"pwwkew\"", "3", "\"wke\" gives the maximum length of 3."),
        ],
        "tests": [
            ("\"abcabcbb\"", "3"),
            ("\"bbbbb\"", "1"),
            ("\"pwwkew\"", "3"),
            ("\"\"", "0"),
            ("\"dvdf\"", "3"),
            ("\"abba\"", "2"),
            ("\"abcdef\"", "6"),
            ("\"tmmzuxt\"", "5"),
            ("\"anviaj\"", "5"),
            ("\"au\"", "2"),
        ],
        "tags": ["sliding-window", "string", "two-pointers"],
    },
    {
        "key": "island-cluster-count",
        "title_suffix": "Island Cluster Count",
        "slug_suffix": "island-cluster-count",
        "function": "island_cluster_count",
        "signature": "def island_cluster_count(grid: list[list[str]]) -> int:",
        "description": (
            "A {theme} {action} scanner returns a map of '1' (solid zone) and '0' (void). "
            "Count how many connected clusters exist using horizontal and vertical adjacency only."
        ),
        "examples": [
            ("grid = [[\"1\",\"1\",\"0\"],[\"0\",\"1\",\"0\"],[\"0\",\"0\",\"1\"]]", "2", "One upper cluster and one isolated cell."),
            ("grid = [[\"1\",\"1\"],[\"1\",\"1\"]]", "1", "All cells belong to one connected component."),
            ("grid = [[\"0\",\"0\"],[\"0\",\"0\"]]", "0", "No solid zones are present."),
        ],
        "tests": [
            ("[[\"1\",\"1\",\"0\"],[\"0\",\"1\",\"0\"],[\"0\",\"0\",\"1\"]]", "2"),
            ("[[\"1\",\"1\"],[\"1\",\"1\"]]", "1"),
            ("[[\"0\",\"0\"],[\"0\",\"0\"]]", "0"),
            ("[[\"1\"]]", "1"),
            ("[[\"1\",\"0\",\"1\"]]", "2"),
            ("[[\"1\",\"0\"],[\"0\",\"1\"]]", "2"),
            ("[[\"1\",\"1\",\"1\"],[\"0\",\"1\",\"0\"]]", "1"),
            ("[[\"1\",\"0\",\"1\"],[\"0\",\"1\",\"0\"],[\"1\",\"0\",\"1\"]]", "5"),
            ("[[\"0\"]]", "0"),
            ("[[\"1\",\"1\",\"0\",\"1\"]]", "2"),
        ],
        "tags": ["dfs", "graph", "bfs"],
    },
    {
        "key": "stair-energy-dp",
        "title_suffix": "Stair Energy DP",
        "slug_suffix": "stair-energy-dp",
        "function": "stair_energy_dp",
        "signature": "def stair_energy_dp(n: int) -> int:",
        "description": (
            "In a {theme} {action} mission, an agent climbs n levels, moving 1 or 2 levels per jump. "
            "Return the number of distinct jump sequences to reach level n."
        ),
        "examples": [
            ("n = 2", "2", "Sequences are [1,1] and [2]."),
            ("n = 3", "3", "Three valid sequences cover the top level."),
            ("n = 5", "8", "Counts follow a Fibonacci-style growth."),
        ],
        "tests": [
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "5"),
            ("5", "8"),
            ("6", "13"),
            ("7", "21"),
            ("8", "34"),
            ("10", "89"),
            ("12", "233"),
        ],
        "tags": ["dynamic-programming", "math", "string"],
    },
    {
        "key": "bracket-integrity-check",
        "title_suffix": "Bracket Integrity Check",
        "slug_suffix": "bracket-integrity-check",
        "function": "bracket_integrity_check",
        "signature": "def bracket_integrity_check(stream: str) -> bool:",
        "description": (
            "The {theme} {action} validator inspects a bracket stream containing (), [], and {{}}. "
            "Return True when every opening token is closed by the right type in valid nesting order."
        ),
        "examples": [
            ("stream = \"()[]{}\"", "True", "All bracket groups are correctly matched."),
            ("stream = \"(]\"", "False", "A round bracket is closed by a square bracket."),
            ("stream = \"{[]}\"", "True", "Nested brackets are fully balanced."),
        ],
        "tests": [
            ("\"()[]{}\"", "True"),
            ("\"(]\"", "False"),
            ("\"{[]}\"", "True"),
            ("\"\"", "True"),
            ("\"([)]\"", "False"),
            ("\"(((())))\"", "True"),
            ("\"{[}\"", "False"),
            ("\"[\"", "False"),
            ("\"[]{}()\"", "True"),
            ("\"(()\"", "False"),
        ],
        "tags": ["string", "graph", "two-pointers"],
    },
    {
        "key": "matrix-rise-route",
        "title_suffix": "Matrix Rise Route",
        "slug_suffix": "matrix-rise-route",
        "function": "matrix_rise_route",
        "signature": "def matrix_rise_route(grid: list[list[int]]) -> int:",
        "description": (
            "For a {theme} {action} matrix, you may move up, down, left, or right. "
            "Find the length of the longest strictly increasing route."
        ),
        "examples": [
            ("grid = [[9,9,4],[6,6,8],[2,1,1]]", "4", "One optimal route is 1 -> 2 -> 6 -> 9."),
            ("grid = [[3,4,5],[3,2,6],[2,2,1]]", "4", "An increasing chain of four exists."),
            ("grid = [[1]]", "1", "Single cell route length is one."),
        ],
        "tests": [
            ("[[9,9,4],[6,6,8],[2,1,1]]", "4"),
            ("[[3,4,5],[3,2,6],[2,2,1]]", "4"),
            ("[[1]]", "1"),
            ("[[1,2,3],[6,5,4],[7,8,9]]", "9"),
            ("[[7,7,7],[7,7,7]]", "1"),
            ("[[1,2],[3,4]]", "3"),
            ("[[5,4,3],[6,1,2],[7,8,9]]", "9"),
            ("[[10,11],[9,8]]", "3"),
            ("[[1,2,1],[2,3,4],[2,2,5]]", "5"),
            ("[[0,-1],[-2,-3]]", "1"),
        ],
        "tags": ["dynamic-programming", "dfs", "graph"],
    },
    {
        "key": "merge-time-slots",
        "title_suffix": "Merge Time Slots",
        "slug_suffix": "merge-time-slots",
        "function": "merge_time_slots",
        "signature": "def merge_time_slots(intervals: list[list[int]]) -> list[list[int]]:",
        "description": (
            "A {theme} {action} coordinator receives intervals representing active windows. "
            "Merge all overlapping intervals and return sorted non-overlapping windows."
        ),
        "examples": [
            ("intervals = [[1,3],[2,6],[8,10],[15,18]]", "[[1, 6], [8, 10], [15, 18]]", "The first two ranges overlap and merge."),
            ("intervals = [[1,4],[4,5]]", "[[1, 5]]", "Touching endpoints count as overlapping."),
            ("intervals = [[1,4],[2,3]]", "[[1, 4]]", "The larger interval absorbs the smaller one."),
        ],
        "tests": [
            ("[[1,3],[2,6],[8,10],[15,18]]", "[[1, 6], [8, 10], [15, 18]]"),
            ("[[1,4],[4,5]]", "[[1, 5]]"),
            ("[[1,4],[2,3]]", "[[1, 4]]"),
            ("[[1,2]]", "[[1, 2]]"),
            ("[[1,2],[3,4]]", "[[1, 2], [3, 4]]"),
            ("[[1,10],[2,3],[4,5]]", "[[1, 10]]"),
            ("[[5,7],[1,3],[2,6]]", "[[1, 7]]"),
            ("[[0,0],[1,4]]", "[[0, 0], [1, 4]]"),
            ("[[2,2],[2,3]]", "[[2, 3]]"),
            ("[[3,8],[1,2],[9,10]]", "[[1, 2], [3, 8], [9, 10]]"),
        ],
        "tags": ["two-pointers", "graph", "string"],
    },
    {
        "key": "bst-kth-signal",
        "title_suffix": "BST Kth Signal",
        "slug_suffix": "bst-kth-signal",
        "function": "bst_kth_signal",
        "signature": "def bst_kth_signal(root: list[int | None], k: int) -> int:",
        "description": (
            "A {theme} {action} index stores values in a Binary Search Tree. "
            "Given level-order BST data and k, return the k-th smallest value in the tree."
        ),
        "examples": [
            ("root = [3,1,4,None,2], k = 1", "1", "The smallest value is found first in sorted BST order."),
            ("root = [5,3,6,2,4,None,None,1], k = 3", "3", "In-order traversal yields 1,2,3,..."),
            ("root = [2,1,3], k = 2", "2", "The middle value is the 2nd smallest."),
        ],
        "tests": [
            ("[3,1,4,None,2], 1", "1"),
            ("[5,3,6,2,4,None,None,1], 3", "3"),
            ("[2,1,3], 2", "2"),
            ("[1], 1", "1"),
            ("[5,3,7,2,4,6,8], 4", "5"),
            ("[5,3,7,2,4,6,8], 1", "2"),
            ("[5,3,7,2,4,6,8], 7", "8"),
            ("[10,5,15,3,7], 2", "5"),
            ("[10,5,15,3,7], 4", "10"),
            ("[8,3,10,1,6,None,14], 5", "8"),
        ],
        "tags": ["tree", "dfs", "bfs"],
    },
    {
        "key": "palindrome-shard-partitions",
        "title_suffix": "Palindrome Shard Partitions",
        "slug_suffix": "palindrome-shard-partitions",
        "function": "palindrome_shard_partitions",
        "signature": "def palindrome_shard_partitions(text: str) -> list[list[str]]:",
        "description": (
            "In a {theme} {action} archive, a string must be split into shards where every shard is a palindrome. "
            "Return all valid partition layouts."
        ),
        "examples": [
            ("text = \"aab\"", "[[\"a\", \"a\", \"b\"], [\"aa\", \"b\"]]", "Both partitions contain only palindrome fragments."),
            ("text = \"aba\"", "[[\"a\", \"b\", \"a\"], [\"aba\"]]", "The whole string and split form are valid."),
            ("text = \"a\"", "[[\"a\"]]", "Single-character shard is always palindromic."),
        ],
        "tests": [
            ("\"aab\"", "[[\"a\", \"a\", \"b\"], [\"aa\", \"b\"]]"),
            ("\"aba\"", "[[\"a\", \"b\", \"a\"], [\"aba\"]]"),
            ("\"a\"", "[[\"a\"]]"),
            ("\"aa\"", "[[\"a\", \"a\"], [\"aa\"]]"),
            ("\"ab\"", "[[\"a\", \"b\"]]"),
            ("\"abba\"", "includes [\"abba\"]"),
            ("\"racecar\"", "includes [\"racecar\"]"),
            ("\"abc\"", "[[\"a\", \"b\", \"c\"]]"),
            ("\"aaa\"", "includes [\"a\", \"a\", \"a\"]"),
            ("\"level\"", "includes [\"level\"]"),
        ],
        "tags": ["backtracking", "string", "dynamic-programming"],
    },
]


def slugify(text: str) -> str:
    text = text.lower().replace("_", "-")
    text = re.sub(r"[^a-z0-9-]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text


def load_existing_slugs(repo_root: Path) -> set[str]:
    slug_pattern = re.compile(r'"slug"\s*:\s*"([^"]+)"')
    slugs: set[str] = set()

    for relative_path in ["ingest_problems.py", "problems.json", "backend/problems.json"]:
        file_path = repo_root / relative_path
        if not file_path.exists():
            continue

        content = file_path.read_text(encoding="utf-8", errors="ignore")
        for match in slug_pattern.finditer(content):
            slugs.add(match.group(1).strip())

    return slugs


def build_problem(theme: str, action: str, template: dict, difficulty: str, slug: str) -> dict:
    title = f"{theme} {action} {template['title_suffix']}"
    description = template["description"].format(theme=theme.lower(), action=action.lower())

    examples = [
        {
            "input": ex_input,
            "output": ex_output,
            "explanation": f"{ex_explanation} Context: {theme} {action} operation.",
        }
        for ex_input, ex_output, ex_explanation in template["examples"]
    ]

    test_cases = [
        {
            "function": template["function"],
            "input": test_input,
            "expected": expected,
        }
        for test_input, expected in template["tests"]
    ]

    tags = list(dict.fromkeys(template["tags"]))
    if not any(tag in ALGO_TAGS for tag in tags):
        tags.append("string")

    return {
        "slug": slug,
        "title": title,
        "difficulty": difficulty,
        "description": description,
        "starterCode": f"{template['signature']}\n    pass",
        "examples": examples,
        "testCases": test_cases,
        "tags": tags,
    }


def generate_problems(total: int, existing_slugs: set[str], seed: int = SEED) -> list[dict]:
    rng = random.Random(seed)
    combinations = list(itertools.product(THEMES, ACTIONS, TEMPLATES))
    rng.shuffle(combinations)

    generated: list[dict] = []
    used_slugs = set(existing_slugs)

    for theme, action, template in combinations:
        if len(generated) >= total:
            break

        base_slug = slugify(f"{theme}-{action}-{template['slug_suffix']}")
        slug = base_slug
        suffix = 2
        while slug in used_slugs:
            slug = f"{base_slug}-{suffix}"
            suffix += 1

        difficulty = rng.choice(DIFFICULTIES)
        problem = build_problem(theme, action, template, difficulty, slug)
        generated.append(problem)
        used_slugs.add(slug)

    if len(generated) < total:
        raise RuntimeError(
            f"Could only generate {len(generated)} problems. Increase templates or theme/action lists."
        )

    return generated


def post_problem(problem: dict) -> tuple[int | None, str]:
    if requests is None:
        return None, "requests library is not installed. Install with: pip install requests"

    payload = {**problem, "ingestKey": INGEST_KEY}
    try:
        response = requests.post(BASE_URL, json=payload, timeout=20)
        return response.status_code, response.text
    except Exception as exc:
        return None, str(exc)


def ingest_problems(problems: list[dict], sleep_ms: int = 0) -> tuple[int, int]:
    success = 0
    failed = 0

    for idx, problem in enumerate(problems, start=1):
        status, body = post_problem(problem)
        if status is not None and 200 <= status < 300:
            success += 1
            print(f"[{idx:4d}/{len(problems)}] ✅ {problem['slug']} ({problem['difficulty']})")
        else:
            failed += 1
            print(f"[{idx:4d}/{len(problems)}] ❌ {problem['slug']} -> {status}: {body[:140]}")

        if sleep_ms > 0:
            time.sleep(sleep_ms / 1000)

    return success, failed


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate and ingest 1,000 unique coding problems")
    parser.add_argument("--count", type=int, default=TOTAL_PROBLEMS, help="Number of problems to generate")
    parser.add_argument("--seed", type=int, default=SEED, help="Random seed for deterministic generation")
    parser.add_argument("--dry-run", action="store_true", help="Generate and print summary without POST")
    parser.add_argument("--write-json", type=str, default="", help="Write generated payloads to a JSON file")
    parser.add_argument("--sleep-ms", type=int, default=0, help="Delay between requests in milliseconds")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent
    existing_slugs = load_existing_slugs(repo_root)
    problems = generate_problems(total=args.count, existing_slugs=existing_slugs, seed=args.seed)

    print(f"Existing slugs detected: {len(existing_slugs)}")
    print(f"Generated problems: {len(problems)}")
    print(f"Unique generated slugs: {len({p['slug'] for p in problems})}")

    if args.write_json:
        output_path = Path(args.write_json)
        output_path.write_text(json.dumps({"problems": problems}, indent=2), encoding="utf-8")
        print(f"Wrote generated payloads to: {output_path}")

    if args.dry_run:
        print("Dry run complete. No requests were sent.")
        return

    print(f"Posting to {BASE_URL}")
    success, failed = ingest_problems(problems, sleep_ms=args.sleep_ms)
    print("=" * 64)
    print(f"Done. success={success}, failed={failed}")


if __name__ == "__main__":
    main()
