# DB connection setup
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")

if __name__ == "__main__":
    try:
        print("Success")
    except Exception as ex:
        print("Error: \n", ex)


def get_session():
    with Session(engine) as session:
        yield session
