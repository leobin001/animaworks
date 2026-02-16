from __future__ import annotations
# AnimaWorks - Digital Person Framework
# Copyright (C) 2026 AnimaWorks Authors
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# This file is part of AnimaWorks core/server, licensed under AGPL-3.0.
# See LICENSES/AGPL-3.0.txt for the full license text.

"""Periodic organizational structure synchronization.

Scans person directories, extracts supervisor relationships from identity.md
tables and status.json, and reconciles them with config.json entries.
Manual config overrides are never clobbered; mismatches are logged as warnings.
"""

import logging
from pathlib import Path

from core.config.models import (
    PersonModelConfig,
    load_config,
    read_person_supervisor,
    save_config,
)

logger = logging.getLogger(__name__)


# ── Circular reference detection ─────────────────────────────────


def _detect_circular_references(
    relationships: dict[str, str | None],
) -> list[tuple[str, ...]]:
    """Detect circular supervisor references.

    Args:
        relationships: Mapping of person name to supervisor name.

    Returns:
        List of cycles found, each represented as a tuple of names.
    """
    cycles: list[tuple[str, ...]] = []
    visited: set[str] = set()

    for start in relationships:
        if start in visited:
            continue

        path: list[str] = []
        path_set: set[str] = set()
        current: str | None = start

        while current is not None and current not in visited:
            if current in path_set:
                # Found a cycle — extract the cycle portion
                cycle_start = path.index(current)
                cycle = tuple(path[cycle_start:])
                cycles.append(cycle)
                break
            path.append(current)
            path_set.add(current)
            current = relationships.get(current)

        visited.update(path_set)

    return cycles


# ── Main sync function ───────────────────────────────────────────


def sync_org_structure(
    persons_dir: Path,
    config_path: Path | None = None,
) -> dict[str, str | None]:
    """Sync organizational structure from person files to config.json.

    For each person directory:

    1. Extract supervisor from identity.md / status.json via
       :func:`~core.config.models.read_person_supervisor`.
    2. If config.json has no entry for this person, create one.
    3. If config.json has ``supervisor=None`` but a value was found, update it.
    4. If config.json already has a supervisor set, don't overwrite
       (respect manual config).
    5. Log warnings for mismatches.

    Args:
        persons_dir: Path to the persons directory
            (e.g. ``~/.animaworks/persons``).
        config_path: Optional explicit path to config.json.  When ``None``,
            the default location is resolved automatically.

    Returns:
        Dict of ``{person_name: supervisor_value}`` for all discovered entries.
    """
    if not persons_dir.is_dir():
        logger.debug("Persons directory does not exist: %s", persons_dir)
        return {}

    # ── Phase 1: discover supervisor relationships from disk ──────

    discovered: dict[str, str | None] = {}

    for person_dir in sorted(persons_dir.iterdir()):
        if not person_dir.is_dir():
            continue
        if not (person_dir / "identity.md").exists():
            continue

        name = person_dir.name
        discovered[name] = read_person_supervisor(person_dir)

    if not discovered:
        logger.debug("No persons discovered in %s", persons_dir)
        return {}

    logger.info("Org sync: discovered %d persons from disk", len(discovered))

    # ── Phase 2: detect circular references ──────────────────────

    cycles = _detect_circular_references(discovered)
    circular_persons: set[str] = set()
    for cycle in cycles:
        circular_persons.update(cycle)
        logger.warning(
            "Org sync: circular supervisor reference detected: %s",
            " -> ".join(cycle) + " -> " + cycle[0],
        )

    # ── Phase 3: reconcile with config.json ──────────────────────

    config = load_config(config_path)
    changed = False

    for name, disk_supervisor in discovered.items():
        # Skip persons involved in circular references
        if name in circular_persons:
            logger.warning(
                "Org sync: skipping %s due to circular reference", name,
            )
            continue

        if name not in config.persons:
            # Person not yet in config — add with discovered supervisor
            config.persons[name] = PersonModelConfig(supervisor=disk_supervisor)
            changed = True
            logger.info(
                "Org sync: added person '%s' with supervisor=%s",
                name,
                disk_supervisor,
            )
            continue

        existing = config.persons[name]

        if existing.supervisor is None and disk_supervisor is not None:
            # Config has no supervisor but disk has one — fill it in
            existing.supervisor = disk_supervisor
            changed = True
            logger.info(
                "Org sync: set supervisor for '%s' to '%s' (was None)",
                name,
                disk_supervisor,
            )
        elif (
            existing.supervisor is not None
            and disk_supervisor is not None
            and existing.supervisor != disk_supervisor
        ):
            # Config already has a different supervisor — warn but don't overwrite
            logger.warning(
                "Org sync: supervisor mismatch for '%s': "
                "config='%s', identity.md='%s' (keeping config value)",
                name,
                existing.supervisor,
                disk_supervisor,
            )

    # ── Phase 4: persist if anything changed ─────────────────────

    if changed:
        save_config(config, config_path)
        logger.info("Org sync: config.json updated")
    else:
        logger.debug("Org sync: no changes needed")

    return discovered
