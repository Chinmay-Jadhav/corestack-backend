from fastapi import status, APIRouter, Depends
from fastapi.exceptions import HTTPException

from src import books
from src.books.models import Book as BookModel
from src.books.schemas import BookUpdateModel, BookCreateModel, Book as BookSchema
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from typing import List
import uuid

book_router = APIRouter()
book_service = BookService()

@book_router.get("/", response_model=List[BookSchema])
async def get_all_books(session : AsyncSession = Depends(get_session)) :
    books = await book_service.get_all_books(session)
    return books

@book_router.post("/", status_code= status.HTTP_201_CREATED, response_model=BookSchema)
async def create_a_book(book_data : BookCreateModel, session : AsyncSession = Depends(get_session)) -> dict :
    new_book = await book_service.create_book(book_data, session)

    return new_book

@book_router.get("/{book_uid}", response_model=BookSchema)
async def get_book(book_uid : uuid.UUID, session : AsyncSession = Depends(get_session)) -> dict :
    book = await book_service.get_book(book_uid, session)
    
    if book :
        return book
    else :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@book_router.patch("/{book_uid}", response_model=BookSchema)
async def update_book(
    book_uid : uuid.UUID,
    book_update_data : BookUpdateModel,
    session : AsyncSession = Depends(get_session)
    ) -> dict :

    updated_book = await book_service.update_book(book_uid, book_update_data, session)

    if updated_book is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    else :
        return updated_book

@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_uid : uuid.UUID,
    session : AsyncSession = Depends(get_session)
    ) :
    book_to_delete = await book_service.delete_book(book_uid, session)

    if book_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    return None