# SQLAlchemy or Tortoise models
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# Model
class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(500))
    name: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[str] = mapped_column(DateTime())
    # Map
    messages: Mapped[List["Messages"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    recipient_u: Mapped[List["Message_Recipients"]] = relationship(
        back_populates="recipient_user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Users(id={self.id!r}, email={self.email!r}, name={self.name!r}), created_at={self.created_at!r})"


class Messages(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    subject: Mapped[str] = mapped_column(String(500), nullable=True)
    content: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[str] = mapped_column(DateTime())
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # Map
    user: Mapped["Users"] = relationship(back_populates="messages")
    recipient_m: Mapped[List["Message_Recipients"]] = relationship(
        back_populates="recipient_message", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Messages(id={self.id!r}, subject={self.subject!r}, content={self.content!r}), timestamp={self.timestamp!r})"


class Message_Recipients(Base):
    __tablename__ = "message_recipients"
    id: Mapped[int] = mapped_column(primary_key=True)
    message_id: Mapped[int] = mapped_column(ForeignKey("messages.id"))
    recipient_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    read: Mapped[bool] = mapped_column(Boolean)
    read_at: Mapped[str] = mapped_column(DateTime(), nullable=True)
    # Map
    recipient_message: Mapped["Messages"] = relationship(back_populates="recipient_m")
    recipient_user: Mapped["Users"] = relationship(back_populates="recipient_u")

    def __repr__(self) -> str:
        return f"Message Recipients(id={self.id!r}, read={self.read!r}, read_at={self.read_at!r})"


#
# Base.metadata.create_all(get_connection)
