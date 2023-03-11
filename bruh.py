import os 
from dotenv import load_dotenv

load_dotenv()
#print all environment variables from .env file
print(os.environ["from_number"])
print(os.environ["to_number"])
print(os.environ["account_sid"])
print(os.environ["auth_token"])


