from sqlalchemy.orm import Session

from app.core.errors import TodoDuplicateError, TodoNotFoundError, TodoValidationError
from app.core.normalization import canonicalize_text, normalize_category, normalize_title
from app.repositories.todo_repository import TodoRepository
from app.schemas.todo import TodoCreateRequest, TodoUpdateRequest


class TodoService:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
        self.todo_repository = TodoRepository(db_session)

    def create_todo(self, payload: TodoCreateRequest):
        try:
            normalized_title = normalize_title(payload.title)
            normalized_category = normalize_category(
                payload.category,
                default_if_empty=True,
                coerce_numeric=False,
            )
        except (TypeError, ValueError) as error:
            raise TodoValidationError(str(error)) from error

        duplicate = self.todo_repository.get_todo_by_canonical_title_and_category(
            title=canonicalize_text(normalized_title),
            category=canonicalize_text(normalized_category),
        )
        if duplicate is not None:
            raise TodoDuplicateError(title=normalized_title, category=normalized_category)

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
        if payload.title is not None:
            try:
                normalized_title = normalize_title(payload.title)
            except (TypeError, ValueError) as error:
                raise TodoValidationError(str(error)) from error

            if canonicalize_text(normalized_title) != canonicalize_text(todo.title):
                todo.title = normalized_title
                has_changes = True

        if payload.category is not None:
            try:
                normalized_category = normalize_category(
                    payload.category,
                    default_if_empty=False,
                    coerce_numeric=True,
                )
            except (TypeError, ValueError) as error:
                raise TodoValidationError(str(error)) from error

            if canonicalize_text(normalized_category) != canonicalize_text(todo.category):
                todo.category = normalized_category
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
