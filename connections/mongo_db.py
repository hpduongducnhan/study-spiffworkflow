# -*- coding: utf-8 -*-
import asyncio
from configs import env
from motor.motor_asyncio import AsyncIOMotorClient
from umongo.frameworks import MotorAsyncIOInstance


def get_umongo_instance(mongo_uri: str, db_name: str):
    """
    Create an instance of mongo db to register model

    Args:
        mongo_uri (str): MongoDb URI for connection.
        db_name (str): Name of the database will be used.

    Returns:
        MotorAsyncIOInstance: implementation for motor-asyncio
    """
    motor_client = AsyncIOMotorClient(mongo_uri)[db_name]
    motor_client.get_io_loop = asyncio.get_running_loop
    instance = MotorAsyncIOInstance(motor_client)
    return instance

db_conn = get_umongo_instance(env.MONGO_URL, env.MONGO_DB_NAME)