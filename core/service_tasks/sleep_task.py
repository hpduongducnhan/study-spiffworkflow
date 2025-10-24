import asyncio
import random
from .base import BaseServiceTask


class SleepTask(BaseServiceTask):
    task_name = "Sleep Task"
    task_type = "system"
    task_sub_type = "sleep"

    async def _execute(self, duration: float=random.uniform(0.5, 2.0), **kwargs):
        await asyncio.sleep(duration)
        return f"Slept for {duration} seconds."