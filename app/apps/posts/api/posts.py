from fastapi import APIRouter, Response, Depends
from fastapi.exceptions import RequestValidationError

from app.apps.users.models import User
from app.db import Session
from app.apps.posts.models import Post
from app.apps.posts.schemas import PostCreate, PostShow
from app.apps.comments.schemas import CommentShow
from typing import List
from http import HTTPStatus
from pydantic.error_wrappers import ErrorWrapper

from app.utils import get_current_user

posts_router = APIRouter(prefix="/posts")


@posts_router.get("/", response_model=List[PostShow])
def list_posts(user: User = Depends(get_current_user)):
    session = Session()
    posts = session.query(Post).all()
    session.commit()
    return [PostShow(id=post.id,
                     text=post.text,
                     created_by=post.created_by,
                     comments=[CommentShow(id=comment.id,
                                           text=comment.text,
                                           related_post_id=comment.related_post_id,
                                           created_by=comment.related_post.created_by)
                               for comment in post.comments]) for post in posts]


@posts_router.get("/{post_id}/", response_model=PostShow)
def get_post(post_id: int, user: User = Depends(get_current_user)):
    session = Session()
    post = session.query(Post).get(post_id)
    if post is None:
        error = ErrorWrapper(ValueError(f"Post with id={post_id} not found"), ("query", "post_id"))
        raise RequestValidationError(errors=[error])
    session.commit()
    return PostShow(id=post.id,
                    text=post.text,
                    created_by=post.created_by,
                    comments=[CommentShow(id=comment.id,
                                          text=comment.text,
                                          related_post_id=comment.related_post_id,
                                          created_by=comment.related_post.created_by)
                              for comment in post.comments])


@posts_router.post("/", response_model=PostShow)
def create_post(data: PostCreate, user: User = Depends(get_current_user)):
    session = Session()
    post = Post(text=data.text, created_by=user.login)
    session.add(post)
    session.commit()
    return PostShow(id=post.id,
                    text=post.text,
                    created_by=post.created_by,
                    comments=[CommentShow(id=comment.id,
                                          text=comment.text,
                                          related_post_id=comment.related_post_id,
                                          created_by=comment.created_by)
                              for comment in post.comments])


@posts_router.patch("/{post_id}/", response_model=PostShow)
def update_post(post_id: int, data: PostCreate, user: User = Depends(get_current_user)):
    session = Session()
    post = session.query(Post).get(post_id)
    if post is None:
        error = ErrorWrapper(ValueError(f"Post with id={post_id} not found"), ("query", "post_id"))
        raise RequestValidationError(errors=[error])
    if post.created_by != user.login:
        error = ErrorWrapper(ValueError("You are not permitted to delete this post"), ("query", "comment_id"))
        raise RequestValidationError(errors=[error])
    post.text = data.text
    session.commit()
    return PostShow(id=post.id,
                    text=post.text,
                    created_by=post.created_by,
                    comments=[CommentShow(id=comment.id,
                                          text=comment.text,
                                          related_post_id=comment.related_post_id,
                                          created_by=comment.created_by)
                              for comment in post.comments])


@posts_router.delete("/{post_id}/", status_code=HTTPStatus.NO_CONTENT)
def delete_post(post_id: int, user: User = Depends(get_current_user)):
    session = Session()
    post = session.query(Post).get(post_id)
    if post is None:
        error = ErrorWrapper(ValueError(f"Post with id={post_id} not found"), ("query", "post_id"))
        raise RequestValidationError(errors=[error])
    if post.created_by != user.login:
        error = ErrorWrapper(ValueError("You are not permitted to delete this post"), ("query", "comment_id"))
        raise RequestValidationError(errors=[error])
    session.delete(post)
    session.commit()
    return Response(status_code=HTTPStatus.NO_CONTENT)
