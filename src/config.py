from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv


class Settings(BaseSettings):
    postgres_database: str
    postgres_username: str
    postgres_password: SecretStr
    postgres_host: str
    postgres_port: str

    redis_host: str
    redis_port: int
    redis_index: str

    s3_access_key: SecretStr
    s3_secret_key: SecretStr
    s3_endpoint_url: str
    s3_bucket_name: str

    MEDIA_DIR: str = '../media'

    @property
    def DATABASE_URL(self):
        return (
            f"postgresql+asyncpg://{self.postgres_username}:{self.postgres_password.get_secret_value()}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_database}"
        )

    @property
    def REDIS_URL(self):
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_index}"

    model_config = SettingsConfigDict(env_file=find_dotenv(), env_file_encoding='utf-8')


settings = Settings()
