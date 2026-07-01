from pwdlib import PasswordHash
from datetime import timedelta, datetime, timezone
import jwt
from src.config import Config
import uuid
import logging

password_hash = PasswordHash.recommended()

ACCESS_TOKEN_EXPIRY = timedelta(hours=1)

class HashHelper:
    @staticmethod
    def hash_password(password: str) -> str:
        return password_hash.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return password_hash.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(user_data : dict, expiry : timedelta = None, refresh : bool = False) :
        
        expire = datetime.now(timezone.utc) + (expiry if expiry else ACCESS_TOKEN_EXPIRY)
        payload = {
            "sub" : str(user_data["uid"]),
            "exp" : expire,
            "jti" : str(uuid.uuid4()),
            "refresh" : refresh
        }

        # payload["user_data"] = user_data
        # payload["exp"] = datetime.now(timezone.utc) + (expiry if expiry else ACCESS_TOKEN_EXPIRY)
        # payload["jti"] = str(uuid.uuid4())
        # payload["refresh"] = refresh

        token = jwt.encode(
            payload=payload ,
            key=Config.JWT_SECRET ,
            algorithm=Config.JWT_ALGO
        )

        return token
    
    @staticmethod
    def decode_token(token : str) -> dict :
        try :
            token_data = jwt.decode(
                jwt=token ,
                key=Config.JWT_SECRET ,
                algorithms=[Config.JWT_ALGO]
            )
            return token_data
        
        except jwt.PyJWTError as e :
            logging.exception(e)
            return None
