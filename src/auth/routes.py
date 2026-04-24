from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import UserCreateModel, UserModel, UserLoginModel
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import HashHelper
from datetime import timedelta
from fastapi.responses import JSONResponse

auth_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIRY = 2

#Bearer Token


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserModel)
async def create_user_account(user_data : UserCreateModel, session : AsyncSession = Depends(get_session)) :
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with this email already exists.")
    new_user = await user_service.create_user(user_data, session)

    return new_user

@auth_router.post("/login")
async def login_users(login_data : UserLoginModel, session : AsyncSession = Depends(get_session)) :
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is not None :
        password_valid = HashHelper.verify_password(plain_password=password, hashed_password=user.password_hash)

        if password_valid :
            access_token = HashHelper.create_access_token(
                user_data = {
                    "email" : user.email,
                    'uid' : str(user.uid)
                }
                                                          )
            
            refresh_token = HashHelper.create_access_token(
                user_data={
                    "email" : user.email,
                    'uid' : str(user.uid)
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )

            return JSONResponse(
                content={
                    "message" : "Login Successful",
                    "access_token" : access_token,
                    "refresh_token" : refresh_token,
                    "user" :{
                        "email" : user.email,
                        "uid" : str(user.uid)
                    }
                }
            )
        
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
