from dotenv import load_dotenv
import os

load_dotenv()

# credentital info for jwt encode and decode
JWT_ACCOUNT_PASSWORD = os.getenv("JWT_ACCOUNT_PASSWORD")
JWT_ACCOUNT_HASHALGO = os.getenv("JWT_ACCOUNT_HASHALGO")


