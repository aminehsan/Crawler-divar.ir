from pydantic_settings import BaseSettings


class ServiceSettings(BaseSettings):
    name: str

    class Config:
        env_prefix = 'SERVICE_'


class BrokerSettings(BaseSettings):
    host: str
    port: int
    username: str
    password: str

    class Config:
        env_prefix = 'BROKER_'


class StorageSettings(BaseSettings):
    host: str
    port: int
    password: str

    class Config:
        env_prefix = 'STORAGE_'


service = ServiceSettings()
broker = BrokerSettings()
storage = StorageSettings()
