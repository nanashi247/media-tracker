from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_username: str
    database_password: str
    database_name: str
    database_port: str
    database_hostname: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    TMDB_API_KEY: str

    class Config():
        env_file = ".env"

settings = Settings()


