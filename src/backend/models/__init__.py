from .user import User
from .post import Post, Account, MonitoringLog

# Add relationships back to User model
from sqlalchemy.orm import relationship

# Add these to User model
User.posts = relationship("Post", back_populates="user")
User.accounts = relationship("Account", back_populates="user")

# Add these to Post model
Post.monitoring_logs = relationship("MonitoringLog", back_populates="post")

__all__ = ["User", "Post", "Account", "MonitoringLog"]