from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.todo import Todo


class TodoRepository:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def create_todo(self, *, title: str) -> Todo:
        todo = Todo(title=title, is_completed=False)
        self.db_session.add(todo)
        self.db_session.flush()
        self.db_session.refresh(todo)
        return todo

    def list_todos(self) -> list[Todo]:
        return self.db_session.query(Todo).order_by(desc(Todo.created_at), desc(Todo.id)).all()

    def get_todo_by_id(self, *, todo_id: int) -> Todo | None:
        return self.db_session.query(Todo).filter(Todo.id == todo_id).first()

    def save(self, todo: Todo) -> Todo:
        self.db_session.add(todo)
        self.db_session.flush()
        self.db_session.refresh(todo)
        return todo

    def delete_todo(self, *, todo: Todo) -> None:
        self.db_session.delete(todo)
