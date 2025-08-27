import os 
from dotenv import load_dotenv
from typing import List

load_dotenv()

class Settings:
    GOOGLE_CLIENT_ID=os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET=os.getenv("GOOGLE_CLIENT_SECRET")

    SECRET_KEY=os.getenv("SECRET_KEY")
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=60*24*7

    FRONTEND_URL=os.getenv("FRONTEND_URL")
    BACKEND_URL=os.getenv("BACKEND_URL")

    ENVIRONMENT=os.getenv("ENVIRONMENT","developement")

    @property
    def CORS_ORIGINS(self)->List[str]:
        if self.ENVIRONMENT=='production':
            return[
                self.FRONTEND_URL
            ]
        else:
            return [
                self.FRONTEND_URL,self.BACKEND_URL
            ]
settings=Settings()