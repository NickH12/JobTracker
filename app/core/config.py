from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Job Application Tracker"
    app_env: str = "development"
    app_debug: bool = True

    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str # required field, no default value for Fast Fail
    db_user: str # required field, no default value
    db_password: str # required field, no default value

    jwt_secret_key: str # required field, no default value
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    @property
    def database_url(self) -> str:
        return f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

settings = Settings()