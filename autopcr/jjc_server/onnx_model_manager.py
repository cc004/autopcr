"""CPU ONNX inference for the bundled JJC generator and six-outcome Critic."""

from __future__ import annotations

import hashlib
import itertools
import json
import logging
import math
import random
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from .runtime_models import Goal, UnitVocabulary, critic_utility


DEFAULT_CRITIC_RETAIN_CANDIDATES = 32
DEFAULT_EXPLORATION_CANDIDATES = 4
DEFAULT_SIMULATE_CANDIDATES = 36
BUNDLE_FORMAT = "autopcr_jjc_onnx_v1"


def _softmax(logits: np.ndarray) -> np.ndarray:
    values = np.asarray(logits, dtype=np.float64)
    maximum = values.max(axis=-1, keepdims=True)
    if not np.isfinite(maximum).all():
        raise ValueError("ONNX 模型没有可用的合法角色")
    weights = np.exp(values - maximum)
    return weights / weights.sum(axis=-1, keepdims=True)


class JJCModelManager:
    """Keep the record manager's inference interface without importing Torch."""

    def __init__(
        self,
        transformer_checkpoint: str | Path,
        critic_checkpoint: str | Path,
        device: str = "auto",
    ) -> None:
        if device not in {"auto", "cpu"}:
            raise ValueError("JJC ONNX inference uses CPUExecutionProvider")
        self.transformer_output_path = Path(transformer_checkpoint).expanduser().resolve()
        self.critic_output_path = Path(critic_checkpoint).expanduser().resolve()
        self.set_checkpoints(transformer_checkpoint, critic_checkpoint)
        self.transformer: Any = None
        self.critic: Any = None
        self.vocabulary: UnitVocabulary | None = None
        self.metadata: dict[str, Any] = {}
        self.device = "cpu"
        self._loaded_checkpoint_paths: tuple[Path, Path] | None = None

    @property
    def checkpoint_paths(self) -> tuple[Path, Path]:
        return self.transformer_checkpoint_path, self.critic_checkpoint_path

    @property
    def is_loaded(self) -> bool:
        return self.transformer is not None and self.critic is not None and self.vocabulary is not None

    def set_checkpoints(self, transformer_checkpoint: str | Path, critic_checkpoint: str | Path) -> None:
        generator = Path(transformer_checkpoint).expanduser().resolve()
        critic = Path(critic_checkpoint).expanduser().resolve()
        if generator == critic:
            raise ValueError("Generator and Critic must use different model files")
        self.transformer_checkpoint_path, self.critic_checkpoint_path = generator, critic

    def load(
        self,
        transformer_checkpoint: str | Path | None = None,
        critic_checkpoint: str | Path | None = None,
        *,
        force: bool = False,
    ) -> dict[str, Any]:
        if (transformer_checkpoint is None) != (critic_checkpoint is None):
            raise ValueError("both Generator and Critic paths are required")
        if transformer_checkpoint is not None and critic_checkpoint is not None:
            self.set_checkpoints(transformer_checkpoint, critic_checkpoint)
        if self.is_loaded and not force and self._loaded_checkpoint_paths == self.checkpoint_paths:
            return self.model_info()
        generator, critic = self.checkpoint_paths
        for path in (generator, critic):
            if not path.is_file():
                raise FileNotFoundError(path)
            if path.suffix != ".onnx":
                raise ValueError("JJC 运行时仅支持 ONNX，请先离线导出模型")
        if generator.parent != critic.parent:
            raise ValueError("Generator and Critic must belong to the same ONNX bundle")
        root = generator.parent
        manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        if manifest.get("format") != BUNDLE_FORMAT:
            raise ValueError("unsupported JJC ONNX bundle format")
        files = manifest.get("files", {})
        required = {generator.name, critic.name, "vocabulary.json"}
        if not required <= files.keys():
            raise ValueError("incomplete JJC ONNX bundle manifest")
        for filename, expected in files.items():
            if Path(filename).name != filename:
                raise ValueError("invalid ONNX bundle filename")
            actual = hashlib.sha256((root / filename).read_bytes()).hexdigest()
            if actual != expected:
                raise ValueError(f"ONNX bundle checksum mismatch: {filename}")
        payload = json.loads((root / "vocabulary.json").read_text(encoding="utf-8"))
        vocabulary = UnitVocabulary.from_dict(payload)
        if list(vocabulary.unit_ids) != payload["unit_ids"] or len(vocabulary.unit_ids) < 5:
            raise ValueError("invalid ONNX model vocabulary")

        import onnxruntime as ort

        options = ort.SessionOptions()
        options.intra_op_num_threads = 2
        options.inter_op_num_threads = 1
        transformer = ort.InferenceSession(str(generator), sess_options=options, providers=["CPUExecutionProvider"])
        critic_session = ort.InferenceSession(str(critic), sess_options=options, providers=["CPUExecutionProvider"])
        probe = np.asarray([[2, 3, 4, 5, 6]], dtype=np.int64)
        tokens = np.asarray([[1, 0, 0, 0, 0]], dtype=np.int64)
        logits = transformer.run(["logits"], {"opponents": probe, "decoder_tokens": tokens, "goals": np.zeros(1, dtype=np.int64)})[0]
        outcomes = critic_session.run(["outcomes"], {"attacks": probe, "defends": probe})[0]
        if logits.shape != (1, 5, len(vocabulary)) or outcomes.shape != (1, 6):
            raise ValueError("ONNX model output does not match its vocabulary/outcome schema")
        if not np.isfinite(logits).all() or not np.isfinite(outcomes).all():
            raise ValueError("ONNX model produced non-finite output")
        self.transformer, self.critic = transformer, critic_session
        self.vocabulary = vocabulary
        self.metadata = manifest
        self._loaded_checkpoint_paths = self.checkpoint_paths
        return self.model_info()

    def load_if_available(self) -> bool:
        try:
            self.load()
            return True
        except Exception as exc:
            logging.warning("JJC ONNX inference unavailable: %s", exc)
            return False

    def model_info(self) -> dict[str, Any]:
        return {
            "model_version": self.metadata.get("model_version"),
            "training_completed_at": self.metadata.get("training_completed_at"),
            "transformer_checkpoint": str(self.transformer_checkpoint_path),
            "critic_checkpoint": str(self.critic_checkpoint_path),
            "device": "cpu",
            "backend": "onnxruntime",
        }

    def supports_team(self, team: Sequence[int]) -> bool:
        return self.vocabulary is not None and all(self.vocabulary.contains(unit) for unit in team)

    def recall(
        self,
        opponent: Sequence[int],
        goal: Any,
        *,
        roster: Sequence[int] | None = None,
        candidate_count: int = 256,
        generation_batch_size: int = 64,
        temperature: float = 1.0,
        top_p: float = 0.95,
        seed: int = 42,
    ) -> list[tuple[int, ...]]:
        self.load()
        assert self.vocabulary is not None
        if candidate_count <= 0 or generation_batch_size <= 0:
            raise ValueError("candidate_count and generation_batch_size must be positive")
        if not math.isfinite(temperature) or temperature <= 0 or not 0 < top_p <= 1:
            raise ValueError("temperature must be positive and top_p must be in (0, 1]")
        encoded = self.vocabulary.encode_team(tuple(opponent))
        available = np.asarray(self.vocabulary.encode_available(None if roster is None else list(roster)), dtype=np.int64)
        goal_id = int(Goal.parse(goal))
        target = min(candidate_count, math.comb(len(available), 5))
        if math.comb(len(available), 5) <= candidate_count:
            return [self.vocabulary.decode_team(team) for team in itertools.combinations(available, 5)]
        rng = np.random.default_rng(seed)
        unique: dict[tuple[int, ...], None] = {}
        for _ in range(max(20, candidate_count * 10 // generation_batch_size)):
            batch = min(generation_batch_size, target - len(unique) + 16)
            defenders = np.tile(encoded, (batch, 1))
            tokens = np.zeros((batch, 5), dtype=np.int64)
            tokens[:, 0] = UnitVocabulary.BOS
            selected = np.zeros((batch, 5), dtype=np.int64)
            goals = np.full(batch, goal_id, dtype=np.int64)
            for step in range(5):
                raw = self.transformer.run(["logits"], {"opponents": defenders, "decoder_tokens": tokens, "goals": goals})[0]
                if raw.shape != (batch, 5, len(self.vocabulary)) or not np.isfinite(raw).all():
                    raise ValueError("ONNX generator output shape or values are invalid")
                logits = np.asarray(raw[:, step], dtype=np.float64) / temperature
                legal = np.zeros_like(logits, dtype=bool)
                legal[:, available[:len(available) - (4 - step)]] = True
                if step:
                    legal &= np.arange(len(self.vocabulary))[None] > selected[:, step - 1, None]
                logits[~legal] = -np.inf
                probabilities = _softmax(logits)
                order = np.argsort(-probabilities, axis=-1, kind="stable")
                weights = np.take_along_axis(probabilities, order, axis=-1)
                weights[np.cumsum(weights, axis=-1) - weights >= top_p] = 0
                weights /= weights.sum(axis=-1, keepdims=True)
                cumulative = np.cumsum(weights, axis=-1)
                cumulative /= cumulative[:, -1:]
                ranks = (cumulative < rng.random((batch, 1))).sum(axis=-1).clip(max=weights.shape[1] - 1)
                chosen = order[np.arange(batch), ranks]
                selected[:, step] = chosen
                if step < 4:
                    tokens[:, step + 1] = chosen
            for row in selected:
                unique[self.vocabulary.decode_team(row)] = None
            if len(unique) >= target:
                break
        if len(unique) < min(target, 5):
            raise RuntimeError("ONNX generator did not produce enough distinct legal teams")
        return list(unique)[:target]

    def rank(
        self,
        candidates: Sequence[Sequence[int]],
        opponent: Sequence[int],
        goal: Any,
        *,
        batch_size: int = 128,
    ) -> tuple[np.ndarray, np.ndarray]:
        self.load()
        assert self.vocabulary is not None
        if batch_size <= 0:
            raise ValueError("batch_size must be positive")
        parsed_goal = Goal.parse(goal)
        defender = self.vocabulary.encode_team(tuple(opponent))
        chunks = []
        for offset in range(0, len(candidates), batch_size):
            attacks = np.stack([self.vocabulary.encode_team(tuple(team)) for team in candidates[offset:offset + batch_size]])
            logits = self.critic.run(["outcomes"], {"attacks": attacks, "defends": np.tile(defender, (len(attacks), 1))})[0]
            if logits.shape != (len(attacks), 6) or not np.isfinite(logits).all():
                raise ValueError("ONNX Critic output shape or values are invalid")
            chunks.append(_softmax(logits).astype(np.float32))
        probabilities = np.concatenate(chunks) if chunks else np.empty((0, 6), dtype=np.float32)
        return probabilities, critic_utility(probabilities, parsed_goal)

    def infer(
        self, opponent: Sequence[int], goal: Any, *, roster: Sequence[int] | None = None,
        candidates: int = 256, simulate_candidates: int = DEFAULT_SIMULATE_CANDIDATES,
        exploration_candidates: int = DEFAULT_EXPLORATION_CANDIDATES,
        generation_batch_size: int = 64, batch_size: int = 128,
        temperature: float = 1.0, top_p: float = 0.95, seed: int = 42,
    ) -> dict[str, Any]:
        generated = self.recall(opponent, goal, roster=roster, candidate_count=candidates,
                                generation_batch_size=generation_batch_size, temperature=temperature,
                                top_p=top_p, seed=seed)
        probabilities, scores = self.rank(generated, opponent, goal, batch_size=batch_size)
        count = min(max(0, simulate_candidates), len(scores))
        exploration = min(max(0, exploration_candidates), count)
        order = np.argsort(-scores).tolist()
        selected = order[:count - exploration]
        selected.extend(random.Random(seed).sample(order[count - exploration:], exploration))
        return {"generated": generated, "probabilities": probabilities, "scores": scores, "selected": selected}

    def suggest(
        self, opponent: Sequence[int], historical_candidates: Sequence[Sequence[int]], *,
        wanted: int, goal: Any = "fast_attack",
    ) -> list[tuple[int, ...]]:
        self.load()
        Goal.parse(goal)
        if not self.supports_team(opponent):
            # Frozen ONNX embeddings cannot expand for a new role; keep the
            # history ordering instead of inventing an embedding or a score.
            return list(dict.fromkeys(tuple(sorted(team)) for team in historical_candidates
                                      if len(team) == 5 and len(set(team)) == 5))[:max(0, wanted)]
        generated = self.recall(opponent, goal, candidate_count=max(64, wanted * 4),
                                generation_batch_size=min(64, max(8, wanted * 2)))
        distinct = list(dict.fromkeys(tuple(sorted(team)) for team in [*historical_candidates, *generated]
                                     if len(set(team)) == 5 and self.supports_team(team)))
        if not distinct:
            return []
        _, scores = self.rank(distinct, opponent, goal)
        return [distinct[index] for index in np.argsort(-scores)[:max(0, wanted)]]
