from datetime import datetime, timedelta, timezone
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from share_files.db.models import UserModel
from share_files.schemas import User
from decouple import config
from passlib.context import CryptContext
from jose import jwt,JWTError

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
crypt_contect = CryptContext(schemes=['sha256_crypt'])

class UserUseCases:
    def __init__(self,db_session : Session):
        self.db_session = db_session
    
    
    def user_register(self,user: User):
        user_model = UserModel(
            username=user.username,
            password=crypt_contect.hash(user.password)
        )
        try:
            self.db_session.add(user_model)
            self.db_session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User already exists'
            )

    def user_login(self, user: User, expires_in: int= 30 ):
        user_on_db = self.db_session.query(UserModel).filter_by(username=user.username).first()
        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid username or password'
            )
        if not crypt_contect.verify(user.password, user_on_db.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid username or password'
            )
        
        exp = datetime.now(timezone.utc) + timedelta(minutes=expires_in)
    

        payload={
            'sub': user.username,
            'exp':exp
        }

        access_token = jwt.encode(payload,SECRET_KEY,ALGORITHM)

        return {
            'access_toke': access_token,
            'exp': exp.isoformat()
        }
    
    def verify_token(self, acess_token):
        try:
            data = jwt.decode(acess_token,SECRET_KEY,algorithms=[ALGORITHM])
        except JWTError:
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid access token'
            )
        
        user_on_db = self.db_session.query(UserModel).filter_by(username=data['sub']).first()

        if user_on_db is None:
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid access token'
            )


        