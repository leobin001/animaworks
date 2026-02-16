"""Tests for 3D asset optimization: armature download, mesh stripping, GLB compression."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch, call

import pytest


# ── download_rigging_animations ──────────────────────────────────


class TestDownloadRiggingAnimations:
    """Tests for MeshyClient.download_rigging_animations armature preference."""

    def _make_client(self):
        with patch("core.tools.image_gen.get_credential", return_value="test-key"):
            from core.tools.image_gen import MeshyClient
            return MeshyClient()

    def test_prefers_armature_glb_url(self):
        """Should prefer armature-only URL over full model URL."""
        client = self._make_client()
        task = {
            "result": {
                "basic_animations": {
                    "walking_glb_url": "https://example.com/walking_full.glb",
                    "walking_armature_glb_url": "https://example.com/walking_armature.glb",
                    "running_glb_url": "https://example.com/running_full.glb",
                    "running_armature_glb_url": "https://example.com/running_armature.glb",
                }
            }
        }
        with patch("httpx.get") as mock_get:
            mock_resp = MagicMock()
            mock_resp.content = b"armature-data"
            mock_get.return_value = mock_resp

            result = client.download_rigging_animations(task)

            # Verify armature URLs were used
            urls_called = [c.args[0] for c in mock_get.call_args_list]
            assert "https://example.com/walking_armature.glb" in urls_called
            assert "https://example.com/running_armature.glb" in urls_called
            assert "https://example.com/walking_full.glb" not in urls_called

    def test_falls_back_to_full_glb(self):
        """Should fall back to full GLB URL when armature URL is missing."""
        client = self._make_client()
        task = {
            "result": {
                "basic_animations": {
                    "walking_glb_url": "https://example.com/walking_full.glb",
                    # No armature URLs
                    "running_glb_url": "https://example.com/running_full.glb",
                }
            }
        }
        with patch("httpx.get") as mock_get:
            mock_resp = MagicMock()
            mock_resp.content = b"full-data"
            mock_get.return_value = mock_resp

            result = client.download_rigging_animations(task)

            urls_called = [c.args[0] for c in mock_get.call_args_list]
            assert "https://example.com/walking_full.glb" in urls_called
            assert "https://example.com/running_full.glb" in urls_called

    def test_empty_basic_animations(self):
        """Should handle empty basic_animations gracefully."""
        client = self._make_client()
        task = {"result": {"basic_animations": {}}}
        result = client.download_rigging_animations(task)
        assert result == {}


# ── strip_mesh_from_glb ──────────────────────────────────────────


class TestStripMeshFromGlb:
    """Tests for strip_mesh_from_glb helper."""

    def test_returns_false_when_node_not_found(self):
        """Should return False and log warning when node is not installed."""
        from core.tools.image_gen import strip_mesh_from_glb

        with patch("shutil.which", return_value=None):
            result = strip_mesh_from_glb(Path("/tmp/test.glb"))
            assert result is False

    def test_returns_false_on_subprocess_error(self):
        """Should return False when subprocess fails."""
        import subprocess
        from core.tools.image_gen import strip_mesh_from_glb

        with patch("shutil.which", return_value="/usr/bin/node"):
            with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "node")):
                result = strip_mesh_from_glb(Path("/tmp/test.glb"))
                assert result is False

    def test_returns_false_on_timeout(self):
        """Should return False when subprocess times out."""
        import subprocess
        from core.tools.image_gen import strip_mesh_from_glb

        with patch("shutil.which", return_value="/usr/bin/node"):
            with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("node", 120)):
                result = strip_mesh_from_glb(Path("/tmp/test.glb"))
                assert result is False


# ── optimize_glb ─────────────────────────────────────────────────


class TestOptimizeGlb:
    """Tests for optimize_glb helper."""

    def test_returns_false_when_npx_not_found(self):
        """Should return False when npx is not installed."""
        from core.tools.image_gen import optimize_glb

        with patch("shutil.which", return_value=None):
            result = optimize_glb(Path("/tmp/test.glb"))
            assert result is False

    def test_calls_optimize_then_draco(self):
        """Should call gltf-transform optimize then draco."""
        from core.tools.image_gen import _run_gltf_transform

        with patch("shutil.which", return_value="/usr/bin/npx"):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=0)
                result = _run_gltf_transform(["optimize", "in.glb", "out.glb"], Path("in.glb"))
                assert result is True
                cmd = mock_run.call_args.args[0]
                assert "@gltf-transform/cli" in cmd
                assert "optimize" in cmd

    def test_returns_false_on_subprocess_error(self):
        """Should return False when gltf-transform fails."""
        import subprocess
        from core.tools.image_gen import _run_gltf_transform

        with patch("shutil.which", return_value="/usr/bin/npx"):
            with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "npx", stderr=b"error")):
                result = _run_gltf_transform(["optimize", "in.glb", "out.glb"], Path("in.glb"))
                assert result is False
