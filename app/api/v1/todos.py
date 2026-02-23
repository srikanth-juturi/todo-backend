from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.schemas.todo import TodoCreateRequest, TodoResponse, TodoUpdateRequest
from app.services.todo_service import TodoService

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreateRequest, db_session: Session = Depends(get_db_session)) -> TodoResponse:
    todo_service = TodoService(db_session)
    todo = todo_service.create_todo(payload)
    return TodoResponse.model_validate(todo)


@router.get("", response_model=list[TodoResponse], status_code=status.HTTP_200_OK)
def list_todos(db_session: Session = Depends(get_db_session)) -> list[TodoResponse]:
    todo_service = TodoService(db_session)
    todos = todo_service.list_todos()
    return [TodoResponse.model_validate(todo) for todo in todos]


@router.patch("/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def update_todo(
    todo_id: int,
    payload: TodoUpdateRequest,
    db_session: Session = Depends(get_db_session),
) -> TodoResponse:
    todo_service = TodoService(db_session)
    todo = todo_service.update_todo(todo_id=todo_id, payload=payload)
    return TodoResponse.model_validate(todo)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db_session: Session = Depends(get_db_session)) -> None:
    todo_service = TodoService(db_session)
    todo_service.delete_todo(todo_id=todo_id)
