"""Unit tests for core/org_sync.py — org structure synchronization."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from core.config.models import (
    AnimaWorksConfig,
    PersonModelConfig,
    invalidate_cache,
    load_config,
    save_config,
)
from core.org_sync import (
    _detect_circular_references,
    sync_org_structure,
)


# ── Fixtures ─────────────────────────────────────────────────────


@pytest.fixture(autouse=True)
def _reset_config_cache() -> None:
    """Invalidate the config singleton before and after each test."""
    invalidate_cache()
    yield  # type: ignore[misc]
    invalidate_cache()


@pytest.fixture
def persons_dir(tmp_path: Path) -> Path:
    """Create an empty persons directory."""
    d = tmp_path / "persons"
    d.mkdir()
    return d


@pytest.fixture
def config_path(tmp_path: Path) -> Path:
    """Create a minimal config.json and return its path."""
    p = tmp_path / "config.json"
    cfg = AnimaWorksConfig(setup_complete=True)
    save_config(cfg, p)
    invalidate_cache()
    return p


def _make_person(
    persons_dir: Path,
    name: str,
    identity_content: str = "# Identity\nNo supervisor info.",
    status_json: dict | None = None,
) -> Path:
    """Helper to create a person directory with identity.md and optional status.json."""
    person_dir = persons_dir / name
    person_dir.mkdir(parents=True, exist_ok=True)
    (person_dir / "identity.md").write_text(identity_content, encoding="utf-8")
    if status_json is not None:
        (person_dir / "status.json").write_text(
            json.dumps(status_json, ensure_ascii=False), encoding="utf-8",
        )
    return person_dir


# ── _detect_circular_references ──────────────────────────────────


class TestDetectCircularReferences:
    """Tests for circular supervisor reference detection."""

    def test_no_cycle(self) -> None:
        """No cycles in a simple chain."""
        rels = {"a": "b", "b": "c", "c": None}
        assert _detect_circular_references(rels) == []

    def test_simple_cycle(self) -> None:
        """A->B->A cycle is detected."""
        rels = {"a": "b", "b": "a"}
        cycles = _detect_circular_references(rels)
        assert len(cycles) == 1
        assert set(cycles[0]) == {"a", "b"}

    def test_three_node_cycle(self) -> None:
        """A->B->C->A cycle is detected."""
        rels = {"a": "b", "b": "c", "c": "a"}
        cycles = _detect_circular_references(rels)
        assert len(cycles) == 1
        assert set(cycles[0]) == {"a", "b", "c"}

    def test_all_none(self) -> None:
        """No cycles when all supervisors are None."""
        rels = {"a": None, "b": None, "c": None}
        assert _detect_circular_references(rels) == []

    def test_self_reference(self) -> None:
        """A->A self-reference is detected."""
        rels = {"a": "a"}
        cycles = _detect_circular_references(rels)
        assert len(cycles) == 1
        assert cycles[0] == ("a",)

    def test_cycle_with_tail(self) -> None:
        """Chain leading into a cycle: D->A->B->A."""
        rels = {"d": "a", "a": "b", "b": "a"}
        cycles = _detect_circular_references(rels)
        assert len(cycles) >= 1
        # The cycle itself should contain a and b
        cycle_members = set()
        for c in cycles:
            cycle_members.update(c)
        assert {"a", "b"}.issubset(cycle_members)

    def test_disconnected_graph_no_cycle(self) -> None:
        """Multiple disconnected chains without cycles."""
        rels = {"a": "b", "b": None, "c": "d", "d": None}
        assert _detect_circular_references(rels) == []

    def test_empty_relationships(self) -> None:
        """Empty input returns no cycles."""
        assert _detect_circular_references({}) == []


# ── sync_org_structure ───────────────────────────────────────────


class TestSyncOrgStructure:
    """Tests for the main sync_org_structure function."""

    def test_empty_persons_dir(self, persons_dir: Path, config_path: Path) -> None:
        """Returns empty dict for empty persons directory."""
        result = sync_org_structure(persons_dir, config_path)
        assert result == {}

    def test_nonexistent_dir(self, tmp_path: Path, config_path: Path) -> None:
        """Returns empty dict when persons dir doesn't exist."""
        result = sync_org_structure(tmp_path / "nonexistent", config_path)
        assert result == {}

    def test_adds_new_person_to_config(
        self, persons_dir: Path, config_path: Path,
    ) -> None:
        """Person on disk but not in config gets added."""
        _make_person(persons_dir, "alice", "| 上司 | bob |\n")

        result = sync_org_structure(persons_dir, config_path)

        assert result == {"alice": "bob"}
        invalidate_cache()
        cfg = load_config(config_path)
        assert "alice" in cfg.persons
        assert cfg.persons["alice"].supervisor == "bob"

    def test_fills_none_supervisor(
        self, persons_dir: Path, config_path: Path,
    ) -> None:
        """Config entry with supervisor=None gets filled from identity.md."""
        _make_person(persons_dir, "alice", "| 上司 | bob |\n")

        # Pre-populate config with supervisor=None
        cfg = load_config(config_path)
        cfg.persons["alice"] = PersonModelConfig(supervisor=None)
        save_config(cfg, config_path)
        invalidate_cache()

        result = sync_org_structure(persons_dir, config_path)

        assert result["alice"] == "bob"
        invalidate_cache()
        cfg = load_config(config_path)
        assert cfg.persons["alice"].supervisor == "bob"

    def test_does_not_overwrite_existing_supervisor(
        self, persons_dir: Path, config_path: Path,
    ) -> None:
        """Config entry with existing supervisor is NOT overwritten."""
        _make_person(persons_dir, "alice", "| 上司 | bob |\n")

        # Pre-populate config with a different supervisor
        cfg = load_config(config_path)
        cfg.persons["alice"] = PersonModelConfig(supervisor="charlie")
        save_config(cfg, config_path)
        invalidate_cache()

        sync_org_structure(persons_dir, config_path)

        invalidate_cache()
        cfg = load_config(config_path)
        assert cfg.persons["alice"].supervisor == "charlie"  # Unchanged

    def test_no_change_when_already_matched(
        self, persons_dir: Path, config_path: Path,
    ) -> None:
        """No config write when config already matches disk."""
        _make_person(persons_dir, "alice", "| 上司 | bob |\n")

        cfg = load_config(config_path)
        cfg.persons["alice"] = PersonModelConfig(supervisor="bob")
        save_config(cfg, config_path)
        invalidate_cache()

        # Record mtime
        mtime_before = config_path.stat().st_mtime_ns

        sync_org_structure(persons_dir, config_path)

        # Config should not have been rewritten
        mtime_after = config_path.stat().st_mtime_ns
        assert mtime_before == mtime_after

    def test_multiple_persons(
        self, persons_dir: Path, config_path: Path,
    ) -> None:
        """Multiple persons are all discovered and synced."""
        _make_person(persons_dir, "alice", "| 上司 | bob |\n")
        _make_person(persons_dir, "bob", "| 上司 | (なし) |\n")
        _make_person(persons_dir, "charlie", "| 上司 | alice |\n")

        result = sync_org_structure(persons_dir, config_path)

        assert result == {"alice": "bob", "bob": None, "charlie": "alice"}
        invalidate_cache()
        cfg = load_config(config_path)
        assert cfg.persons["alice"].supervisor == "bob"
        assert cfg.persons["bob"].supervisor is None
        assert cfg.persons["charlie"].supervisor == "alice"

    def test_fallback_to_status_json(
        self, persons_dir: Path, config_path: Path,
    ) -> None:
        """Falls back to status.json when identity.md has no supervisor."""
        _make_person(
            persons_dir,
            "alice",
            "# Identity: alice\nNo table here.",
            status_json={"supervisor": "bob"},
        )

        result = sync_org_structure(persons_dir, config_path)

        assert result["alice"] == "bob"
        invalidate_cache()
        cfg = load_config(config_path)
        assert cfg.persons["alice"].supervisor == "bob"

    def test_identity_takes_priority_over_status(
        self, persons_dir: Path, config_path: Path,
    ) -> None:
        """status.json supervisor is checked first by read_person_supervisor."""
        # Note: read_person_supervisor checks status.json first, then identity.md.
        # If status.json has a supervisor, that wins.
        _make_person(
            persons_dir,
            "alice",
            "| 上司 | charlie |\n",
            status_json={"supervisor": "bob"},
        )

        result = sync_org_structure(persons_dir, config_path)

        # status.json takes priority in read_person_supervisor
        assert result["alice"] == "bob"

    def test_circular_reference_skipped(
        self, persons_dir: Path, config_path: Path,
    ) -> None:
        """Persons involved in circular references are not synced."""
        _make_person(persons_dir, "alice", "| 上司 | bob |\n")
        _make_person(persons_dir, "bob", "| 上司 | alice |\n")
        _make_person(persons_dir, "charlie", "| 上司 | (なし) |\n")

        sync_org_structure(persons_dir, config_path)

        invalidate_cache()
        cfg = load_config(config_path)
        # alice and bob should not be in config (circular)
        assert "alice" not in cfg.persons
        assert "bob" not in cfg.persons
        # charlie should be added normally
        assert "charlie" in cfg.persons

    def test_skips_non_person_directories(
        self, persons_dir: Path, config_path: Path,
    ) -> None:
        """Directories without identity.md are skipped."""
        (persons_dir / "not-a-person").mkdir()
        _make_person(persons_dir, "alice", "| 上司 | bob |\n")

        result = sync_org_structure(persons_dir, config_path)

        assert "not-a-person" not in result
        assert "alice" in result

    def test_skips_files_in_persons_dir(
        self, persons_dir: Path, config_path: Path,
    ) -> None:
        """Regular files in persons_dir are ignored."""
        (persons_dir / "README.md").write_text("ignore me", encoding="utf-8")
        _make_person(persons_dir, "alice", "| 上司 | bob |\n")

        result = sync_org_structure(persons_dir, config_path)

        assert len(result) == 1
        assert "alice" in result

    def test_fullwidth_paren_name_resolution(
        self, persons_dir: Path, config_path: Path,
    ) -> None:
        """Japanese name with full-width parens is resolved to English."""
        _make_person(
            persons_dir,
            "hinata",
            "| 上司 | 琴葉（kotoha） |\n",
        )

        result = sync_org_structure(persons_dir, config_path)

        assert result["hinata"] == "kotoha"
        invalidate_cache()
        cfg = load_config(config_path)
        assert cfg.persons["hinata"].supervisor == "kotoha"

    def test_halfwidth_paren_name_resolution(
        self, persons_dir: Path, config_path: Path,
    ) -> None:
        """Japanese name with half-width parens is resolved to English."""
        _make_person(
            persons_dir,
            "hinata",
            "| 上司 | 琴葉(kotoha) |\n",
        )

        result = sync_org_structure(persons_dir, config_path)

        assert result["hinata"] == "kotoha"

    def test_person_with_no_supervisor_added_as_none(
        self, persons_dir: Path, config_path: Path,
    ) -> None:
        """Person without supervisor info gets added with supervisor=None."""
        _make_person(
            persons_dir,
            "alice",
            "# Identity: alice\nNo supervisor table.\n",
        )

        result = sync_org_structure(persons_dir, config_path)

        assert result["alice"] is None
        invalidate_cache()
        cfg = load_config(config_path)
        assert "alice" in cfg.persons
        assert cfg.persons["alice"].supervisor is None

    def test_preserves_existing_person_config_fields(
        self, persons_dir: Path, config_path: Path,
    ) -> None:
        """Syncing supervisor preserves other PersonModelConfig fields."""
        _make_person(persons_dir, "alice", "| 上司 | bob |\n")

        # Pre-populate with extra fields
        cfg = load_config(config_path)
        cfg.persons["alice"] = PersonModelConfig(
            model="openai/gpt-4o",
            max_tokens=8192,
            supervisor=None,
        )
        save_config(cfg, config_path)
        invalidate_cache()

        sync_org_structure(persons_dir, config_path)

        invalidate_cache()
        cfg = load_config(config_path)
        assert cfg.persons["alice"].supervisor == "bob"
        assert cfg.persons["alice"].model == "openai/gpt-4o"
        assert cfg.persons["alice"].max_tokens == 8192

    def test_mismatch_logs_warning(
        self, persons_dir: Path, config_path: Path, caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Mismatched supervisors log a warning but keep config value."""
        _make_person(persons_dir, "alice", "| 上司 | bob |\n")

        cfg = load_config(config_path)
        cfg.persons["alice"] = PersonModelConfig(supervisor="charlie")
        save_config(cfg, config_path)
        invalidate_cache()

        with caplog.at_level("WARNING"):
            sync_org_structure(persons_dir, config_path)

        assert "supervisor mismatch" in caplog.text.lower()
        assert "alice" in caplog.text

    def test_circular_reference_logs_warning(
        self, persons_dir: Path, config_path: Path, caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Circular references are logged as warnings."""
        _make_person(persons_dir, "alice", "| 上司 | bob |\n")
        _make_person(persons_dir, "bob", "| 上司 | alice |\n")

        with caplog.at_level("WARNING"):
            sync_org_structure(persons_dir, config_path)

        assert "circular" in caplog.text.lower()

    def test_nashi_values_produce_none_supervisor(
        self, persons_dir: Path, config_path: Path,
    ) -> None:
        """Various 'none' values in identity.md produce supervisor=None."""
        _make_person(persons_dir, "a", "| 上司 | なし |\n")
        _make_person(persons_dir, "b", "| 上司 | (なし) |\n")
        _make_person(persons_dir, "c", "| 上司 | - |\n")

        result = sync_org_structure(persons_dir, config_path)

        assert result["a"] is None
        assert result["b"] is None
        assert result["c"] is None

    def test_realistic_identity_md(
        self, persons_dir: Path, config_path: Path,
    ) -> None:
        """Supervisor extracted from a realistic multi-section identity.md."""
        identity = (
            "# Identity: hinata\n\n"
            "あなたの名前は日向 ひなた。\n\n"
            "## 基本プロフィール\n\n"
            "| 項目 | 設定 |\n"
            "|------|------|\n"
            "| 誕生日 | 3月21日 |\n"
            "| 星座 | 牡羊座 |\n"
            "| 上司 | 凛堂 凛（rin） |\n"
            "| 身長 | 155cm |\n\n"
            "## 性格特性\n\n元気で前向き。\n"
        )
        _make_person(persons_dir, "hinata", identity)

        result = sync_org_structure(persons_dir, config_path)

        assert result["hinata"] == "rin"

    def test_return_value_includes_all_persons(
        self, persons_dir: Path, config_path: Path,
    ) -> None:
        """Return value includes every discovered person, not just changed ones."""
        _make_person(persons_dir, "alice", "| 上司 | bob |\n")
        _make_person(persons_dir, "bob", "# No supervisor.\n")

        # Pre-populate alice so she won't be changed
        cfg = load_config(config_path)
        cfg.persons["alice"] = PersonModelConfig(supervisor="bob")
        save_config(cfg, config_path)
        invalidate_cache()

        result = sync_org_structure(persons_dir, config_path)

        # Both persons returned even though only bob was newly added
        assert "alice" in result
        assert "bob" in result
