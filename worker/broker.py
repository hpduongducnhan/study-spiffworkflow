# -*- coding: utf-8 -*-
import os
from configs import env
from taskiq import AsyncBroker, TaskiqEvents, TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_aio_pika import AioPikaBroker
from taskiq_redis import RedisScheduleSource
from .result_backend import MongoDBResultBackend

result_backend = MongoDBResultBackend(
    mongo_url=env.MONGO_URL, 
    database=env.MONGO_DB_NAME, 
    collection='TaskIqResults'
)


tiq_broker: AsyncBroker = AioPikaBroker(
    url=env.RBMQ_URL,
    qos=env.RBMQ_CONSUMER_PREFETCH_COUNT,
    queue_name=env.RBMQ_TASKIQ_QUEUE_NAME,
    exchange_name=env.RBMQ_TASKIQ_EXCHANGE_NAME,
).with_result_backend(result_backend)


