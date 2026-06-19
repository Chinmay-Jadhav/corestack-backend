from fastapi.security import HTTPBearer
from fastapi import Request, status, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Any

from src.auth.utils import HashHelper
from src.db.redis import token_in_blocklist
from src.db.main import get_session
from .service import UserService
from src.db.models import User

user_service = UserService()

class TokenBearer(HTTPBearer) :

    
    def __init__(self, *, bearerFormat = None, scheme_name = None, description = None, auto_error = True):
        super().__init__(bearerFormat=bearerFormat, scheme_name=scheme_name, description=description, auto_error=auto_error)

    async def __call__(self, request : Request):
        creds =  await super().__call__(request)

        # print(creds.scheme)
        # print(creds.credentials)

        token = creds.credentials
        token_data = HashHelper.decode_token(token)

        if not self.token_valid(token) :
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail={
                    "error" : "This token is invalid or expired.",
                    "resolution" : "Please get new token."
                     }
                     )
        
        if await token_in_blocklist(token_data['jti']) :
             raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                     "error" : "This token is invalid or has been revoked.",
                     "resolution" : "Please get new token"
                     }
                  )
        
        # if token_data['refresh'] :
        #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide an access token")

        self.verify_token_data(token_data)

        return token_data
    
    def token_valid(self, token : str) -> bool :

        token_data = HashHelper.decode_token(token=token)

        if token_data is not None : 
            return True
        else :
            return False
        
    def verify_token_data(self, token_data) :
         raise NotImplementedError("Please override this method in child classes")

class AccessTokenBearer(TokenBearer) :
    
    def verify_token_data(self, token_data : dict) -> None :
        if token_data and token_data['refresh'] :
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide an access token")

class RefreshTokenBearer(TokenBearer) :
    
    def verify_token_data(self, token_data : dict) -> None :
        if token_data and not token_data['refresh'] :
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide a refresh token")
        

async def get_current_user(
        token_details : dict = Depends(AccessTokenBearer()), 
        session : AsyncSession = Depends(get_session) 
        ) :
     
     user_id = token_details['sub']

     user = await user_service.get_user_by_id(user_id, session)

     return user


class RoleChecker :

    def __init__(self, allowed_roles : List[str]) -> None :
          
          self.allowed_roles = allowed_roles

    def __call__(self, current_user : User = Depends(get_current_user)) -> Any :

        if current_user.role in self.allowed_roles :
              return True
         
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource"
            ) 
          
          
          
    

































