"""Tests for task delegation between persons.

Delegation uses the delegate_task tool: a commander calls delegate_fn
which executes a run_cycle on the worker's AgentCore.
"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock

import pytest

from tests.helpers.mocks import (
    make_litellm_response,
    make_tool_call,
    patch_litellm,
)


class TestDelegation:
    """Delegation tests using mocked LLM calls."""

    async def test_commander_delegates_to_worker(self, make_agent_core):
        """Commander delegates a task and receives the worker's result."""
        commander = make_agent_core(
            name="commander",
            model="openai/gpt-4o",
            role="commander",
        )

        # Set up delegate_fn that simulates worker response
        async def mock_delegate(target: str, task: str, context: str | None) -> str:
            return f"Worker completed: {task[:50]}"

        commander.set_delegate_fn(mock_delegate)

        # Commander's LLM calls delegate_task
        tc = make_tool_call(
            "delegate_task",
            {"to": "worker", "task": "Count to 5"},
            call_id="call_delegate",
        )
        resp1 = make_litellm_response(content="", tool_calls=[tc])
        resp2 = make_litellm_response(
            content="Worker said: Count to 5 completed."
        )

        with patch_litellm(resp1, resp2):
            result = await commander.run_cycle("Delegate counting to worker")

        assert result.summary

    async def test_delegate_to_nonexistent_person(self, make_agent_core):
        """Delegation to nonexistent person returns error gracefully."""
        commander = make_agent_core(
            name="commander-err",
            model="openai/gpt-4o",
            role="commander",
        )

        async def mock_delegate(target: str, task: str, context: str | None) -> str:
            return f"Error: Person '{target}' not found"

        commander.set_delegate_fn(mock_delegate)

        tc = make_tool_call(
            "delegate_task",
            {"to": "nonexistent", "task": "Do something"},
            call_id="call_delegate_err",
        )
        resp1 = make_litellm_response(content="", tool_calls=[tc])
        resp2 = make_litellm_response(
            content="The person was not found."
        )

        with patch_litellm(resp1, resp2):
            result = await commander.run_cycle("Delegate to nonexistent")

        assert result.summary

    async def test_delegate_timeout(self, make_agent_core):
        """Delegation times out when worker takes too long."""
        commander = make_agent_core(
            name="commander-timeout",
            model="openai/gpt-4o",
            role="commander",
        )

        # Set a very short timeout
        commander._DELEGATE_TIMEOUT_S = 1

        async def slow_delegate(target: str, task: str, context: str | None) -> str:
            await asyncio.sleep(10)
            return "This should not be reached"

        commander.set_delegate_fn(slow_delegate)

        tc = make_tool_call(
            "delegate_task",
            {"to": "slow-worker", "task": "Take forever"},
            call_id="call_delegate_slow",
        )
        resp1 = make_litellm_response(content="", tool_calls=[tc])
        resp2 = make_litellm_response(
            content="Delegation timed out."
        )

        with patch_litellm(resp1, resp2):
            result = await commander.run_cycle("Delegate slow task")

        assert result.summary
