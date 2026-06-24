# Testing anti-patterns

Read this when writing or changing tests, adding a mock, or tempted to add a
method to production code that only the tests will call.

**Core principle:** test what the code does, not what the mocks do. A mock is a
means to isolate a unit, never the thing under test. If you find yourself
asserting on a mock, the test has drifted off the behaviour.

Strict test-first development prevents most of these on its own: writing the
test against real code and watching it fail forces you to confront what you are
actually testing before any mock exists.

## Contents

1. [Testing mock behaviour](#1-testing-mock-behaviour)
2. [Test-only methods in production code](#2-test-only-methods-in-production-code)
3. [Mocking without understanding the dependency](#3-mocking-without-understanding-the-dependency)
4. [Incomplete mocks](#4-incomplete-mocks)
5. [Tests as an afterthought](#5-tests-as-an-afterthought)
6. [When mocks get too complex](#when-mocks-get-too-complex)

## 1. Testing mock behaviour

The failure mode: the assertion checks that the mock is present or was called,
not that the real behaviour happened.

```python
# Asserts the mock was installed, not that anything works.
def test_sends_welcome_email(monkeypatch):
    sent = []
    monkeypatch.setattr(mailer, "send", lambda msg: sent.append(msg))

    register_user("alice@example.com")

    assert mailer.send.called  # passes because we mocked it, proves nothing
```

The test passes whenever the mock is wired up and tells you nothing about
whether registration actually produces a welcome email. The useful question to
ask: *am I testing real behaviour, or just that a mock exists?*

The fix is either to not mock the collaborator and assert on the real outcome,
or, if the collaborator must be isolated, to assert on the *effect the unit
under test produces* rather than on the mock:

```python
# Asserts the observable effect: a correctly-addressed message was produced.
def test_sends_welcome_email(monkeypatch):
    sent = []
    monkeypatch.setattr(mailer, "send", lambda msg: sent.append(msg))

    register_user("alice@example.com")

    assert sent == [WelcomeEmail(to="alice@example.com")]
```

## 2. Test-only methods in production code

The failure mode: a method exists on a production class solely so tests can call
it — a `reset()`, a `_clear_cache()`, a `destroy()` used only in teardown.

```python
# Session.destroy() is only ever called from afterEach-style teardown.
class Session:
    def destroy(self) -> None:
        if self._workspace is not None:
            self._workspace_manager.destroy(self._workspace.id)
```

This pollutes the production API, risks being called for real, and confuses the
object's lifecycle with the entity's. Before adding a method to a production
class, ask: *is this only used by tests?* If so, it belongs in a test utility,
not in the class:

```python
# In tests/utils.py
def cleanup_session(session: Session) -> None:
    workspace = session.workspace_info
    if workspace is not None:
        workspace_manager.destroy(workspace.id)
```

Also ask: *does this class own this resource's lifecycle?* If not, the method is
on the wrong class regardless of who calls it.

## 3. Mocking without understanding the dependency

The failure mode: mocking a method that had a side effect the test relied on, so
the test passes (or fails) for the wrong reason.

```python
# The mock suppresses the config write that the duplicate check depends on.
def test_detects_duplicate_server(monkeypatch):
    monkeypatch.setattr(ToolCatalog, "discover_and_cache", lambda self: None)

    add_server(config)
    add_server(config)  # should raise DuplicateServer — but now it won't
```

Over-mocking "to be safe" removes behaviour the test needs. Before mocking a
method, work through:

1. What side effects does the real method have?
2. Does this test depend on any of them?
3. Do I actually understand what the test needs to happen?

If the test depends on a side effect, mock at a *lower* level — the genuinely
slow or external operation — not the high-level method the test relies on. If
you are unsure what the test depends on, run it against the real implementation
first and observe, then add the minimal mock at the right level.

Warning signs: "I'll mock this to be safe", "this might be slow, better mock
it", mocking without tracing the dependency chain.

## 4. Incomplete mocks

The failure mode: the mock includes only the fields you happened to think of, so
it diverges from the real structure and the test gives false confidence.

```python
# Real API also returns `metadata`; downstream code reads response["metadata"]["request_id"].
mock_response = {
    "status": "success",
    "data": {"user_id": "123", "name": "Alice"},
}
```

The test passes, but integration fails the moment code reaches a field the mock
omitted. Mirror the **complete** structure as it exists in reality, not just the
fields your immediate assertion touches:

```python
mock_response = {
    "status": "success",
    "data": {"user_id": "123", "name": "Alice"},
    "metadata": {"request_id": "req-789", "timestamp": 1234567890},
}
```

If you are constructing a mock, you are taking responsibility for the whole
shape. When uncertain, include every documented field.

## 5. Tests as an afterthought

The failure mode: "implementation complete, ready for testing." Testing is part
of implementation, not a follow-up. Test-first would have caught this — you
cannot claim a unit is complete without the tests that prove it, and those tests
should have come first.

## When mocks get too complex

If the mock setup is longer than the test logic, if you are mocking nearly
everything to make a test pass, or if the test breaks whenever the mock changes,
that is a signal — not to write a more elaborate mock, but to step back. Often an
integration test against the real collaborators is simpler and more honest than
a tower of mocks. The question worth asking out loud: *do we need a mock here at
all?*

## Quick reference

| Anti-pattern | Fix |
|--------------|-----|
| Asserting on a mock | Test the real component, or assert on the effect the unit produces |
| Test-only method in production | Move it to a test utility |
| Mocking without understanding | Trace the dependencies first; mock minimally, at the right level |
| Incomplete mock | Mirror the real structure completely |
| Tests as afterthought | Tests first — that is the whole point |
| Over-complex mocks | Prefer an integration test with real collaborators |

## The bottom line

Mocks isolate; they are not what you test. If watching a test fail reveals you
are exercising mock behaviour, the test is wrong — test the real behaviour, or
question why you are mocking at all.

---

_Adapted from [superpowers](https://github.com/obra/superpowers) by Jesse Vincent (MIT License, © 2025), merged with project standards._
