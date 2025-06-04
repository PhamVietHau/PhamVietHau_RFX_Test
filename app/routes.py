# FastAPI routes
from datetime import datetime
from typing import Annotated, List
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.db import get_session
from app.models import Message_Recipients, Messages, Users
from app.schemas import (MessageAllRecipients, MessageCreate, MessageInbox,
                         MessageRead, MessageRecipientRead, UserRead,
                         UsersCreate)

SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter()


# User APIs
# Create User
@router.post("/users", response_model=UserRead)
async def create_user(user_data: UsersCreate, session: SessionDep) -> Users:
    user = session.query(Users).filter(Users.email == user_data.email).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    user = Users(
        id=uuid4(),
        email=user_data.email,
        name=user_data.name,
        created_at=datetime.utcnow(),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# Retrieve user info
@router.get("/users/{user_id}", response_model=UserRead)
async def retrieve_user(user_id: UUID, session: SessionDep) -> Users:
    user = session.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


# List users
@router.get("/users", response_model=List[UserRead])
async def list_user(session: SessionDep) -> Users:
    user = session.query(Users).all()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


# Message APIs
# Send a message to one or more recipients
@router.post("/message/send")
async def send_message(message_data: MessageCreate, session: SessionDep):
    message = Messages(
        id=uuid4(),
        sender_id=message_data.sender_id,
        subject=message_data.subject,
        content=message_data.content,
        timestamp=datetime.utcnow(),
    )
    session.add(message)
    session.commit()
    session.refresh(message)
    for recipient_id in message_data.recipient_id:
        recipient = Message_Recipients(
            id=uuid4(),
            message_id=message.id,
            recipient_id=recipient_id,
            read=False,
            read_at=None,
        )
        session.add(recipient)
    session.commit()
    return {"status": "ok"}


# View sent messages
@router.get("/message/{sender_id}/sent", response_model=List[MessageRead])
async def view_sent_message(sender_id: UUID, session: SessionDep) -> Messages:
    sent_message = session.query(Messages).filter(Messages.sender_id == sender_id).all()
    if not sent_message:
        raise HTTPException(status_code=404, detail="user not found")
    return sent_message


# View inbox messages
@router.get("/message/{recipient_id}/inbox", response_model=List[MessageInbox])
async def view_inbox_message(
    recipient_id: UUID, session: SessionDep
) -> Message_Recipients:
    inbox_message = (
        session.query(
            Message_Recipients.id,
            Message_Recipients.message_id,
            Messages.subject,
            Messages.content,
            Messages.sender_id,
            Messages.timestamp,
            Message_Recipients.recipient_id,
            Message_Recipients.read,
            Message_Recipients.read_at,
        )
        .join(Message_Recipients, Message_Recipients.message_id == Messages.id)
        .filter(Message_Recipients.recipient_id == recipient_id)
    )
    if not inbox_message:
        raise HTTPException(status_code=404, detail="user not found")
    return inbox_message


# View unread messages
@router.get(
    "/message/{recipient_id}/inbox/unread", response_model=List[MessageRecipientRead]
)
async def view_unread_message(
    recipient_id: UUID, session: SessionDep
) -> Message_Recipients:
    inbox_message = (
        session.query(
            Message_Recipients.id,
            Message_Recipients.message_id,
            Messages.subject,
            Messages.content,
            Messages.sender_id,
            Messages.timestamp,
            Message_Recipients.recipient_id,
            Message_Recipients.read,
            Message_Recipients.read_at,
        )
        .join(Message_Recipients, Message_Recipients.message_id == Messages.id)
        .filter(
            Message_Recipients.recipient_id == recipient_id,
            Message_Recipients.read == False,
        )
        .all()
    )

    if not inbox_message:
        raise HTTPException(status_code=404, detail="user not found")
    return inbox_message


# View a message with all recipients
@router.get(
    "/message/view_recipients/{message_id}", response_model=MessageAllRecipients
)
async def view_message_with_all_recipients(
    message_id: UUID, session: SessionDep
) -> Messages:
    view_with_all = (
        session.query(Messages)
        .options(joinedload(Messages.recipient_m))
        .filter(Messages.id == message_id)
        .first()
    )

    if not view_with_all:
        raise HTTPException(status_code=404, detail="user not found")
    return view_with_all


# Mark a message as read


@router.patch("/message/{recipient_id}/inbox/{message_id}")
async def update_status(recipient_id: UUID, message_id: UUID, session: SessionDep):
    message = (
        session.query(Message_Recipients)
        .filter(
            Message_Recipients.message_id == message_id,
            Message_Recipients.recipient_id == recipient_id,
        )
        .first()
    )
    if not message:
        raise HTTPException(status_code=404, detail="message not found")
    message.read = True
    message.read_at = datetime.utcnow()
    session.commit()
    session.refresh(message)
    return {"status": "ok"}
