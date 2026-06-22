"""End-to-end integration tests for the organizational learning layer.

Exercises the full flow: history -> patterns -> insights -> recommendations ->
maturity -> reports, using the built-in example datasets.
"""

from workflow_os.learning import (
    continuous_improvement_report,
    learning_report,
    organizational_dashboard,
    organizational_maturity_score,
    struggling_organization,
    successful_organization,
)


def _maturity(example):
    return organizational_maturity_score(
        example.records,
        sops=example.sops,
        exceptions=example.exceptions,
        approvals=example.approvals,
        recoveries=example.recoveries,
    )


def test_successful_organization_is_healthy():
    example = successful_organization()
    maturity = _maturity(example)
    assert maturity.overall >= 0.8
    assert maturity.level in {"managed", "optimizing"}

    report = learning_report(
        example.records,
        sops=example.sops,
        exceptions=example.exceptions,
        approvals=example.approvals,
        recoveries=example.recoveries,
    )
    assert any(i.category == "success" for i in report.insights)


def test_struggling_organization_yields_recommendations():
    example = struggling_organization()
    report = learning_report(
        example.records,
        sops=example.sops,
        exceptions=example.exceptions,
        approvals=example.approvals,
        recoveries=example.recoveries,
    )
    categories = {r.category for r in report.recommendations}
    assert "workflow" in categories
    assert any(i.category == "failure" for i in report.insights)
    assert _maturity(example).overall < 0.6


def test_continuous_improvement_and_dashboard_align():
    example = struggling_organization()
    cir = continuous_improvement_report(
        example.records,
        sops=example.sops,
        exceptions=example.exceptions,
        approvals=example.approvals,
        recoveries=example.recoveries,
    )
    dashboard = organizational_dashboard(
        example.records,
        sops=example.sops,
        exceptions=example.exceptions,
        approvals=example.approvals,
        recoveries=example.recoveries,
    )
    assert dashboard["totals"]["recommendations"] == len(cir.opportunities)
    assert cir.maturity is not None
    assert dashboard["maturity"]["level"] == cir.maturity.level
