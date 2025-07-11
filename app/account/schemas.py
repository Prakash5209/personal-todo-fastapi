from pydantic import BaseModel


# validation for Account creation
class Account_creation_schema(BaseModel):
    full_name: str
    email: str
    password: str


# used by /create-account (response_model) and /update-email (validation)
class EmailOnlySchema(BaseModel):
    email: str


# validation for generating jwt 
class GetTokenSchema(BaseModel):
    email: str
    password: str
