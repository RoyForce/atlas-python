from fastapi import APIRouter, Depends, Response, Request
import typing as t

from app.db.session import get_db
from app.db.questions.models import Question
from app.db.core import (
    get_lists,
    get_item,
    create_item,
    delete_item,
    edit_item,
)

from app.db.questions.schemas import (
    QuestionEdit,
    QuestionOut,
)

from app.core.auth import get_current_active_user

question_router = r = APIRouter()


@r.get(
    "/questions",
    response_model=t.List[QuestionOut],
)
async def question_list(
    request: Request,
    response: Response,
    db=Depends(get_db),
):
    """
    Get all question
    """
    questions = get_lists(db, Question, request.query_params)
    response.headers["Content-Range"] = f"0-9/{len(questions)}"
    return questions


@r.get(
    "/questions/{question_id}",
    response_model=QuestionOut,
)
async def question_details(
    question_id: int,
    db=Depends(get_db),
):
    """
    Get any question details
    """
    return get_item(db, Question, question_id)


@r.post(
    "/questions",
    response_model=QuestionOut,
)
async def question_create(
    question: QuestionEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Create a new question
    """

    question.created_by = current_user.id
    return create_item(db, Question, question)


@r.put(
    "/questions/{question_id}",
    response_model=QuestionOut,
)
async def question_edit(
    question_id: int,
    question: QuestionEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Update existing question
    """
    question.updated_by = current_user.id
    return edit_item(db, Question, question_id, question)


@r.delete(
    "/questions/{question_id}",
    response_model=QuestionOut,
)
async def question_delete(
    question_id: int,
    db=Depends(get_db),
):
    """
    Delete existing question
    """
    return delete_item(db, Question, question_id)
