# Pydantic models
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ValidationError


# Users
class UsersBase(BaseModel):
    email: str
    name: str


class UsersCreate(UsersBase):
    pass


class UserRead(UsersBase):
    id: UUID
    created_at: datetime


# Message
class MessageBase(BaseModel):
    sender_id: Optional[UUID]
    subject: Optional[str]
    content: str
    timestamp: Optional[datetime]


class MessageCreate(MessageBase):
    recipient_id: List[UUID]


class MessageRead(MessageBase):
    id: UUID


# Message Recipient


class MessageRecipientRead(BaseModel):
    id: UUID
    read: bool
    read_at: datetime | None = None
    message_id: UUID


class MessageInbox(MessageRecipientRead):
    subject: Optional[str]
    content: str
    timestamp: Optional[datetime]


class MessageAllRecipients(MessageBase):
    recipient_m: List[MessageRecipientRead]

    class Config:
        orm_mode = True
