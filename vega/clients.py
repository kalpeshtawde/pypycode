import logging
import httpx
from typing import Any, Dict, Optional

from vega.schemas import CreateProjectRequestPayload, ProblemSetRequestPayload

logger = logging.getLogger(__name__)


class BackendClient:
    def __init__(self, base_url: str, token: Optional[str]):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.client = httpx.AsyncClient(timeout=10.0)
        logger.info(
            "Initialized BackendClient",
            extra={"base_url": self.base_url, "has_token": bool(self.token)},
        )

    def _headers(self):
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    async def get_user_stat(self, user_id: str) -> Dict[str, Any]:
        logger.info("Fetching user stats", extra={"user_id": user_id})
        response = await self.client.get(
            f"{self.base_url}/submissions/difficulty-stats?userId=" f"{user_id}",
            headers=self._headers(),
        )
        if response.status_code != 200:
            logger.error(
                "Failed to fetch user stats",
                extra={
                    "user_id": user_id,
                    "status_code": response.status_code,
                    "response_text": response.text,
                },
            )
            raise Exception(f"Failed to fetch stats: {response.text}")

        payload = response.json()
        logger.info(
            "Fetched user stats",
            extra={"user_id": user_id, "payload_keys": list(payload.keys())},
        )

        return payload

    async def get_user_tag_stat(self, user_id: str) -> Dict[str, Any]:
        logger.info("Fetching user stats", extra={"user_id": user_id})
        response = await self.client.get(
            f"{self.base_url}/submissions/tag-stats?userId=" f"{user_id}",
            headers=self._headers(),
        )
        if response.status_code != 200:
            logger.error(
                "Failed to fetch user stats",
                extra={
                    "user_id": user_id,
                    "status_code": response.status_code,
                    "response_text": response.text,
                },
            )
            raise Exception(f"Failed to fetch stats: {response.text}")

        payload = response.json()
        logger.info(
            "Fetched user stats",
            extra={"user_id": user_id, "payload_keys": list(payload.keys())},
        )

        return payload

    async def problems_selector(self, payload: ProblemSetRequestPayload) -> dict:
        logger.info("Selecting problems", extra={"payload": payload.model_dump()})
        response = await self.client.post(
            f"{self.base_url}/problems/select",
            headers=self._headers(),
            json=payload.model_dump(),
        )
        if response.status_code != 200:
            logger.error(
                "Failed to select problems",
                extra={
                    "status_code": response.status_code,
                    "response_text": response.text,
                },
            )
            raise Exception(f"Failed to select problems: {response.text}")

        result = response.json()
        logger.info(
            "Selected problems",
            extra={
                "problem_count": len(result.get("problems", [])),
                "selection": result.get("selection"),
            },
        )
        return result

    async def create_project(self, payload: CreateProjectRequestPayload) -> dict:
        logger.info(
            "Creating project",
            extra={
                "project_name": payload.name,
                "problem_ids_count": len(payload.problemIds or []),
            },
        )
        response = await self.client.post(
            f"{self.base_url}/projects/",
            headers=self._headers(),
            json=payload.model_dump(exclude_none=True),
        )
        if response.status_code != 201:
            logger.error(
                "Failed to create project",
                extra={
                    "project_name": payload.name,
                    "status_code": response.status_code,
                    "response_text": response.text,
                },
            )
            raise Exception(f"Failed to create project: {response.text}")

        result = response.json()
        logger.info(
            "Created project",
            extra={"project_id": result.get("id"), "project_name": result.get("name")},
        )
        return result
