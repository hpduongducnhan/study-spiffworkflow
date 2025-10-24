from typing import Dict, Type
from SpiffWorkflow.bpmn.specs.defaults import ServiceTask
from .base import BaseServiceTask
from .sleep_task import SleepTask


class ServiceTaskManager:
    def __init__(self):
        self.service_tasks: Dict[str, BaseServiceTask] = {}
        self.sleep_task: SleepTask = None

    def register_handler(self, task_cls: Type[BaseServiceTask]) -> None:
        instance = task_cls()
        instance.verify()
        instance.set_manager(self)
        self.service_tasks[instance.service_task_id] = instance
        if isinstance(instance, SleepTask):
            self.sleep_task = instance

    def get_sleep_task(self) -> SleepTask | None:
        return self.sleep_task

    def get_handler(self, service_task_id: str) -> BaseServiceTask | None:
        return self.service_tasks.get(service_task_id)

    def remove_handler(self, service_task_id: str) -> None:
        if service_task_id in self.service_tasks:
            del self.service_tasks[service_task_id]

    async def run_task(self, task: ServiceTask, *args,  **kwargs) -> any:
        if not isinstance(task, ServiceTask):
            raise ValueError("The provided task is not a ServiceTask instance.")
        handler = self.get_sleep_task()
        return await handler.execute(*args, **kwargs)


service_task_manager = ServiceTaskManager()
for task_handler_cls in (
    SleepTask,
):    
    service_task_manager.register_handler(task_handler_cls)