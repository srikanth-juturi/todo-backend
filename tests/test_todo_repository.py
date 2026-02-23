from sqlalchemy.orm import Session
import pytest
from sqlalchemy.exc import IntegrityError

from app.models.todo import Todo
from app.repositories.todo_repository import TodoRepository


def test_create_and_get_todo_by_id(db_session: Session) -> None:
    repository = TodoRepository(db_session)

    created = repository.create_todo(title="Read docs")
    db_session.commit()

    loaded = repository.get_todo_by_id(todo_id=created.id)

    assert loaded is not None
    assert loaded.id == created.id
    assert loaded.title == "Read docs"
    assert loaded.category == "general"
    assert loaded.is_completed is False


def test_list_todos_orders_by_created_desc_and_id_desc(db_session: Session) -> None:
    repository = TodoRepository(db_session)

    first = repository.create_todo(title="First")
    second = repository.create_todo(title="Second")
    third = repository.create_todo(title="Third")
    db_session.commit()

    todos = repository.list_todos()

    assert [todo.id for todo in todos] == [third.id, second.id, first.id]


def test_delete_todo_removes_row(db_session: Session) -> None:
    repository = TodoRepository(db_session)

    todo = repository.create_todo(title="To remove")
    db_session.commit()

    persistent_todo = repository.get_todo_by_id(todo_id=todo.id)
    assert persistent_todo is not None

    repository.delete_todo(todo=persistent_todo)
    db_session.commit()

    assert repository.get_todo_by_id(todo_id=todo.id) is None


def test_save_persists_updated_fields(db_session: Session) -> None:
    repository = TodoRepository(db_session)

    todo = repository.create_todo(title="Original")
    db_session.commit()

    todo.title = "Updated"
    todo.category = "work"
    todo.is_completed = True
    repository.save(todo)
    db_session.commit()

    refreshed = db_session.query(Todo).filter(Todo.id == todo.id).first()
    assert refreshed is not None
    assert refreshed.title == "Updated"
    assert refreshed.category == "work"
    assert refreshed.is_completed is True


def test_create_todo_persists_custom_category(db_session: Session) -> None:
    repository = TodoRepository(db_session)

    created = repository.create_todo(title="Refactor", category="engineering")
    db_session.commit()

    loaded = repository.get_todo_by_id(todo_id=created.id)
    assert loaded is not None
    assert loaded.category == "engineering"


def test_create_todo_rejects_category_beyond_db_limit(db_session: Session) -> None:
    repository = TodoRepository(db_session)

    repository.create_todo(title="Too long", category="x" * 51)

    with pytest.raises(IntegrityError):
        db_session.commit()
