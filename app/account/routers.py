from fastapi import APIRouter,Depends

from database import db_dependency
from app.account.schemas import Account_creation_schema, EmailOnlySchema,GetTokenSchema
from app.account.services.account_service import AccountCreate,GetToken,UpdateEmail
from app.tokenparser import parse_token


router = APIRouter()

# get the access jwt token using email and password
@router.post("/get-token")
def get_token(schema: GetTokenSchema,db: db_dependency):
    df = GetToken(schema,db=db)
    to_dict = df.to_dict()
    return to_dict

# creation of new account
@router.post("/create-account",response_model=EmailOnlySchema)
def create_account(schema: Account_creation_schema,db: db_dependency):
    accountcreate_obj = AccountCreate(schema = schema, db = db)
    value = accountcreate_obj.create_account()
    return value


# update the email, jwt token needed
@router.put("/update-email",response_model=EmailOnlySchema)
def update_email(schema: EmailOnlySchema,db: db_dependency, payload:dict = Depends(parse_token)):
    obj = UpdateEmail(data = payload,schema = schema,db = db)
    update_email = obj.updateEmail()
    return update_email

