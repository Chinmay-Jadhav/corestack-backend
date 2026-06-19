from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import UserCreateModel, UserModel, UserLoginModel, UserBooksModel
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from src.db.redis import add_jti_to_blocklist

from .utils import HashHelper
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(allowed_roles=["admin", "user"])

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
                    'uid' : str(user.uid),
                    "role" : user.role
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

@auth_router.get("/refresh_token")
async def get_new_access_token(token_details : dict = Depends(RefreshTokenBearer())) :

    new_access_token = HashHelper.create_access_token(
        user_data= {
            "uid" : token_details["sub"]
        }
    )

    return JSONResponse(content={"access_token" : new_access_token})

@auth_router.get('/me', response_model=UserBooksModel)
async def get_current_user(
    user = Depends(get_current_user),
    _ : bool = Depends(role_checker)
) :
    return user
    
@auth_router.get('/logout')
async def revoke_token(token_details : dict = Depends(AccessTokenBearer())) :
    
    jti = token_details['jti']

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={"message" : "Logged out successfully"},
        status_code=status.HTTP_200_OK
    )



    
    
 