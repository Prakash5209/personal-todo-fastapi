from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
import datetime
import re
import jwt


from config import JWT_ACCOUNT_PASSWORD,JWT_ACCOUNT_HASHALGO
from database import db_dependency
from app.account.schemas import Account_creation_schema,UpdateEmailSchema,GetTokenSchema
from app.account.services.account_service import AccountCreate,GetToken,UpdateEmail


router = APIRouter()


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_valid_password(password):
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*\W).{5,10}$"
    return re.match(pattern, password) is not None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def parse_token(token: Annotated[str,Depends(oauth2_scheme)]) -> dict:
    payload = jwt.decode(token,JWT_ACCOUNT_PASSWORD,algorithms=[JWT_ACCOUNT_HASHALGO])
    d = payload
    print("payload",d)
    timestamp_to_utc = datetime.datetime.utcfromtimestamp(d.get("exp"))
    now = datetime.datetime.utcnow().replace(tzinfo=None)
    print("now",now)
    print("timestamp_to_utc",timestamp_to_utc)
    if timestamp_to_utc < now:
        raise HTTPException(status_code=401,detail="token expired or invalid")

    return payload



@router.post("/get-token")
def get_token(schema: GetTokenSchema,db: db_dependency):
    df = GetToken(schema.email,schema.password,db=db)
    to_dict = df.to_dict()
    return to_dict

@router.post("/create-account")
def create_account(schema: Account_creation_schema,db: db_dependency):
    accountcreate_obj = AccountCreate(schema = schema, db = db)
    value = accountcreate_obj.create_account()
    return value

@router.post("/update-email")
def update_email(schema: UpdateEmailSchema,db: db_dependency, payload:dict = Depends(parse_token)):
    obj = UpdateEmail(data = payload,schema = schema,db = db)
    update_email = obj.updateEmail()
    return update_email

