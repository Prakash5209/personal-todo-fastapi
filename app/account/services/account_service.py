from fastapi import HTTPException
import datetime
import bcrypt
import re
import jwt


from app.account.models import UserModel
from config import JWT_ACCOUNT_PASSWORD,JWT_ACCOUNT_HASHALGO


# helper functions 
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_valid_password(password):
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*\W).{5,10}$"
    return re.match(pattern, password) is not None


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("UTF-8"),salt)
    result = hashed.decode("UTF-8")
    return result

def checkhash_password(plain_password: str,hashed_password: str) -> bool:
    result = bcrypt.checkpw(plain_password.encode("UTF-8"),hashed_password.encode("UTF-8"))
    return result

class AccountCreate:
    def __init__(self,schema,db):
        self.schema = schema
        self.db = db

    def create_account(self):
        full_name = self.schema.full_name.strip()
        email = self.schema.email.strip()
        raw_password = self.schema.password.strip()

        is_email = is_valid_email(email=email)
        is_password = is_valid_password(password=raw_password)

        if not is_email:
            raise HTTPException(status_code=400, detail="email is invalid")

        if not is_password:
            raise HTTPException(status_code=400,detail="password is invalid")

        if not full_name:
            raise HTTPException(status_code=400,detail="full_name field is empty")

        # bcrypting password
        password = hash_password(password=raw_password)

        new_account = UserModel(full_name = full_name,email = email, password=password)
        self.db.add(new_account)
        try:
            self.db.commit()
            self.db.refresh(new_account)
            return dict(status_code=201,content="email created")
        except Exception as e:
            print(e)
            self.db.rollback()
            raise HTTPException(status_code=409,detail="email already exist")


class GetToken:
    def __init__(self,email,password,db):
        self.email = email
        self.password = password
        self.db = db
        self.__jwt: str


        stmt = self.db.query(UserModel).filter(
            UserModel.email == self.email
        ).first()

        
        if checkhash_password(self.password,stmt.password):
            payload = {}
            payload["id"] = stmt.id
            payload["email"] = stmt.email
            payload["exp"] = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours = 5)
            encoded_jwt = jwt.encode(payload,JWT_ACCOUNT_PASSWORD,algorithm=JWT_ACCOUNT_HASHALGO)
            self.__jwt = encoded_jwt

    def to_dict(self):
        return {"token":self.__jwt}


class UpdateEmail:
    """
    you can update email with token;
    """
    def __init__(self,schema,data: dict,db):
        self.payload = data
        self.schema = schema
        self.db = db

    def updateEmail(self):
        that_user = self.db.query(UserModel).where(UserModel.email == self.payload.get("email")).first()
        if not that_user:
            raise HTTPException(status_code=404,detail="user not found")

        if is_valid_email(self.schema.email):
            that_user.email = self.schema.email
            self.db.commit()
            self.db.refresh(that_user)
            return {
                "status":200,
                "content":"email updated successfully",
                "warning":"get new jwt token due to change in email"
            }
        
    def __str__(self):
        return str(self.payload)

    
