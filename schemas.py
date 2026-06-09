from pydantic import BaseModel, EmailStr, Field


# USER SIGNUP SCHEMA
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


# USER LOGIN SCHEMA
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# RESPONSE SCHEMA
class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True