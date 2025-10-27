# -*- coding: utf-8 -*-
from typing import Optional


from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Application Info
    APP_NAME: Optional[str] = "EmBpmn"
    APP_DESCRIPTION: Optional[str] = "SCC AutoFlow system"
    APP_VERSION: Optional[str] = "0.1.0"

    # Debugging, Logging
    DEBUG: Optional[bool] = False
    LOG_FORMAT: Optional[str] = "json"
    LOGGER_FILE: Optional[str] = None

    # OpenTelemetry
    OTEL_ENABLE: Optional[bool] = False
    OTEL_ENDPOINT: Optional[str] = "http://otel-collector-hni01.ftel.scc/v1/traces"
    OTEL_SERVICE_NAME: Optional[str] = "EmBpmn-Service"
    OTEL_ENVIRONMENT: Optional[str] = "dev"


    # RabbitMQ configuration
    RBMQ_URL: Optional[str] = "amqp://username:password@localhost:5672,localhost:5673/"
    RBMQ_CONSUMER_PREFETCH_COUNT: Optional[int] = 20
    RBMQ_CONSUMER_HOST: Optional[str] = "0.0.0.0"
    RBMQ_CONSUMER_PORT: Optional[int] = 6002

    # MongoDB configuration
    MONGO_URL: Optional[str] = "mongodb://localhost:27017"
    MONGO_DB_NAME: Optional[str] = "EmBpmn"

    # Redis configuration
    REDIS_URL: Optional[str] = "redis://:password@localhost:6379/0"

    # discord general notification
    DISCORD_TOKEN: Optional[str] = None
    DISCORD_CHANNEL_ID: Optional[str] = None
    DISCORD_PROXY: Optional[str] = "http://proxy.hcm.fpt.vn:80"


    def post_setup(self):
        if self.DEBUG:
            ...


env = EnvSettings()
env.post_setup()
# print(f"Environment settings loaded: {env.model_dump()}")