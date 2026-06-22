"""SOP author metadata.

Beyond the primary ``author`` field, a SOP tracks reviewers, owners, and
contributors in its metadata. These helpers read and update that information
without disturbing other metadata keys.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from workflow_os.sop.record import SOPRecord

REVIEWERS_KEY = "reviewers"
OWNERS_KEY = "owners"
CONTRIBUTORS_KEY = "contributors"


@dataclass
class SOPAuthorship:
    """A view of who is responsible for a SOP."""

    author: str | None = None
    reviewers: list[str] = field(default_factory=list)
    owners: list[str] = field(default_factory=list)
    contributors: list[str] = field(default_factory=list)


def _people(record: SOPRecord, key: str) -> list[str]:
    value = record.metadata.get(key, [])
    if isinstance(value, list):
        return [str(person) for person in value]
    return []


def get_authorship(record: SOPRecord) -> SOPAuthorship:
    """Return the authorship view of a SOP record."""
    return SOPAuthorship(
        author=record.author,
        reviewers=_people(record, REVIEWERS_KEY),
        owners=_people(record, OWNERS_KEY),
        contributors=_people(record, CONTRIBUTORS_KEY),
    )


def _set_people(record: SOPRecord, key: str, people: list[str]) -> None:
    deduped: list[str] = []
    for person in people:
        if person not in deduped:
            deduped.append(person)
    record.metadata[key] = deduped


def set_reviewers(record: SOPRecord, reviewers: list[str]) -> None:
    """Replace the reviewers of a SOP."""
    _set_people(record, REVIEWERS_KEY, reviewers)


def set_owners(record: SOPRecord, owners: list[str]) -> None:
    """Replace the owners of a SOP."""
    _set_people(record, OWNERS_KEY, owners)


def set_contributors(record: SOPRecord, contributors: list[str]) -> None:
    """Replace the contributors of a SOP."""
    _set_people(record, CONTRIBUTORS_KEY, contributors)


def _add_person(record: SOPRecord, key: str, person: str) -> None:
    people = _people(record, key)
    if person not in people:
        people.append(person)
    record.metadata[key] = people


def add_reviewer(record: SOPRecord, reviewer: str) -> None:
    """Add a reviewer to a SOP if not already present."""
    _add_person(record, REVIEWERS_KEY, reviewer)


def add_owner(record: SOPRecord, owner: str) -> None:
    """Add an owner to a SOP if not already present."""
    _add_person(record, OWNERS_KEY, owner)


def add_contributor(record: SOPRecord, contributor: str) -> None:
    """Add a contributor to a SOP if not already present."""
    _add_person(record, CONTRIBUTORS_KEY, contributor)
