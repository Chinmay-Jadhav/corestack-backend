from src.db.models import User
from .schemas import UserCreateModel
from .utils import HashHelper
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select


class UserService :
    async def get_user_by_email(self, email : str, session : AsyncSession) :
        statement = select(User).where(User.email == email)

        result = await session.exec(statement)

        user = result.first()

        return user
    
    async def get_user_by_id(self, user_id : str, session : AsyncSession) :
        statement = select(User).where(User.uid == user_id)

        result = await session.exec(statement)

        return result.first()
    
    async def user_exists(self, email : str, session : AsyncSession) :
        user = await self.get_user_by_email(email, session)

        return True if user is not None else False
    
    async def create_user(self, user_data : UserCreateModel, session : AsyncSession) :

        user_data_dict = user_data.model_dump()
        
        password = user_data_dict.pop("password")

        new_user = User(**user_data_dict)

        new_user.password_hash = HashHelper.hash_password(password)
        new_user.role = "user"

        session.add(new_user)

        await session.commit()
        await session.refresh(new_user)

        return new_user



        
