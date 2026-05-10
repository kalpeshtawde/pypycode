import logging
from typing import Any, Dict

from constants import (
    ADVANCED_DISTRIBUTION,
    BEGINNER_DISTRIBUTION,
    INTERMEDIATE_DISTRIBUTION,
)
from enums import UserLevel
from schemas import DifficultyDistro


logger = logging.getLogger(__name__)


class ProblemSetGenerator:
    _difficulty_distro = DifficultyDistro()

    def __init__(self, stats: Dict[str, Any], total: int):
        if total < 0:
            raise ValueError("Total must be non-negative")
        self.stats = stats
        self.total = total
        self.level = UserLevel.BEGINNER

    def _difficulty_stats(self, difficulty: str) -> Dict[str, Any]:
        return self.stats.get(difficulty, {})

    def determine_level(self) -> UserLevel:
        hard_stats = self._difficulty_stats("hard")
        medium_stats = self._difficulty_stats("medium")
        if (
            hard_stats.get("attempted", 0) >= ADVANCED_HARD_ATTEMPT_THRESHOLD
            and hard_stats.get("score", 0) >= ADVANCED_HARD_SCORE_THRESHOLD
        ):
            logger.info("Determined user level", extra={"level": UserLevel.ADVANCED.value})
            return UserLevel.ADVANCED
        if medium_stats.get("score", 0) >= INTERMEDIATE_MEDIUM_SCORE_THRESHOLD:
            logger.info("Determined user level", extra={"level": UserLevel.INTERMEDIATE.value})
            return UserLevel.INTERMEDIATE
        if medium_stats.get("attempted", 0) == 0:
            logger.info("Determined user level", extra={"level": UserLevel.BEGINNER.value})
            return UserLevel.BEGINNER
        logger.info("Determined user level", extra={"level": UserLevel.BEGINNER.value})
        return UserLevel.BEGINNER

    def get_distribution_template(self, level: UserLevel) -> Dict[str, int]:
        return getattr(self._difficulty_distro, level.value).model_dump()

    @staticmethod
    def allocate_counts(distribution: Dict[str, int], total: int) -> Dict[str, int]:
        exact = {key: value / 100 * total for key, value in distribution.items()}
        floored = {key: int(value) for key, value in exact.items()}
        remainder = total - sum(floored.values())
        logger.info("Allocating problem counts", extra={"distribution": distribution, "exact": exact, "floored": floored, "remainder": remainder, "total": total})
        ranked_remainders = sorted(
            exact.keys(),
            key=lambda key: (-(exact[key] - floored[key]), key),
        )

        for key in ranked_remainders[:remainder]:
            floored[key] += 1

        logger.info("Allocated problem counts", extra={"allocated": floored})
        return floored

    def get_difficulty_split(self) -> Dict[str, int]:
        self.level = self.determine_level()
        distribution = self.get_distribution_template(self.level)
        return self.allocate_counts(distribution, self.total)
