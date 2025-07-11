from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
import datetime
import jwt

# importing jwt conversion creatential data
from config import JWT_ACCOUNT_PASSWORD,JWT_ACCOUNT_HASHALGO

# always loook for token in header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# decode the jwt token back to payload/data
def parse_token(token: Annotated[str,Depends(oauth2_scheme)]) -> dict:
    try:
        payload = jwt.decode(token, JWT_ACCOUNT_PASSWORD, algorithms=[JWT_ACCOUNT_HASHALGO])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

