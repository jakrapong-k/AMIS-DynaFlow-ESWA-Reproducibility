from app.models.entities import RunStatus, can_transition


def test_allowed_status_transitions() -> None:
    assert can_transition(RunStatus.QUEUED, RunStatus.RUNNING)
    assert can_transition(RunStatus.RUNNING, RunStatus.SUCCEEDED)


def test_disallowed_status_transitions() -> None:
    assert not can_transition(RunStatus.SUCCEEDED, RunStatus.RUNNING)
    assert not can_transition(RunStatus.CANCELLED, RunStatus.QUEUED)
