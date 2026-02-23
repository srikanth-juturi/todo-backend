from sqlalchemy.orm import Session

from app.core.errors import TodoNotFoundError, TodoValidationError
from app.repositories.todo_repository import TodoRepository
from app.schemas.todo import TodoCreateRequest, TodoUpdateRequest


class TodoService:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
        self.todo_repository = TodoRepository(db_session)

    def create_todo(self, payload: TodoCreateRequest):
        normalized_title = payload.title.strip()
        if not normalized_title:
            raise TodoValidationError("Title must not be empty")

        normalized_category = payload.category.strip()
        if not normalized_category:
            raise TodoValidationError("Category must not be empty")

        todo = self.todo_repository.create_todo(title=normalized_title, category=normalized_category)
        self.db_session.commit()
        return todo

    def list_todos(self):
        return self.todo_repository.list_todos()

    def update_todo(self, *, todo_id: int, payload: TodoUpdateRequest):
        todo = self.todo_repository.get_todo_by_id(todo_id=todo_id)
        if todo is None:
            raise TodoNotFoundError(todo_id)

        has_changes = False
        if payload.title is not None and payload.title != todo.title:
            todo.title = payload.title
            has_changes = True
        if payload.category is not None and payload.category != todo.category:
            todo.category = payload.category
            has_changes = True
        if payload.is_completed is not None and payload.is_completed != todo.is_completed:
            todo.is_completed = payload.is_completed
            has_changes = True

        if has_changes:
            todo = self.todo_repository.save(todo)
            self.db_session.commit()

        return todo

    def delete_todo(self, *, todo_id: int) -> None:
        todo = self.todo_repository.get_todo_by_id(todo_id=todo_id)
        if todo is None:
            raise TodoNotFoundError(todo_id)

        self.todo_repository.delete_todo(todo=todo)
        self.db_session.commit()
