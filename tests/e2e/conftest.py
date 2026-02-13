"""E2E-specific fixtures for constructing AgentCore and DigitalPerson instances."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from core.agent import AgentCore
from core.memory import MemoryManager
from core.messenger import Messenger
from core.person import DigitalPerson


@pytest.fixture
def make_agent_core(data_dir: Path, make_person):
    """Factory to create an AgentCore instance with isolated filesystem.

    Bypasses DigitalPerson to test AgentCore directly.
    """

    def _make(name: str = "test-agent", **kwargs: Any) -> AgentCore:
        person_dir = make_person(name, **kwargs)
        memory = MemoryManager(person_dir)
        model_config = memory.read_model_config()
        messenger = Messenger(data_dir / "shared", name)
        return AgentCore(person_dir, memory, model_config, messenger)

    return _make


@pytest.fixture
def make_digital_person(data_dir: Path, make_person):
    """Factory to create a DigitalPerson instance with isolated filesystem."""

    def _make(name: str = "test-person", **kwargs: Any) -> DigitalPerson:
        person_dir = make_person(name, **kwargs)
        shared_dir = data_dir / "shared"
        return DigitalPerson(person_dir, shared_dir)

    return _make
