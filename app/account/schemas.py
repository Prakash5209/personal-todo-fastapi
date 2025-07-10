from pydantic import BaseModel

class Account_creation_schema(BaseModel):
    full_name: str
    email: str
    password: str


class UpdateEmailSchema(BaseModel):
    email: str

class GetTokenSchema(BaseModel):
    email: str
    password: str
