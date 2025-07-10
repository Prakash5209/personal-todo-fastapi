from dotenv import load_dotenv
import os


load_dotenv()

JWT_ACCOUNT_PASSWORD = os.getenv("JWT_ACCOUNT_PASSWORD")
JWT_ACCOUNT_HASHALGO = os.getenv("JWT_ACCOUNT_HASHALGO")


