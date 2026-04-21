from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine, String
from config import setting
from typing import Annotated
from fastapi.security import HTTPBearer


sync_engine = create_engine(
    url=setting.DATABASE_URL_psycopg,
    echo=True,
    pool_size=5,
    max_overflow=10
)


session_factory = sessionmaker(sync_engine)

str_256 = Annotated[str,256]

class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }
    
    def __repr__(self):
        cols = []
        for col in self.__table__.columns.keys():
            cols.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.__name__} {','.join(cols)}>"
    
def get_session():
    with session_factory() as session:
        yield session
        
security = HTTPBearer()