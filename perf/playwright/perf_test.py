#!/usr/bin/env python3
"""
Playwright perf test: for every problem that has a reference solution in the DB,
load the solution into the editor, click Run, and verify all tests pass.

Config (env vars or .env.local in this directory):
    BASE_URL                Frontend URL                        (default: http://localhost:81)
    API_URL                 Backend API URL                     (default: http://localhost:81/api)
    PERF_USER_EMAIL         Perfuser email                      (default: perfuser@local.test)
    PERF_USER_PASSWORD      Perfuser password                   (required)
    HEADLESS                Run browser headlessly              (default: true)
    SLOW_MO_MS              Slow-motion ms per op               (default: 0)
    RUN_TIMEOUT_MS          Max ms to wait for run result       (default: 45000)
    DELAY_BETWEEN_MS        Pause between problems (throttle)   (default: 800)
    MAX_CONSECUTIVE_ERRORS  Abort after this many timeouts in a row (default: 5)
"""
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from typing import Optional

import requests
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Page, BrowserContext

load_dotenv(os.path.join(os.path.dirname(__file__), ".env.local"))

BASE_URL = os.environ.get("BASE_URL", "http://localhost:81")
API_URL = os.environ.get("API_URL", "http://localhost:81/api")
PERF_EMAIL = os.environ.get("PERF_USER_EMAIL", "perfuser@local.test")
PERF_PASSWORD = os.environ.get("PERF_USER_PASSWORD", "")
HEADLESS = os.environ.get("HEADLESS", "true").lower() != "false"
SLOW_MO = int(os.environ.get("SLOW_MO_MS", "0"))
RUN_TIMEOUT = int(os.environ.get("RUN_TIMEOUT_MS", "45000"))
DELAY_BETWEEN_MS = int(os.environ.get("DELAY_BETWEEN_MS", "800"))
MAX_CONSECUTIVE_ERRORS = int(os.environ.get("MAX_CONSECUTIVE_ERRORS", "5"))


@dataclass
class ProblemResult:
    slug: str
    title: str
    difficulty: str
    passed: int = 0
    total: int = 0
    status: str = "unknown"
    runtime_ms: Optional[float] = None
    error: Optional[str] = None
    duration_s: float = 0.0

    @property
    def ok(self) -> bool:
        return self.passed == self.total and self.total > 0 and self.error is None


def login(api_url: str, email: str, password: str) -> str:
    resp = requests.post(
        f"{api_url}/auth/login",
        json={"email": email, "password": password},
        timeout=10,
    )
    if resp.status_code != 200:
        print(f"Login failed ({resp.status_code}): {resp.text}")
        sys.exit(1)
    token = resp.json().get("token")
    if not token:
        print(f"Login response missing token: {resp.text}")
        sys.exit(1)
    return token


def get_problem_solutions(api_url: str, jwt: str) -> list[dict]:
    resp = requests.get(
        f"{api_url}/dev/problem-solutions",
        headers={"Authorization": f"Bearer {jwt}"},
        timeout=10,
    )
    if resp.status_code == 404:
        print("ERROR: /dev/problem-solutions returned 404.")
        print("Make sure DEV_ENDPOINTS_ENABLED=true in backend environment.")
        sys.exit(1)
    if resp.status_code != 200:
        print(f"Failed to fetch solutions ({resp.status_code}): {resp.text}")
        sys.exit(1)
    data = resp.json()
    if not data:
        print("No problems with solutions found in the database.")
        sys.exit(0)
    return data


def run_problem(page: Page, jwt: str, slug: str, solution_code: str) -> tuple[str, int, int, Optional[float]]:
    """Navigate to problem, inject solution, click Run, return (status, passed, total, runtime_ms)."""
    problem_url = f"{BASE_URL}/problems/{slug}"

    page.evaluate(
        """([slug, code]) => {
            localStorage.setItem('pypycode:code:' + slug, code);
        }""",
        [slug, solution_code],
    )

    page.goto(problem_url, wait_until="domcontentloaded", timeout=15_000)

    run_btn = page.get_by_role("button", name="Run")
    run_btn.wait_for(state="visible", timeout=15_000)

    run_btn.click()

    page.wait_for_function(
        """() => {
            const spans = Array.from(document.querySelectorAll('span'));
            return spans.some(s => /\\d+\\/\\d+ tests passed/.test(s.textContent));
        }""",
        timeout=RUN_TIMEOUT,
    )

    result_text = page.evaluate(
        """() => {
            const spans = Array.from(document.querySelectorAll('span'));
            const s = spans.find(s => /\\d+\\/\\d+ tests passed/.test(s.textContent));
            return s ? s.textContent.trim() : '';
        }"""
    )

    status_text = page.evaluate(
        """() => {
            const spans = Array.from(document.querySelectorAll('span'));
            const badge = spans.find(s => s.className && s.className.includes('rounded-full') && s.className.includes('font-mono'));
            return badge ? badge.textContent.trim() : '';
        }"""
    )

    runtime_text = page.evaluate(
        """() => {
            const spans = Array.from(document.querySelectorAll('span.whitespace-nowrap'));
            const s = spans.find(s => /\\d+ms/.test(s.textContent));
            return s ? s.textContent.trim() : null;
        }"""
    )

    m = re.search(r"(\d+)/(\d+)", result_text)
    passed = int(m.group(1)) if m else 0
    total = int(m.group(2)) if m else 0

    runtime_ms = None
    if runtime_text:
        rm = re.search(r"(\d+)", runtime_text)
        if rm:
            runtime_ms = float(rm.group(1))

    status = "accepted" if passed == total and total > 0 else "failed"

    return status, passed, total, runtime_ms


def main():
    if not PERF_PASSWORD:
        print("Error: PERF_USER_PASSWORD is required (set in .env.local or env)")
        sys.exit(1)

    print(f"Logging in as {PERF_EMAIL}...")
    jwt = login(API_URL, PERF_EMAIL, PERF_PASSWORD)
    print("Login OK")

    print("Fetching problem solutions...")
    problems = get_problem_solutions(API_URL, jwt)
    print(f"Found {len(problems)} problem(s) with solutions\n")

    results: list[ProblemResult] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        context: BrowserContext = browser.new_context()
        page = context.new_page()

        page.goto(BASE_URL, wait_until="domcontentloaded", timeout=15_000)
        page.evaluate(f"localStorage.setItem('token', '{jwt}')")

        consecutive_errors = 0

        for idx, prob in enumerate(problems, 1):
            slug = prob["slug"]
            title = prob["title"]
            difficulty = prob["difficulty"]
            solution_code = prob["solutionCode"]

            result = ProblemResult(slug=slug, title=title, difficulty=difficulty)
            print(f"[{idx:3d}/{len(problems)}] {slug} ...", end="", flush=True)

            t0 = time.perf_counter()
            try:
                status, passed, total, runtime_ms = run_problem(page, jwt, slug, solution_code)
                result.status = status
                result.passed = passed
                result.total = total
                result.runtime_ms = runtime_ms
                consecutive_errors = 0
            except Exception as exc:
                result.error = str(exc)
                result.status = "error"
                consecutive_errors += 1
            finally:
                result.duration_s = time.perf_counter() - t0

            if result.ok:
                rt = f"{result.runtime_ms:.0f}ms" if result.runtime_ms else "—"
                print(f" ✓  {result.passed}/{result.total} passed  {rt}  ({result.duration_s:.1f}s)")
            else:
                print(f" ✗  {result.passed}/{result.total} passed  [{result.status}]  ({result.duration_s:.1f}s)")
                if result.error:
                    print(f"         Error: {result.error}")

            results.append(result)

            if consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
                print(f"\nAborted: {consecutive_errors} consecutive errors — worker is likely down.")
                print("Run: docker compose restart worker  then re-run the test.")
                break

            if DELAY_BETWEEN_MS > 0 and idx < len(problems):
                time.sleep(DELAY_BETWEEN_MS / 1000)

        browser.close()

    total_problems = len(results)
    passed_problems = sum(1 for r in results if r.ok)
    failed_problems = total_problems - passed_problems

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Total    : {total_problems}")
    print(f"  Passed   : {passed_problems} ✓")
    print(f"  Failed   : {failed_problems} ✗")

    if failed_problems:
        print()
        print("Failed problems:")
        for r in results:
            if not r.ok:
                label = r.error if r.error else f"{r.passed}/{r.total}"
                print(f"  - {r.slug}: {label}")
        sys.exit(1)
    else:
        print()
        print("All problems passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
