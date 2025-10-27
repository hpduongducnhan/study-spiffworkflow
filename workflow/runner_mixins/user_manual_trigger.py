from typing import Dict


class UserManualTaskTriggerMixin:
    async def trigger_user_manual_task(self, wf_id: str, task_id: str, data: Dict = {}, **kwargs):
        wf: BpmnWorkflow = await self._load_workflow_from_id(wf_id, **kwargs)
        updated_tasks: Dict = await self._trigger_user_manual_task_in_workflow(wf, task_id, data=data, **kwargs)
        return wf, updated_tasks