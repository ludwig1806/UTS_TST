from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Alexander Ludwig Agu",
                "email": "18219033@std.stei.itb.ac.id",
                "password": "Password lemah"
            }
        }

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "18219033@std.stei.itb.ac.id",
                "password": "Password lemah"
            }
        }

