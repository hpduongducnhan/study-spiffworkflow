# -*- coding: utf-8 -*-
import asyncio
from typing import Any, Optional

from motor.motor_asyncio import AsyncIOMotorClient
from taskiq import AsyncResultBackend, TaskiqResult

# Backend tùy chỉnh cho MongoDB


class MongoDBResultBackend(AsyncResultBackend):
    def __init__(self, mongo_url: str, database: str, collection: str):
        self.mongo_url = mongo_url
        self.database = database
        self.collection = collection
        self.client = None
        self.db = None

    async def startup(self) -> None:
        """Khởi tạo kết nối tới MongoDB."""
        self.client = AsyncIOMotorClient(self.mongo_url)
        self.db = self.client[self.database]
        self.collection_obj = self.db[self.collection]

    async def shutdown(self) -> None:
        """Đóng kết nối MongoDB."""
        if self.client:
            self.client.close()

    async def set_result(self, task_id: str, result: TaskiqResult[Any]) -> None:
        """Lưu kết quả vào MongoDB."""
        await self.collection_obj.update_one(
            {"task_id": task_id},
            {
                "$set": {
                    "task_id": task_id,
                    "result": result.return_value,
                    "success": not result.is_err,
                    "error": str(result.error) if result.error else None,
                    "execution_time": result.execution_time if result.execution_time is not None else 0.0,
                    "labels": result.labels if result.labels is not None else {},
                    "timestamp": asyncio.get_event_loop().time(),
                }
            },
            upsert=True,
        )

    async def get_result(self, task_id: str, with_logs: bool = False) -> Optional[TaskiqResult[Any]]:
        """Lấy kết quả từ MongoDB."""
        doc = await self.collection_obj.find_one({"task_id": task_id})
        if doc:
            return TaskiqResult(
                return_value=doc.get("result"),
                is_err=not doc.get("success", True),
                error=doc.get("error"),
                log=doc.get("log"),
                execution_time=doc.get("execution_time", 0.0),
                labels=doc.get("labels", {}),
            )
        return None

    async def is_result_ready(self, task_id: str) -> bool:
        """Kiểm tra xem kết quả đã sẵn sàng chưa."""
        doc = await self.collection_obj.find_one({"task_id": task_id})
        return doc is not None
