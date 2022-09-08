from app.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    related_post_id = Column(Integer, ForeignKey("post.id"), nullable=True)
    related_post = relationship("Post", back_populates="comments")
    parent_comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    children_comments = relationship("Comment",
                                     remote_side=[parent_comment_id],
                                     uselist=True,
                                     cascade="delete, all,")
    created_by = Column(String, nullable=False)
