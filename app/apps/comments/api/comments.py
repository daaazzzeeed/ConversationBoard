from fastapi import APIRouter, Response, Depends
from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ErrorWrapper

from app.apps.users.models import User
from app.db import Session
from app.apps.comments.models import Comment
from app.apps.comments.schemas import CommentCreate, CommentShow, ChildCommentShow
from app.apps.posts.schemas import PostShow, PostComment
from typing import List
from http import HTTPStatus
from app.utils import get_current_user


comments_router = APIRouter(prefix="/comments")


@comments_router.get("/", response_model=List[CommentShow])
def list_comments(user: User = Depends(get_current_user)):
    session = Session()
    comments = session.query(Comment).all()
    session.commit()
    return [CommentShow(id=comment.id,
                        text=comment.text,
                        related_post_id=comment.related_post_id,
                        created_by=comment.created_by,
                        related_post=PostShow(id=comment.related_post_id,
                                              text=comment.related_post.text,
                                              created_by=comment.related_post.created_by,
                                              comments=[PostComment(id=comment.id)
                                                        for comment in comment.related_post.comments]),
                        responds_to_comment_id=comment.parent_comment_id,
                        children_comments=[ChildCommentShow(id=comment.id,
                                                            text=comment.text,
                                                            created_by=comment.created_by)
                                           for comment in comment.children_comments])
            for comment in comments]


@comments_router.get("/{comment_id}/", response_model=CommentShow)
def get_comment(comment_id: int, user: User = Depends(get_current_user)):
    session = Session()
    comment = session.query(Comment).get(comment_id)
    if comment is None:
        error = ErrorWrapper(ValueError(f"Comment with id={comment_id} not found"), ("query", "comment_id"))
        raise RequestValidationError(errors=[error])
    session.commit()
    return CommentShow(id=comment.id,
                       text=comment.text,
                       related_post_id=comment.related_post_id,
                       created_by=comment.created_by,
                       related_post=PostShow(id=comment.related_post_id,
                                             text=comment.related_post.text,
                                             created_by=comment.related_post.created_by,
                                             comments=[PostComment(id=comment.id)
                                                       for comment in comment.related_post.comments]),
                       responds_to_comment_id=comment.parent_comment_id,
                       children_comments=[ChildCommentShow(id=comment.id,
                                                           text=comment.text,
                                                           created_by=comment.created_by)
                                          for comment in comment.children_comments])


@comments_router.post("/", response_model=CommentShow)
def create_comment(data: CommentCreate, user: User = Depends(get_current_user)):
    session = Session()
    comment = Comment(text=data.text,
                      related_post_id=data.related_post_id,
                      parent_comment_id=data.responds_to_comment_id,
                      created_by=user.login)
    session.add(comment)
    session.commit()
    related_post = comment.related_post
    return CommentShow(id=comment.id,
                       text=comment.text,
                       related_post_id=related_post.id,
                       created_by=comment.created_by,
                       related_post=PostShow(id=related_post.id,
                                             text=related_post.text,
                                             created_by=related_post.created_by,
                                             comments=[PostComment(id=comment.id)
                                                       for comment in related_post.comments]),
                       responds_to_comment_id=comment.parent_comment_id,
                       children_comments=[ChildCommentShow(id=comment.id,
                                                           text=comment.text,
                                                           created_by=comment.created_by)
                                          for comment in comment.children_comments])


@comments_router.patch("/{comment_id}/", response_model=CommentShow)
def update_comment(comment_id: int, data: CommentCreate, user: User = Depends(get_current_user)):
    session = Session()
    comment = session.query(Comment).get(comment_id)
    if comment is None:
        error = ErrorWrapper(ValueError(f"Comment with id={comment_id} not found"), ("query", "comment_id"))
        raise RequestValidationError(errors=[error])
    if comment.created_by != user.login:
        error = ErrorWrapper(ValueError("You are not permitted to edit this comment"), ("query", "comment_id"))
        raise RequestValidationError(errors=[error])
    comment.text = data.text
    session.add(comment)
    session.commit()
    related_post = comment.related_post
    return CommentShow(id=comment.id,
                       text=comment.text,
                       related_post_id=related_post.id,
                       related_post=PostShow(id=related_post.id,
                                             text=related_post.text,
                                             created_by=related_post.created_by,
                                             comments=[PostComment(id=comment.id)
                                                       for comment in related_post.comments]),
                       responds_to_comment_id=comment.parent_comment_id,
                       created_by=comment.created_by,
                       children_comments=[ChildCommentShow(id=comment.id,
                                                           text=comment.text,
                                                           created_by=comment.created_by)
                                          for comment in comment.children_comments])


@comments_router.delete("/{comment_id}/", status_code=HTTPStatus.NO_CONTENT)
def delete_comment(comment_id: int, user: User = Depends(get_current_user)):
    session = Session()
    comment = session.query(Comment).get(comment_id)
    if comment is None:
        error = ErrorWrapper(ValueError(f"Comment with id={comment_id} not found"), ("query", "comment_id"))
        raise RequestValidationError(errors=[error])
    if comment.created_by != user.login:
        error = ErrorWrapper(ValueError("You are not permitted to delete this comment"), ("query", "comment_id"))
        raise RequestValidationError(errors=[error])
    session.delete(comment)
    session.commit()
    return Response(status_code=HTTPStatus.NO_CONTENT)
