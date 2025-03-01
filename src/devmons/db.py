from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from devmons.settings import BACKEND_DB_URL

engine = create_engine(BACKEND_DB_URL, echo=False)

Session = sessionmaker(engine)


def get_session():
    with Session() as session:
        yield session
