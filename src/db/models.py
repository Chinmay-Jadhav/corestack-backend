from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime, timezone, date
from typing import Optional, List

"""
class User :
    uid : uuid.UUID
    username : str
    email : str
    first_name : str
    last_name : str
    is_verified : bool = False
    created_at : datetime
    updated_at : datetime
"""

class User(SQLModel, table = True) :
    __tablename__ = "users"

    uid : uuid.UUID = Field(
        sa_column= Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    username : str
    password_hash : str = Field(nullable=False, exclude=True)
    email : str
    first_name : str
    last_name : str
    role : str = Field(sa_column = Column(
        pg.VARCHAR,
        nullable = False,
        server_default = "user"
    ))
    is_verified : bool = Field(default=False)
    created_at : datetime = Field(sa_column = Column(
        pg.TIMESTAMP(timezone=True),
        default=lambda : datetime.now(timezone.utc)
        ))
    updated_at : datetime = Field(sa_column = Column(
        pg.TIMESTAMP(timezone=True),
        default= lambda : datetime.now(timezone.utc),
        onupdate=lambda : datetime.now(timezone.utc)
        ))
    books : List["Book"] = Relationship(back_populates="user", sa_relationship_kwargs={'lazy' : 'selectin'})

    def __repr__(self):
        return f"<User {self.username}>"
    


class Book(SQLModel, table = True) :
    __tablename__ = "books"

    uid : uuid.UUID = Field(
        sa_column= Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    title : str
    author : str
    publisher : str
    published_date : date
    page_count : int
    language : str
    user_uid : Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    created_at : datetime = Field(sa_column = Column(pg.TIMESTAMP, default=datetime.now()))
    updated_at : datetime = Field(sa_column = Column(pg.TIMESTAMP, default=datetime.now()))
    user : Optional[User] = Relationship(back_populates="books")
    # user : Optional["models.User"] = Relationship(back_populates="books", sa_relationship_kwargs={'lazy' : 'selectin'})

    def __repr__(self):
        return f"<Book {self.title}"
    
class Review(SQLModel, table = True) :
    __tablename__ = "reviews"

    uid : uuid.UUID = Field(
        sa_column= Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    rating : int = Field(lt=5)
    review_text : str
    user_uid : Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    book_uid : Optional[uuid.UUID] = Field(default=None, foreign_key="books.uid")
    created_at : datetime = Field(sa_column = Column(pg.TIMESTAMP, default=datetime.now()))
    updated_at : datetime = Field(sa_column = Column(pg.TIMESTAMP, default=datetime.now()))
    user : Optional[User] = Relationship(back_populates="books")

    def __repr__(self):
        return f"<Review for {self.book_uid} by user {self.user_uid}>   `"