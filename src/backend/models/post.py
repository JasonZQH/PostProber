from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    platforms = Column(JSON)  # List of platforms to post to
    status = Column(String, default="draft")  # draft, posting, posted, failed
    ai_suggestions = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    posted_at = Column(DateTime(timezone=True))

    # Relationship
    user = relationship("User", back_populates="posts")

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    platform = Column(String, nullable=False)  # twitter, linkedin, instagram
    account_name = Column(String)
    access_token = Column(Text)  # Encrypted
    refresh_token = Column(Text)  # Encrypted
    token_expires_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    user = relationship("User", back_populates="accounts")

class MonitoringLog(Base):
    __tablename__ = "monitoring_logs"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    platform = Column(String)
    step = Column(String)  # authentication, posting, verification, engagement
    status = Column(String)  # pending, success, failed, warning
    details = Column(JSON)
    ai_analysis = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    post = relationship("Post", back_populates="monitoring_logs")