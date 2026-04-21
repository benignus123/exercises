from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5433
    DB_USER: str = 'postgres'
    DB_PASS: str = '1234'
    DB_NAME: str = 'postgres'
    
    @property
    def DATABASE_URL_psycopg(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
setting = Settings()

SECRET_KEY = "GSJGS"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30