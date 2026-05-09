import asyncio
import logging
from uuid import uuid4

from vega.constants import (
    DEFAULT_AUTH_TOKEN,
    DEFAULT_BACKEND_BASE_URL,
    DEFAULT_USER_ID,
    DEFAULT_TOTAL_QUESTIONS,
)
from vega.clients import BackendClient
from vega.problem_set_generator import ProblemSetGenerator
from vega.schemas import CreateProjectRequestPayload, DifficultyCountPayload, ProblemSetRequestPayload


logger = logging.getLogger(__name__)


class BuildProject:
    def __init__(self, user_id):
        self.user_id = user_id

    async def build(self):
        logger.info("Starting build project flow", extra={"user_id": self.user_id})
        client = BackendClient(DEFAULT_BACKEND_BASE_URL, DEFAULT_AUTH_TOKEN)

        stats = await client.get_user_stat(self.user_id)
        logger.info("Retrieved quiz stats", extra={"user_id": self.user_id, "last_attempt_at": stats.get("lastAttemptAt")})

        problem_set = ProblemSetGenerator(stats, DEFAULT_TOTAL_QUESTIONS).get_difficulty_split()
        logger.info("Generated problem set distribution", extra={"distribution": problem_set, "total_questions": DEFAULT_TOTAL_QUESTIONS})
        payload = ProblemSetRequestPayload(
            difficultyCounts=DifficultyCountPayload(**problem_set),
            ignoreSlugs=[],
            tagWeights={},
            total=DEFAULT_TOTAL_QUESTIONS,
        )
        selected_problems = await client.problems_selector(payload)
        selected_problem_ids = [problem["id"] for problem in selected_problems.get("problems", []) if problem.get("id")]
        logger.info("Extracted selected problem ids", extra={"selected_problem_ids": selected_problem_ids, "selected_count": len(selected_problem_ids)})
        project_payload = CreateProjectRequestPayload(
            name=f"Vega-{uuid4().hex[:8]}",
            problemIds=selected_problem_ids,
        )
        project = await client.create_project(project_payload)
        logger.info("Completed build project flow", extra={"project": project})
        print(project)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
p = BuildProject(DEFAULT_USER_ID)
asyncio.run(p.build())
