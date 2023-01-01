from ipaddress import IPv4Address
from os import getenv
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, validator

load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = "Varla-Orchestrator"

    ORCHESTRATOR_HOST: str
    ORCHESTRATOR_PORT: int

    SERVICES_CONFIG_PATH: str

    NOTIFICATION_CORE_URL: Optional[str]
    DEFAULT_CHANNEL: Optional[str]

    @validator("ORCHESTRATOR_PORT", always=True)
    def orchestrator_port_validator(cls, v):
        return int(getenv("ORCHESTRATOR_PORT"))

    @validator("ORCHESTRATOR_HOST", always=True)
    def orchestrator_host_validator(cls, v):
        return str(IPv4Address(getenv("ORCHESTRATOR_HOST")))

    @validator("SERVICES_CONFIG_PATH", always=True)
    def services_config_path_validator(cls, v):
        return getenv("SERVICES_CONFIG_PATH")

    @validator("NOTIFICATION_CORE_URL", always=True)
    def notification_core_url_validator(cls, v):
        return getenv("NOTIFICATION_CORE_URL")

    @validator("DEFAULT_CHANNEL", always=True)
    def default_channel_validator(cls, v):
        return getenv("DEFAULT_CHANNEL")


settings = Settings()
