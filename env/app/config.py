from pydantic_settings import BaseSettings
# pydantic will auto convert those var to uppercase
class Settings(BaseSettings):
    database_hostname: str
    database_password:str
    database_port:str
    database_name:str
    database_username:str
    secret_key:str
    algorithm:str
    access_token_expire_minutes:int

    class Config:
        env_file=".env"


settings=Settings()