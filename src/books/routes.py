from fastapi import status, APIRouter, Depends

from src import books
from src.db.models import Book as BookModel
from src.books.schemas import BookUpdateModel, BookCreateModel,BookDetailModel, Book as BookSchema
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.errors import BookNotFound


from typing import List
import uuid

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(allowed_roles=["admin", "user"])

@book_router.get("/", response_model=List[BookSchema], dependencies=[Depends(role_checker)])
async def get_all_books(
    session : AsyncSession = Depends(get_session), 
    token_details : dict = Depends(access_token_bearer),
    ) -> dict :
    # print(user_details)
    books = await book_service.get_all_books(session)
    return books

@book_router.get("/user/{user_uid}", response_model=List[BookSchema], dependencies=[Depends(role_checker)])
async def get_user_book_submissions(
    user_uid : str , 
    session : AsyncSession = Depends(get_session), 
    token_details : dict = Depends(access_token_bearer),
    ) -> dict :

    books = await book_service.get_user_books(user_uid, session)
    return books

@book_router.post("/", status_code= status.HTTP_201_CREATED, response_model=BookSchema, dependencies=[Depends(role_checker)])
async def create_a_book(
    book_data : BookCreateModel,
    session : AsyncSession = Depends(get_session),
    token_details : dict = Depends(access_token_bearer)
    ) -> dict :

    user_id = token_details['sub']
    new_book = await book_service.create_book(book_data, user_id, session)

    return new_book

@book_router.get("/{book_uid}", response_model=BookDetailModel, dependencies=[Depends(role_checker)])
async def get_book(
    book_uid : uuid.UUID,
    session : AsyncSession = Depends(get_session),
    token_details : dict = Depends(access_token_bearer)
    ) -> dict :
    book = await book_service.get_book(book_uid, session)
    
    if book :
        return book
    else :
        raise BookNotFound()
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@book_router.patch("/{book_uid}", response_model=BookSchema, dependencies=[Depends(role_checker)])
async def update_book(
    book_uid : uuid.UUID,
    book_update_data : BookUpdateModel,
    session : AsyncSession = Depends(get_session),
    token_details : dict = Depends(access_token_bearer)
    ) -> dict :

    updated_book = await book_service.update_book(book_uid, book_update_data, session)

    if updated_book is None :
        raise BookNotFound()
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    else :
        return updated_book

@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(role_checker)])
async def delete_book(
    book_uid : uuid.UUID,
    session : AsyncSession = Depends(get_session),
    token_details : dict = Depends(access_token_bearer)
    ) :
    book_to_delete = await book_service.delete_book(book_uid, session)

    if book_to_delete is None:
        raise BookNotFound()
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    return None