from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:Witness%40123@localhost:5432/Witness"

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print("Connected successfully!")
except Exception as e:
    print(e)