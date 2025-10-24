


class BaseServiceTask:
    manager: 'ServiceTaskManager' = None  # type: ignore
    task_name: str 
    task_type: str
    task_sub_type: str

    def verify(self):
        # print('Verifying service task:', self.task_name, self.task_type, self.task_sub_type)
        if (not self.task_name or 
            not self.task_type or 
            not self.task_sub_type):
            raise ValueError("Service Task must have name, type and sub_type defined.")

    async def _execute(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement this method.")
    
    @property
    def service_task_id(self):
        return f"[{self.task_type}.{self.task_sub_type}] - {self.task_name}"

    def set_manager(self, manager: 'ServiceTaskManager'):
        self.manager = manager

    async def execute(self, *args, **kwargs):
        # may be retry from here
        try:
            return await self._execute(*args, **kwargs)
        except Exception as e:
            print(f"Error executing service task {self.task_name}: {e}")
            raise e