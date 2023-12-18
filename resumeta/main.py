import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

API_HOST = os.environ.get("API_HOST")
API_PORT = os.environ.get("API_PORT")

if __name__ == "__main__":
    uvicorn.run("resumeta.api:app", host=API_HOST, port=int(API_PORT), reload=True)
