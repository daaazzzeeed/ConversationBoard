from app.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.apps.comments.models import Comment


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    comments = relationship("Comment", back_populates="related_post", cascade="delete, all, ")
    created_by = Column(String, nullable=False)
