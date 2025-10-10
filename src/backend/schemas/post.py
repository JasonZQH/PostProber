from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

# Post schemas
class PostBase(BaseModel):
    content: str
    platforms: List[str]

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    content: Optional[str] = None
    platforms: Optional[List[str]] = None
    status: Optional[str] = None

class PostResponse(PostBase):
    id: int
    user_id: int
    status: str
    ai_suggestions: Optional[Dict[str, Any]] = None
    created_at: datetime
    posted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Account schemas
class AccountBase(BaseModel):
    platform: str
    account_name: Optional[str] = None

class AccountCreate(AccountBase):
    access_token: str
    refresh_token: Optional[str] = None

class AccountResponse(AccountBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Monitoring schemas
class MonitoringLogResponse(BaseModel):
    id: int
    post_id: int
    platform: Optional[str]
    step: Optional[str]
    status: Optional[str]
    details: Optional[Dict[str, Any]] = None
    ai_analysis: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True