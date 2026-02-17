"""E2E tests for shared channel messaging (channels + DM logs)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from core.messenger import Messenger


@pytest.fixture
def shared_dir(tmp_path: Path) -> Path:
    d = tmp_path / "shared"
    d.mkdir()
    (d / "inbox").mkdir()
    (d / "channels").mkdir()
    (d / "dm_logs").mkdir()
    return d


class TestE2EDMFlow:
    """Full DM flow: send → inbox + dm_logs."""

    def test_send_creates_both_inbox_and_dm_log(self, shared_dir):
        alice = Messenger(shared_dir, "alice")
        alice.send("bob", "Hello Bob!")

        # Inbox file exists
        bob_inbox = shared_dir / "inbox" / "bob"
        assert len(list(bob_inbox.glob("*.json"))) == 1

        # DM log exists
        dm_log = shared_dir / "dm_logs" / "alice-bob.jsonl"
        assert dm_log.exists()
        entry = json.loads(dm_log.read_text(encoding="utf-8").strip())
        assert entry["from"] == "alice"
        assert entry["text"] == "Hello Bob!"

    def test_bidirectional_dm_conversation(self, shared_dir):
        alice = Messenger(shared_dir, "alice")
        bob = Messenger(shared_dir, "bob")

        alice.send("bob", "Hi Bob, how are you?")
        bob.send("alice", "I'm fine, thanks Alice!")
        alice.send("bob", "Great to hear!")

        # Both should share the same DM log
        dm_log = shared_dir / "dm_logs" / "alice-bob.jsonl"
        lines = dm_log.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 3

        # Read via API
        alice_history = alice.read_dm_history("bob")
        bob_history = bob.read_dm_history("alice")
        assert len(alice_history) == 3
        assert len(bob_history) == 3

        # Content matches
        assert alice_history[0]["from"] == "alice"
        assert alice_history[1]["from"] == "bob"
        assert alice_history[2]["from"] == "alice"

    def test_receive_and_archive_preserves_dm_log(self, shared_dir):
        alice = Messenger(shared_dir, "alice")
        bob = Messenger(shared_dir, "bob")

        alice.send("bob", "Important message")
        bob.receive_and_archive()

        # Inbox is archived
        assert not bob.has_unread()

        # But DM log persists
        history = bob.read_dm_history("alice")
        assert len(history) >= 1
        assert any("Important message" in h["text"] for h in history)


class TestE2EChannelFlow:
    """Channel posting and reading."""

    def test_multiple_animas_post_and_read(self, shared_dir):
        alice = Messenger(shared_dir, "alice")
        bob = Messenger(shared_dir, "bob")
        charlie = Messenger(shared_dir, "charlie")

        alice.post_channel("general", "Hello from Alice")
        bob.post_channel("general", "Hello from Bob")
        charlie.post_channel("general", "Hello from Charlie")

        # All can read
        for m in (alice, bob, charlie):
            msgs = m.read_channel("general")
            assert len(msgs) == 3

    def test_channel_post_and_mention(self, shared_dir):
        alice = Messenger(shared_dir, "alice")
        bob = Messenger(shared_dir, "bob")

        alice.post_channel("ops", "@bob Server is down!")
        bob.post_channel("ops", "On it!")

        # Bob can find his mentions
        mentions = bob.read_channel_mentions("ops")
        assert len(mentions) == 1
        assert "@bob" in mentions[0]["text"]

    def test_ops_channel_isolation(self, shared_dir):
        alice = Messenger(shared_dir, "alice")
        alice.post_channel("general", "General msg")
        alice.post_channel("ops", "Ops msg")

        gen = alice.read_channel("general")
        ops = alice.read_channel("ops")
        assert len(gen) == 1
        assert len(ops) == 1
        assert gen[0]["text"] == "General msg"
        assert ops[0]["text"] == "Ops msg"


class TestE2EAtAllMirroring:
    """@all mirroring from receive_external to general channel."""

    def test_human_at_all_appears_in_general(self, shared_dir):
        sakura = Messenger(shared_dir, "sakura")

        sakura.receive_external(
            "@all The server error is now resolved.",
            source="human",
            external_user_id="taka",
        )

        # Message should be in sakura's inbox
        messages = sakura.receive()
        assert len(messages) == 1

        # AND in the general channel
        channel_msgs = sakura.read_channel("general")
        assert len(channel_msgs) == 1
        assert channel_msgs[0]["source"] == "human"
        assert "@all" in channel_msgs[0]["text"]

    def test_all_animas_can_see_mirrored_message(self, shared_dir):
        sakura = Messenger(shared_dir, "sakura")
        yuki = Messenger(shared_dir, "yuki")
        mio = Messenger(shared_dir, "mio")

        sakura.receive_external(
            "@all Error is resolved",
            source="human",
            external_user_id="taka",
        )

        # All animas should see it in the general channel
        for m in (sakura, yuki, mio):
            msgs = m.read_channel("general")
            assert len(msgs) == 1
            assert "Error is resolved" in msgs[0]["text"]

    def test_no_mirroring_without_at_all(self, shared_dir):
        sakura = Messenger(shared_dir, "sakura")
        sakura.receive_external(
            "Just a normal message",
            source="human",
            external_user_id="taka",
        )
        msgs = sakura.read_channel("general")
        assert len(msgs) == 0


class TestE2ENoMessageLog:
    """Verify old message_log is not used anymore."""

    def test_send_no_message_log(self, shared_dir):
        alice = Messenger(shared_dir, "alice")
        alice.send("bob", "test")
        assert not (shared_dir / "message_log").exists()

    def test_receive_external_no_message_log(self, shared_dir):
        alice = Messenger(shared_dir, "alice")
        alice.receive_external("test", source="human")
        assert not (shared_dir / "message_log").exists()
