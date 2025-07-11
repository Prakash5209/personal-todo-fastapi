from fastapi import HTTPException,status
from fastapi.responses import JSONResponse
import datetime
import bcrypt
import re
import jwt


from app.account.models import UserModel
from config import JWT_ACCOUNT_PASSWORD,JWT_ACCOUNT_HASHALGO


# regex to validate email
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$' # eg: test@gmail.com
    return re.match(pattern, email) is not None


# regex to validate password
def is_valid_password(password):
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*\W).{5,10}$" # must have atleast 1 number, special charactr like "@", uppercase and lowercase. length >= 5 & <= 10
    return re.match(pattern, password) is not None


# function to hash password using bcrypt
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("UTF-8"),salt)
    result = hashed.decode("UTF-8")
    return result


# check password. params: plain_password and hashed password
def checkhash_password(plain_password: str,hashed_password: str) -> bool:
    result = bcrypt.checkpw(plain_password.encode("UTF-8"),hashed_password.encode("UTF-8"))
    return result


# this class is used by: localhost:8000/get-token
class GetToken:
    def __init__(self,schema,db):
        self.schema = schema
        self.db = db
        self.__jwt: str # private
        self.stmt = None


        # filter by email , first()
        try:
            stmt = self.db.query(UserModel).filter(UserModel.email == self.schema.email).one()
            self.stmt = stmt
        except Exception as e:
            raise HTTPException(status_code=500,detail="user not found")

            # creating data/ payload for the jwt creation
        if checkhash_password(self.schema.password,self.stmt.password):
            payload = {}
            payload["id"] = self.stmt.id
            payload["email"] = self.stmt.email
            payload["exp"] = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours = 5) # alive time 5 hour
            print("payload",payload)
            encoded_jwt = jwt.encode(payload,JWT_ACCOUNT_PASSWORD,algorithm=JWT_ACCOUNT_HASHALGO)
            print("encoded_jwt",encoded_jwt)
            self.__jwt = encoded_jwt
        else:
            raise HTTPException(status_code=400,detail="password didn't match")

    def to_dict(self):
        return {"token":self.__jwt}



# this class is used by: localhost:8000/create-account
class AccountCreate:
    def __init__(self,schema,db):
        self.schema = schema
        self.db = db


    def create_account(self):

        # removing/striping the whitespace at first and last
        full_name = self.schema.full_name.strip()
        email = self.schema.email.strip()
        raw_password = self.schema.password.strip()


        # checking if email and password is valid
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

        # creating new model object -an instance of the UserModel
        new_account = UserModel(full_name = full_name,email = email, password=password)
        self.db.add(new_account) # adding instance to session
        try:
            self.db.commit() # execute / make changes
            self.db.refresh(new_account) # refresh value with updated one from the DB
            # return dict(status_code=201,content="email created")
            return new_account

        except Exception as e:
            print(e)
            self.db.rollback() # rolling back if anything goes wrong
            raise HTTPException(status_code=409,detail="email already exist")




class UpdateEmail:
    """
    jwt token is must for the email update
    """
    def __init__(self,schema,data: dict,db):
        self.payload = data
        self.schema = schema
        self.db = db

    def updateEmail(self):

        # query to locate user instance using jwt token payload
        that_user = self.db.query(UserModel).where(UserModel.email == self.payload.get("email")).first()
        if not that_user:
            raise HTTPException(status_code=404,detail="user not found")

        # update email when email is valid
        if is_valid_email(self.schema.email):
            that_user.email = self.schema.email
            self.db.commit()
            self.db.refresh(that_user)
            # return that_user
            return JSONResponse(
                status_code=status.HTTP_200_OK, content={
                    "message": "Email updated successfully.",
                    "warning": "Please get a new JWT token due to change in email.",
                    "updated_email": that_user.email
                }
            )
        else:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,detail="invalid email")
    def __str__(self):
        return str(self.payload)



class DeleteUser:
    """
    this is just for clearing the database to test.

    created to clear the database user and it's tasks (childs)

    warning: simply putting id will delete the user and it's task (child)
    """
    def __init__(self,id,db):
        self.id = id
        self.db = db

    def userdelete(self):
        that_user = self.db.query(UserModel).get(self.id)
        if not that_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user not found"
                )
        self.db.delete(that_user)
        self.db.commit()
        return {"status": 200, "message": "User deleted successfully"}
