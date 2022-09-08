from fastapi import FastAPI

from app.apps.posts.api.posts import posts_router
from app.apps.comments.api.comments import comments_router
from app.apps.users.api.users import users_router

app = FastAPI(title="Conversations")


app.include_router(posts_router)
app.include_router(comments_router)
app.include_router(users_router)


@app.get("/")
def check_app():
    return {"app": "OK"}

