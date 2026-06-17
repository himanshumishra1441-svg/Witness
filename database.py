import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:Witness%40123@localhost:5432/Witness"
)

engine = create_engine(DATABASE_URL)

try:
    with engine.connect():
        print("Connected successfully!")
except Exception as e:
    print(e)