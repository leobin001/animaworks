"""Unit tests for supervisor-related functions in core/config/models.py.

Tests _resolve_supervisor_name(), read_person_supervisor(), and
register_person_in_config().
"""
from __future__ import annotations

import json
import logging
from pathlib import Path

import pytest

from core.config.models import (
    AnimaWorksConfig,
    PersonModelConfig,
    _resolve_supervisor_name,
    invalidate_cache,
    load_config,
    read_person_supervisor,
    register_person_in_config,
    save_config,
)


# ── Fixtures ─────────────────────────────────────────────────────


@pytest.fixture(autouse=True)
def _reset_config_cache() -> None:
    """Invalidate the config singleton before and after each test."""
    invalidate_cache()
    yield  # type: ignore[misc]
    invalidate_cache()


def _make_person(
    tmp_path: Path,
    name: str,
    identity_content: str | None = None,
    status_content: dict | None = None,
) -> Path:
    """Helper to create a person directory with optional identity.md and status.json."""
    person_dir = tmp_path / name
    person_dir.mkdir(parents=True, exist_ok=True)
    if identity_content is not None:
        (person_dir / "identity.md").write_text(identity_content, encoding="utf-8")
    if status_content is not None:
        (person_dir / "status.json").write_text(
            json.dumps(status_content, ensure_ascii=False), encoding="utf-8",
        )
    return person_dir


# ── _resolve_supervisor_name ─────────────────────────────────────


class TestResolveSupervisorName:
    """Tests for the raw supervisor name resolution function."""

    def test_fullwidth_parens(self) -> None:
        """Japanese name with full-width parenthesised English name."""
        assert _resolve_supervisor_name("琴葉（kotoha）") == "kotoha"

    def test_halfwidth_parens(self) -> None:
        """Japanese name with half-width parenthesised English name."""
        assert _resolve_supervisor_name("琴葉(kotoha)") == "kotoha"

    def test_plain_ascii(self) -> None:
        """Plain ASCII name is returned as-is (lowered)."""
        assert _resolve_supervisor_name("sakura") == "sakura"

    def test_uppercase_lowered(self) -> None:
        """Uppercase ASCII name is lowered."""
        assert _resolve_supervisor_name("Sakura") == "sakura"

    def test_nashi_halfwidth_parens(self) -> None:
        """Half-width (なし) returns None."""
        assert _resolve_supervisor_name("(なし)") is None

    def test_nashi_bare(self) -> None:
        """Bare なし returns None."""
        assert _resolve_supervisor_name("なし") is None

    def test_nashi_fullwidth_parens(self) -> None:
        """Full-width （なし） returns None."""
        assert _resolve_supervisor_name("（なし）") is None

    def test_dash(self) -> None:
        """Dash value returns None."""
        assert _resolve_supervisor_name("-") is None

    def test_empty_string(self) -> None:
        """Empty string returns None."""
        assert _resolve_supervisor_name("") is None

    def test_whitespace_only(self) -> None:
        """Whitespace-only string returns None after stripping."""
        assert _resolve_supervisor_name("   ") is None

    def test_japanese_only_no_english(self, caplog: pytest.LogCaptureFixture) -> None:
        """Japanese-only name without English in parens returns None with warning."""
        with caplog.at_level(logging.WARNING, logger="animaworks.config"):
            result = _resolve_supervisor_name("純日本語名")
        assert result is None
        assert "no English name" in caplog.text

    def test_mixed_case_in_parens(self) -> None:
        """Mixed-case English name in parens is lowered."""
        assert _resolve_supervisor_name("凛堂 凛（Rin）") == "rin"

    def test_underscore_in_name(self) -> None:
        """Name with underscores is accepted."""
        assert _resolve_supervisor_name("chatwork_checker") == "chatwork_checker"

    def test_triple_dash(self) -> None:
        """Triple-dash is treated as none value."""
        assert _resolve_supervisor_name("---") is None

    def test_leading_trailing_whitespace(self) -> None:
        """Leading/trailing whitespace is stripped before resolution."""
        assert _resolve_supervisor_name("  sakura  ") == "sakura"


# ── read_person_supervisor ───────────────────────────────────────


class TestReadPersonSupervisor:
    """Tests for reading supervisor from status.json / identity.md."""

    def test_status_json_with_supervisor(self, tmp_path: Path) -> None:
        """Reads supervisor from status.json when present."""
        person_dir = _make_person(
            tmp_path, "hinata",
            status_content={"supervisor": "kotoha"},
        )
        assert read_person_supervisor(person_dir) == "kotoha"

    def test_status_json_without_supervisor_falls_to_identity(
        self, tmp_path: Path,
    ) -> None:
        """Falls through to identity.md when status.json lacks supervisor."""
        person_dir = _make_person(
            tmp_path, "hinata",
            identity_content="| 上司 | 琴葉（kotoha） |\n",
            status_content={"enabled": True},
        )
        assert read_person_supervisor(person_dir) == "kotoha"

    def test_identity_md_table_fullwidth_parens(self, tmp_path: Path) -> None:
        """Parses supervisor from identity.md table with full-width parens."""
        person_dir = _make_person(
            tmp_path, "hinata",
            identity_content=(
                "| 項目 | 設定 |\n"
                "|------|------|\n"
                "| 上司 | 琴葉（kotoha） |\n"
            ),
        )
        assert read_person_supervisor(person_dir) == "kotoha"

    def test_no_status_json_no_identity_md(self, tmp_path: Path) -> None:
        """Returns None when neither file exists."""
        person_dir = _make_person(tmp_path, "hinata")
        assert read_person_supervisor(person_dir) is None

    def test_status_json_empty_supervisor_falls_to_identity(
        self, tmp_path: Path,
    ) -> None:
        """Falls through to identity.md when status.json supervisor is empty."""
        person_dir = _make_person(
            tmp_path, "hinata",
            identity_content="| 上司 | sakura |\n",
            status_content={"supervisor": ""},
        )
        assert read_person_supervisor(person_dir) == "sakura"

    def test_status_json_takes_priority(self, tmp_path: Path) -> None:
        """status.json supervisor wins over identity.md when both present."""
        person_dir = _make_person(
            tmp_path, "hinata",
            identity_content="| 上司 | alice |\n",
            status_content={"supervisor": "bob"},
        )
        assert read_person_supervisor(person_dir) == "bob"

    def test_status_json_nashi_falls_to_identity(self, tmp_path: Path) -> None:
        """status.json with なし resolves to None, falls to identity.md."""
        person_dir = _make_person(
            tmp_path, "hinata",
            identity_content="| 上司 | sakura |\n",
            status_content={"supervisor": "なし"},
        )
        # "なし" resolves to None in _resolve_supervisor_name, so it falls through
        assert read_person_supervisor(person_dir) == "sakura"

    def test_identity_no_supervisor_row(self, tmp_path: Path) -> None:
        """Returns None when identity.md has no supervisor row."""
        person_dir = _make_person(
            tmp_path, "hinata",
            identity_content="# Identity\n| 項目 | 設定 |\n| 誕生日 | 1月1日 |\n",
        )
        assert read_person_supervisor(person_dir) is None

    def test_invalid_status_json(self, tmp_path: Path) -> None:
        """Returns None when status.json is invalid JSON."""
        person_dir = tmp_path / "hinata"
        person_dir.mkdir(parents=True)
        (person_dir / "status.json").write_text("not valid json", encoding="utf-8")
        assert read_person_supervisor(person_dir) is None

    def test_identity_embedded_in_real_file(self, tmp_path: Path) -> None:
        """Extracts supervisor from a realistic multi-row identity.md."""
        person_dir = _make_person(
            tmp_path, "hinata",
            identity_content=(
                "# Identity: hinata\n\n"
                "## 基本プロフィール\n\n"
                "| 項目 | 設定 |\n"
                "|------|------|\n"
                "| 誕生日 | 3月21日 |\n"
                "| 上司 | 凛堂 凛（rin） |\n"
                "| 身長 | 155cm |\n\n"
                "## 性格\nGenki.\n"
            ),
        )
        assert read_person_supervisor(person_dir) == "rin"

    def test_nonexistent_person_dir(self, tmp_path: Path) -> None:
        """Returns None when person directory does not exist."""
        assert read_person_supervisor(tmp_path / "nonexistent") is None


# ── register_person_in_config ────────────────────────────────────


class TestRegisterPersonInConfig:
    """Tests for registering a person in config.json with supervisor synced."""

    def test_registers_new_person_with_supervisor(self, tmp_path: Path) -> None:
        """New person with status.json supervisor is registered correctly."""
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        persons_dir = data_dir / "persons"
        persons_dir.mkdir()

        # Create config.json
        config = AnimaWorksConfig(setup_complete=True)
        save_config(config, data_dir / "config.json")
        invalidate_cache()

        # Create person directory with supervisor
        _make_person(
            persons_dir, "hinata",
            identity_content="| 上司 | sakura |\n",
        )

        register_person_in_config(data_dir, "hinata")

        invalidate_cache()
        cfg = load_config(data_dir / "config.json")
        assert "hinata" in cfg.persons
        assert cfg.persons["hinata"].supervisor == "sakura"

    def test_registers_new_person_without_supervisor(self, tmp_path: Path) -> None:
        """New person without supervisor source is registered with supervisor=None."""
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        persons_dir = data_dir / "persons"
        persons_dir.mkdir()

        # Create config.json
        config = AnimaWorksConfig(setup_complete=True)
        save_config(config, data_dir / "config.json")
        invalidate_cache()

        # Create person directory without supervisor info
        _make_person(
            persons_dir, "hinata",
            identity_content="# Identity\nNo supervisor info.\n",
        )

        register_person_in_config(data_dir, "hinata")

        invalidate_cache()
        cfg = load_config(data_dir / "config.json")
        assert "hinata" in cfg.persons
        assert cfg.persons["hinata"].supervisor is None

    def test_existing_person_is_noop(self, tmp_path: Path) -> None:
        """Person already in config is not modified."""
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        persons_dir = data_dir / "persons"
        persons_dir.mkdir()

        # Create config.json with existing person
        config = AnimaWorksConfig(setup_complete=True)
        config.persons["hinata"] = PersonModelConfig(
            model="openai/gpt-4o",
            supervisor="original",
        )
        save_config(config, data_dir / "config.json")
        invalidate_cache()

        # Create person directory with different supervisor
        _make_person(
            persons_dir, "hinata",
            identity_content="| 上司 | different |\n",
        )

        register_person_in_config(data_dir, "hinata")

        invalidate_cache()
        cfg = load_config(data_dir / "config.json")
        assert cfg.persons["hinata"].supervisor == "original"
        assert cfg.persons["hinata"].model == "openai/gpt-4o"

    def test_config_json_does_not_exist(self, tmp_path: Path) -> None:
        """No error when config.json does not exist."""
        data_dir = tmp_path / "data"
        data_dir.mkdir()

        # No config.json created — should return without error
        register_person_in_config(data_dir, "hinata")
        # No assertion needed — just verifying no exception is raised

    def test_person_dir_does_not_exist(self, tmp_path: Path) -> None:
        """Registers person with supervisor=None when person dir is missing."""
        data_dir = tmp_path / "data"
        data_dir.mkdir()

        # Create config.json but no persons directory
        config = AnimaWorksConfig(setup_complete=True)
        save_config(config, data_dir / "config.json")
        invalidate_cache()

        register_person_in_config(data_dir, "hinata")

        invalidate_cache()
        cfg = load_config(data_dir / "config.json")
        assert "hinata" in cfg.persons
        assert cfg.persons["hinata"].supervisor is None

    def test_registers_with_status_json_supervisor(self, tmp_path: Path) -> None:
        """Person registered with supervisor from status.json when identity.md has none."""
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        persons_dir = data_dir / "persons"
        persons_dir.mkdir()

        config = AnimaWorksConfig(setup_complete=True)
        save_config(config, data_dir / "config.json")
        invalidate_cache()

        _make_person(
            persons_dir, "hinata",
            identity_content="# Identity\nNo supervisor.\n",
            status_content={"supervisor": "kotoha"},
        )

        register_person_in_config(data_dir, "hinata")

        invalidate_cache()
        cfg = load_config(data_dir / "config.json")
        assert cfg.persons["hinata"].supervisor == "kotoha"
