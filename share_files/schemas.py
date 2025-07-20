import re
from pydantic import BaseModel, field_validator
from email_validator import validate_email , EmailNotValidError   

class User(BaseModel):
    username: str
    password: str
    email: str 

    @field_validator('username')
    def validate_username(cls, value):
        if not re.match(r'^([a-z]|[0-9]|@)', value):
            raise ValueError('Username format invalid')
        return value
    
    @field_validator('email')
    def validate_email(cls, value):
        try:
            email_valid = validate_email(value)
            return email_valid.email
        except EmailNotValidError as e:
            raise ValueError('Email format invalid')
    

