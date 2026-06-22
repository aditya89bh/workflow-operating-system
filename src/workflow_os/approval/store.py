"""Approval store abstraction.

:class:`ApprovalStore` is a structural protocol describing how approval requests
are stored and retrieved. :class:`ApprovalQuery` expresses the filters a store
must support, and :func:`apply_query` provides reusable in-memory filtering so
implementations share identical query semantics. :class:`InMemoryApprovalStore`
is a simple dictionary-backed implementation used in tests and demos.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, runtime_checkable

from workflow_os.approval.record import ApprovalRequest

ApprovalList = list[ApprovalRequest]


class ApprovalNotFoundError(KeyError):
    """Raised when an approval id cannot be found in an approval store."""


@dataclass
class ApprovalQuery:
    """A filter over approval requests.

    All fields are optional; an empty query matches every record. Results are
    ordered by ``created_at`` (ascending by default).
    """

    workflow_id: str | None = None
    step_id: str | None = None
    requester: str | None = None
    approver: str | None = None
    states: tuple[str, ...] | None = None
    since: datetime | None = None
    until: datetime | None = None
    limit: int | None = None
    order: str = "asc"


@runtime_checkable
class ApprovalStore(Protocol):
    """Storage interface for approval requests."""

    def add(self, request: ApprovalRequest) -> None:
        """Persist a single approval request."""
        ...

    def get(self, approval_id: str) -> ApprovalRequest:
        """Return the request with ``approval_id`` or raise if missing."""
        ...

    def update(self, request: ApprovalRequest) -> None:
        """Persist changes to an existing request or raise if missing."""
        ...

    def delete(self, approval_id: str) -> None:
        """Remove the request with ``approval_id`` or raise if missing."""
        ...

    def list(self) -> ApprovalList:
        """Return all stored requests ordered by ``created_at``."""
        ...

    def query(self, query: ApprovalQuery) -> ApprovalList:
        """Return requests matching ``query`` ordered by ``created_at``."""
        ...


def matches(request: ApprovalRequest, query: ApprovalQuery) -> bool:
    """Return ``True`` if ``request`` satisfies every filter in ``query``."""
    if query.workflow_id is not None and request.workflow_id != query.workflow_id:
        return False
    if query.step_id is not None and request.step_id != query.step_id:
        return False
    if query.requester is not None and request.requester != query.requester:
        return False
    if query.approver is not None and query.approver not in request.approvers:
        return False
    if query.states is not None and request.state not in {
        str(state) for state in query.states
    }:
        return False
    if query.since is not None and request.created_at < query.since:
        return False
    if query.until is not None and request.created_at > query.until:
        return False
    return True


def apply_query(
    requests: Iterable[ApprovalRequest], query: ApprovalQuery
) -> list[ApprovalRequest]:
    """Filter, order, and limit ``requests`` according to ``query``."""
    result = [request for request in requests if matches(request, query)]
    result.sort(key=lambda request: request.created_at, reverse=query.order == "desc")
    if query.limit is not None:
        result = result[: query.limit]
    return result


class InMemoryApprovalStore:
    """A dictionary-backed :class:`ApprovalStore` implementation."""

    def __init__(self) -> None:
        self._requests: dict[str, ApprovalRequest] = {}

    def add(self, request: ApprovalRequest) -> None:
        self._requests[request.approval_id] = request

    def get(self, approval_id: str) -> ApprovalRequest:
        try:
            return self._requests[approval_id]
        except KeyError as exc:
            raise ApprovalNotFoundError(approval_id) from exc

    def update(self, request: ApprovalRequest) -> None:
        if request.approval_id not in self._requests:
            raise ApprovalNotFoundError(request.approval_id)
        self._requests[request.approval_id] = request

    def delete(self, approval_id: str) -> None:
        if approval_id not in self._requests:
            raise ApprovalNotFoundError(approval_id)
        del self._requests[approval_id]

    def list(self) -> ApprovalList:
        return apply_query(self._requests.values(), ApprovalQuery())

    def query(self, query: ApprovalQuery) -> ApprovalList:
        return apply_query(self._requests.values(), query)
