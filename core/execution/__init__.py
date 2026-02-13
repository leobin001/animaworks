"""Execution engines for AgentCore.

Each engine implements one execution mode:
  - ``AgentSDKExecutor``  (A1): Claude Agent SDK — full tool access via subprocess
  - ``LiteLLMExecutor``   (A2): LiteLLM + tool_use loop — any model with tool support
  - ``AssistedExecutor``  (B):  1-shot LLM call — framework handles memory I/O
  - ``AnthropicFallbackExecutor``: Anthropic SDK direct — fallback when Agent SDK unavailable
"""
from __future__ import annotations

from core.execution.agent_sdk import AgentSDKExecutor
from core.execution.anthropic_fallback import AnthropicFallbackExecutor
from core.execution.assisted import AssistedExecutor
from core.execution.base import BaseExecutor, ExecutionResult
from core.execution.litellm_loop import LiteLLMExecutor

__all__ = [
    "AgentSDKExecutor",
    "AnthropicFallbackExecutor",
    "AssistedExecutor",
    "BaseExecutor",
    "ExecutionResult",
    "LiteLLMExecutor",
]
