from unittest.mock import create_autospec

import pytest
from sqlalchemy.orm import Session

from app.core.errors import TodoNotFoundError, TodoValidationError
from app.models.todo import Todo
from app.repositories.todo_repository import TodoRepository
from app.schemas.todo import TodoCreateRequest, TodoUpdateRequest
from app.services.todo_service import TodoService


def test_create_todo_trims_title_and_commits(db_session: Session) -> None:
    service = TodoService(db_session)

    created = service.create_todo(TodoCreateRequest(title="  Keep clean  "))

    assert created.title == "Keep clean"


@pytest.mark.parametrize("invalid_title", ["", "   "])
def test_create_todo_rejects_empty_title_when_payload_is_bypassed(
    db_session: Session,
    invalid_title: str,
) -> None:
    service = TodoService(db_session)
    payload = TodoCreateRequest.model_construct(title=invalid_title)

    with pytest.raises(TodoValidationError) as error:
        service.create_todo(payload)

    assert error.value.code == "TODO_VALIDATION_ERROR"


def test_update_todo_raises_not_found_for_unknown_id(db_session: Session) -> None:
    service = TodoService(db_session)

    with pytest.raises(TodoNotFoundError) as error:
        service.update_todo(todo_id=99999, payload=TodoUpdateRequest(title="Update"))

    assert error.value.code == "TODO_NOT_FOUND"
    assert error.value.details == {"todo_id": 99999}


def test_update_todo_applies_partial_changes(db_session: Session) -> None:
    service = TodoService(db_session)
    created = service.create_todo(TodoCreateRequest(title="Pending"))

    updated = service.update_todo(todo_id=created.id, payload=TodoUpdateRequest(is_completed=True))

    assert updated.id == created.id
    assert updated.title == "Pending"
    assert updated.is_completed is True


def test_update_todo_without_changes_does_not_call_commit(db_session: Session) -> None:
    service = TodoService(db_session)
    created = service.create_todo(TodoCreateRequest(title="No changes"))

    service.db_session.commit = create_autospec(service.db_session.commit)

    unchanged = service.update_todo(
        todo_id=created.id,
        payload=TodoUpdateRequest(title="No changes", is_completed=False),
    )

    assert unchanged.id == created.id
    assert unchanged.title == "No changes"
    assert unchanged.is_completed is False
    service.db_session.commit.assert_not_called()


def test_delete_todo_raises_not_found_for_unknown_id(db_session: Session) -> None:
    service = TodoService(db_session)

    with pytest.raises(TodoNotFoundError):
        service.delete_todo(todo_id=123456)


def test_delete_todo_removes_entity(db_session: Session) -> None:
    service = TodoService(db_session)
    repository = TodoRepository(db_session)

    created = service.create_todo(TodoCreateRequest(title="Delete me"))
    service.delete_todo(todo_id=created.id)

    assert repository.get_todo_by_id(todo_id=created.id) is None


def test_list_todos_returns_repository_results(db_session: Session) -> None:
    service = TodoService(db_session)

    service.create_todo(TodoCreateRequest(title="A"))
    service.create_todo(TodoCreateRequest(title="B"))

    todos = service.list_todos()

    assert len(todos) == 2
    assert [todo.title for todo in todos] == ["B", "A"]
