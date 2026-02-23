from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.models.todo import Todo


class TodoRepository:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def create_todo(self, *, title: str, category: str = "general") -> Todo:
        todo = Todo(title=title, category=category, is_completed=False)
        self.db_session.add(todo)
        return todo

    def list_todos(self) -> list[Todo]:
        return self.db_session.query(Todo).order_by(desc(Todo.created_at), desc(Todo.id)).all()

    def get_todo_by_id(self, *, todo_id: int) -> Todo | None:
        return self.db_session.query(Todo).filter(Todo.id == todo_id).first()

    def get_todo_by_canonical_title_and_category(self, *, title: str, category: str) -> Todo | None:
        return (
            self.db_session.query(Todo)
            .filter(
                func.lower(Todo.title) == title.lower(),
                func.lower(Todo.category) == category.lower(),
            )
            .first()
        )

    def save(self, todo: Todo) -> Todo:
        self.db_session.add(todo)
        return todo

    def delete_todo(self, *, todo: Todo) -> None:
        self.db_session.delete(todo)
