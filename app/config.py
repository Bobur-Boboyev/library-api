from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_name: str

    class Config:
        env_file = ".env"


settings = Settings()
