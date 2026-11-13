"""Torch-free JJC vocabulary, goals, and outcome utilities."""

from __future__ import annotations

from enum import IntEnum

import numpy as np


TEAM_SIZE = 5
OUTCOME_COUNT = 6


class OutcomeClass(IntEnum):
    WIN_0_15 = 0
    WIN_15_30 = 1
    WIN_30_60 = 2
    WIN_60_90 = 3
    LOSS = 4
    TIMEOUT = 5


class Goal(IntEnum):
    FAST_ATTACK = 0
    STALL_DEFENSE = 1

    @classmethod
    def parse(cls, value: str | int | "Goal") -> "Goal":
        if isinstance(value, cls):
            return value
        if isinstance(value, int):
            return cls(value)
        normalized = value.strip().upper().replace("-", "_")
        aliases = {
            "FAST": cls.FAST_ATTACK,
            "ATTACK": cls.FAST_ATTACK,
            "FAST_ATTACK": cls.FAST_ATTACK,
            "STALL": cls.STALL_DEFENSE,
            "DEFENSE": cls.STALL_DEFENSE,
            "STALL_DEFENSE": cls.STALL_DEFENSE,
        }
        try:
            return aliases[normalized]
        except KeyError as exc:
            raise ValueError(f"unknown JJC goal: {value}") from exc


OUTCOME_NAMES = tuple(item.name.lower() for item in OutcomeClass)
GOAL_UTILITIES = np.asarray(
    [
        [1.00, 0.80, 0.60, 0.40, -1.00, -0.80],
        [0.10, 0.30, 0.55, 0.80, -1.00, 1.00],
    ],
    dtype=np.float32,
)


def outcome_class(result: int, duration: float) -> OutcomeClass:
    if int(result) == 1:
        return OutcomeClass.LOSS
    if int(result) == 2:
        return OutcomeClass.TIMEOUT
    if int(result) != 0:
        raise ValueError(f"unsupported simulator result: {result}")
    duration = max(0.0, float(duration))
    if duration <= 15.0:
        return OutcomeClass.WIN_0_15
    if duration <= 30.0:
        return OutcomeClass.WIN_15_30
    if duration <= 60.0:
        return OutcomeClass.WIN_30_60
    return OutcomeClass.WIN_60_90


def critic_utility(probabilities: np.ndarray, goal: Goal | int) -> np.ndarray:
    probabilities = np.asarray(probabilities, dtype=np.float32)
    if probabilities.shape[-1] != len(OutcomeClass):
        raise ValueError("critic probabilities must have six outcome columns")
    return probabilities @ GOAL_UTILITIES[int(Goal.parse(goal))]


class UnitVocabulary:
    PAD = 0
    BOS = 1

    def __init__(self, unit_ids: list[int] | tuple[int, ...]) -> None:
        canonical = tuple(sorted({int(value) for value in unit_ids}))
        if not canonical:
            raise ValueError("unit vocabulary cannot be empty")
        self.unit_ids = canonical
        self._unit_to_index = {
            unit_id: index + 2 for index, unit_id in enumerate(self.unit_ids)
        }

    def __len__(self) -> int:
        return len(self.unit_ids) + 2

    def contains(self, unit_id: int) -> bool:
        return int(unit_id) in self._unit_to_index

    def encode_team(self, team: list[int] | tuple[int, ...]) -> np.ndarray:
        canonical = tuple(sorted(int(value) for value in team))
        if len(canonical) != TEAM_SIZE or len(set(canonical)) != TEAM_SIZE:
            raise ValueError("a team must contain five distinct unit IDs")
        try:
            return np.asarray(
                [self._unit_to_index[unit_id] for unit_id in canonical],
                dtype=np.int64,
            )
        except KeyError as exc:
            raise ValueError(f"unknown unit ID: {exc.args[0]}") from exc

    def decode_team(self, indices: list[int] | np.ndarray) -> tuple[int, ...]:
        values = tuple(int(value) for value in indices)
        if len(values) != TEAM_SIZE or any(
            value < 2 or value >= len(self) for value in values
        ):
            raise ValueError("invalid encoded team")
        team = tuple(self.unit_ids[value - 2] for value in values)
        if tuple(sorted(team)) != team or len(set(team)) != TEAM_SIZE:
            raise ValueError("decoded team is not canonical")
        return team

    def encode_available(
        self,
        unit_ids: list[int] | tuple[int, ...] | None,
    ) -> list[int]:
        if unit_ids is None:
            return list(range(2, len(self)))
        encoded = [
            self._unit_to_index[unit_id]
            for unit_id in sorted({int(value) for value in unit_ids})
            if unit_id in self._unit_to_index
        ]
        if len(encoded) < TEAM_SIZE:
            raise ValueError("available roster has fewer than five known units")
        return encoded

    def to_dict(self) -> dict[str, list[int]]:
        return {"unit_ids": list(self.unit_ids)}

    @classmethod
    def from_dict(cls, value: dict[str, list[int]]) -> "UnitVocabulary":
        return cls(value["unit_ids"])
