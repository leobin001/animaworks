# AnimaWorks - Digital Anima Framework
# Copyright (C) 2026 AnimaWorks Authors
# SPDX-License-Identifier: Apache-2.0

"""Unit tests for core/memory/_llm_utils.py."""

from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import pytest

import core.memory._llm_utils as llm_utils

# ── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture(autouse=True)
def reset_credentials_exported() -> None:
    """Reset _credentials_exported between tests so ensure_credentials_in_env runs."""
    yield
    llm_utils._credentials_exported = False


def _make_cred(api_key: str = "") -> MagicMock:
    """Create a CredentialConfig-like mock with api_key attribute."""
    cred = MagicMock()
    cred.api_key = api_key
    return cred


def _make_config(
    llm_model: str = "anthropic/claude-sonnet-4-6",
    credentials: dict[str, MagicMock] | None = None,
) -> MagicMock:
    """Create a config mock with consolidation and credentials."""
    cfg = MagicMock()
    cfg.consolidation.llm_model = llm_model
    cfg.credentials = credentials or {}
    return cfg


# ── get_consolidation_llm_kwargs ──────────────────────────────────────────────


class TestGetConsolidationLlmKwargs:
    """Tests for get_consolidation_llm_kwargs()."""

    def test_returns_model_from_config(self) -> None:
        """get_consolidation_llm_kwargs returns dict with 'model' key from config."""
        cfg = _make_config(llm_model="anthropic/claude-sonnet-4-6")
        with patch("core.config.load_config", return_value=cfg):
            result = llm_utils.get_consolidation_llm_kwargs()
        assert result["model"] == "anthropic/claude-sonnet-4-6"

    def test_includes_api_key_when_credential_exists(self) -> None:
        """get_consolidation_llm_kwargs includes api_key when credential exists."""
        cred = _make_cred(api_key="sk-test-key")
        cfg = _make_config(
            llm_model="anthropic/claude-sonnet-4-6",
            credentials={"anthropic": cred},
        )
        with patch("core.config.load_config", return_value=cfg):
            result = llm_utils.get_consolidation_llm_kwargs()
        assert result["model"] == "anthropic/claude-sonnet-4-6"
        assert result["api_key"] == "sk-test-key"

    def test_works_without_api_key_model_only(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """get_consolidation_llm_kwargs works without api_key (model only)."""
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        cfg = _make_config(
            llm_model="anthropic/claude-sonnet-4-6",
            credentials={"anthropic": _make_cred(api_key="")},
        )
        with patch("core.config.load_config", return_value=cfg):
            result = llm_utils.get_consolidation_llm_kwargs()
        assert result["model"] == "anthropic/claude-sonnet-4-6"
        assert "api_key" not in result


# ── ensure_credentials_in_env ─────────────────────────────────────────────────


class TestEnsureCredentialsInEnv:
    """Tests for ensure_credentials_in_env()."""

    def test_exports_credentials_to_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """ensure_credentials_in_env exports credentials to environment."""
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        cred = _make_cred(api_key="sk-exported")
        cfg = _make_config(credentials={"anthropic": cred})
        with patch("core.config.load_config", return_value=cfg):
            llm_utils.ensure_credentials_in_env()
        assert os.environ.get("ANTHROPIC_API_KEY") == "sk-exported"

    def test_does_not_overwrite_existing_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """ensure_credentials_in_env does not overwrite existing env vars."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "existing-key")
        cred = _make_cred(api_key="sk-from-config")
        cfg = _make_config(credentials={"anthropic": cred})
        with patch("core.config.load_config", return_value=cfg):
            llm_utils.ensure_credentials_in_env()
        assert os.environ.get("ANTHROPIC_API_KEY") == "existing-key"

    def test_runs_only_once_idempotent(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """ensure_credentials_in_env runs only once (idempotent)."""
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        cred = _make_cred(api_key="sk-first")
        cfg = _make_config(credentials={"anthropic": cred})
        with patch("core.config.load_config", return_value=cfg) as mock_load:
            llm_utils.ensure_credentials_in_env()
            llm_utils.ensure_credentials_in_env()
            llm_utils.ensure_credentials_in_env()
        # load_config called once in ensure_credentials_in_env (first run only)
        assert mock_load.call_count == 1
        assert os.environ.get("ANTHROPIC_API_KEY") == "sk-first"

    def test_silently_returns_on_config_load_failure(self) -> None:
        """ensure_credentials_in_env silently returns on config load failure."""
        with patch("core.config.load_config", side_effect=RuntimeError("config error")):
            llm_utils.ensure_credentials_in_env()
        # No exception raised; function returns normally
