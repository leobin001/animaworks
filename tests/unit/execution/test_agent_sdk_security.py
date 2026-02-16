"""Tests for A1 mode security functions in core.execution.agent_sdk."""
from __future__ import annotations

from pathlib import Path

import pytest

from core.execution.agent_sdk import (
    _PROTECTED_FILES,
    _WRITE_COMMANDS,
    _check_a1_bash_command,
    _check_a1_file_access,
)


# ── Fixtures ──────────────────────────────────────────────────


@pytest.fixture
def persons_dir(tmp_path: Path) -> Path:
    d = tmp_path / "persons"
    d.mkdir()
    return d


@pytest.fixture
def person_dir(persons_dir: Path) -> Path:
    d = persons_dir / "test-person"
    d.mkdir()
    (d / "permissions.md").write_text("", encoding="utf-8")
    (d / "identity.md").write_text("", encoding="utf-8")
    (d / "bootstrap.md").write_text("", encoding="utf-8")
    (d / "knowledge").mkdir()
    return d


@pytest.fixture
def other_person_dir(persons_dir: Path) -> Path:
    d = persons_dir / "other-person"
    d.mkdir()
    (d / "identity.md").write_text("secret", encoding="utf-8")
    (d / "episodes").mkdir()
    return d


# ── Constants ──────────────────────────────────────────────────


class TestConstants:
    def test_protected_files_contains_expected(self):
        assert "permissions.md" in _PROTECTED_FILES
        assert "identity.md" in _PROTECTED_FILES
        assert "bootstrap.md" in _PROTECTED_FILES

    def test_protected_files_is_frozenset(self):
        assert isinstance(_PROTECTED_FILES, frozenset)

    def test_write_commands_contains_expected(self):
        assert "cp" in _WRITE_COMMANDS
        assert "mv" in _WRITE_COMMANDS
        assert "rsync" in _WRITE_COMMANDS


# ── _check_a1_file_access ────────────────────────────────────


class TestCheckA1FileAccess:
    def test_empty_path_allowed(self, person_dir: Path):
        assert _check_a1_file_access("", person_dir, write=True) is None

    def test_write_to_own_permissions_blocked(self, person_dir: Path):
        path = str(person_dir / "permissions.md")
        result = _check_a1_file_access(path, person_dir, write=True)
        assert result is not None
        assert "protected file" in result

    def test_write_to_own_identity_blocked(self, person_dir: Path):
        path = str(person_dir / "identity.md")
        result = _check_a1_file_access(path, person_dir, write=True)
        assert result is not None
        assert "protected file" in result

    def test_write_to_own_bootstrap_blocked(self, person_dir: Path):
        path = str(person_dir / "bootstrap.md")
        result = _check_a1_file_access(path, person_dir, write=True)
        assert result is not None
        assert "protected file" in result

    def test_read_own_permissions_allowed(self, person_dir: Path):
        """Reading protected files should be allowed."""
        path = str(person_dir / "permissions.md")
        result = _check_a1_file_access(path, person_dir, write=False)
        assert result is None

    def test_write_to_own_knowledge_allowed(self, person_dir: Path):
        path = str(person_dir / "knowledge" / "note.md")
        result = _check_a1_file_access(path, person_dir, write=True)
        assert result is None

    def test_read_other_person_blocked(
        self, person_dir: Path, other_person_dir: Path,
    ):
        path = str(other_person_dir / "identity.md")
        result = _check_a1_file_access(path, person_dir, write=False)
        assert result is not None
        assert "other person" in result.lower()

    def test_write_other_person_blocked(
        self, person_dir: Path, other_person_dir: Path,
    ):
        path = str(other_person_dir / "episodes" / "log.md")
        result = _check_a1_file_access(path, person_dir, write=True)
        assert result is not None
        assert "other person" in result.lower()

    def test_path_outside_persons_root_allowed(self, person_dir: Path):
        """Paths outside the persons/ root are not restricted by this function."""
        result = _check_a1_file_access("/tmp/some_file.txt", person_dir, write=True)
        assert result is None

    def test_write_to_own_heartbeat_allowed(self, person_dir: Path):
        """heartbeat.md is not protected."""
        path = str(person_dir / "heartbeat.md")
        result = _check_a1_file_access(path, person_dir, write=True)
        assert result is None

    def test_write_to_own_cron_allowed(self, person_dir: Path):
        """cron.md is not protected."""
        path = str(person_dir / "cron.md")
        result = _check_a1_file_access(path, person_dir, write=True)
        assert result is None


# ── _check_a1_bash_command ───────────────────────────────────


class TestCheckA1BashCommand:
    def test_cp_to_other_person_blocked(
        self, person_dir: Path, other_person_dir: Path,
    ):
        cmd = f"cp {other_person_dir}/identity.md ./stolen.md"
        result = _check_a1_bash_command(cmd, person_dir)
        assert result is not None
        assert "other person" in result.lower()

    def test_mv_to_other_person_blocked(
        self, person_dir: Path, other_person_dir: Path,
    ):
        cmd = f"mv ./file.md {other_person_dir}/file.md"
        result = _check_a1_bash_command(cmd, person_dir)
        assert result is not None
        assert "other person" in result.lower()

    def test_normal_ls_allowed(self, person_dir: Path):
        result = _check_a1_bash_command("ls -la", person_dir)
        assert result is None

    def test_normal_python_allowed(self, person_dir: Path):
        result = _check_a1_bash_command("python3 script.py", person_dir)
        assert result is None

    def test_cp_within_own_dir_allowed(self, person_dir: Path):
        cmd = f"cp {person_dir}/file1.md {person_dir}/file2.md"
        result = _check_a1_bash_command(cmd, person_dir)
        assert result is None

    def test_non_write_command_to_other_person_allowed(
        self, person_dir: Path, other_person_dir: Path,
    ):
        """Non-write commands like 'cat' are not checked."""
        cmd = f"cat {other_person_dir}/identity.md"
        result = _check_a1_bash_command(cmd, person_dir)
        assert result is None

    def test_empty_command_allowed(self, person_dir: Path):
        result = _check_a1_bash_command("", person_dir)
        assert result is None

    def test_malformed_command_allowed(self, person_dir: Path):
        """Malformed commands that can't be parsed should not crash."""
        result = _check_a1_bash_command("echo 'unclosed", person_dir)
        assert result is None

    def test_rsync_to_other_person_blocked(
        self, person_dir: Path, other_person_dir: Path,
    ):
        cmd = f"rsync -a ./data/ {other_person_dir}/data/"
        result = _check_a1_bash_command(cmd, person_dir)
        assert result is not None

    def test_flags_are_skipped(self, person_dir: Path):
        """Arguments starting with - should be skipped."""
        result = _check_a1_bash_command("cp -r --verbose file1 file2", person_dir)
        assert result is None
