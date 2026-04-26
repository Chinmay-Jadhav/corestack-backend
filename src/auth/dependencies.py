from fastapi.security import HTTPBearer
from fastapi import Request, status
from fastapi.exceptions import HTTPException

from src.auth.utils import HashHelper
from src.db.redis import token_in_blocklist

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