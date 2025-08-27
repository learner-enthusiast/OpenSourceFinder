import os
from dotenv import load_dotenv
from prisma import Prisma

load_dotenv()
DATABASE_URL=os.getenv('DATABASE_URL')

if not DATABASE_URL:
    raise ValueError("Database-URL not set in env")

db=Prisma()