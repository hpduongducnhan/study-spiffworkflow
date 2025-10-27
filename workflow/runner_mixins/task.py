import asyncio
import os   
import random
import httpx
from typing import List
from SpiffWorkflow.task import Task as SpiffTask
from SpiffWorkflow.bpmn.specs.defaults import ServiceTask
from SpiffWorkflow.util.task import TaskState
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow
from SpiffWorkflow.bpmn.specs.mixins.events.event_types import CatchingEvent

print('os proxy', os.environ.get('HTTP_PROXY'), os.environ.get('HTTPS_PROXY'))

httpx_client = httpx.AsyncClient(proxy=None)
manual_task_notification_url = "http://172.27.230.30:9002/api/manual_task"  # replace with actual URL


class RunnerTaskMixin:
    async def _run_service_task(self, task: SpiffTask, **kwargs):
        # TODO: for quickly loadtest, I random sleep here to simulate service task processing time
        # then complete the task
        # you should user scriptengine or custom task spec to implement your service task logic
        sleep_secs = random.uniform(0.1, 10)
        await asyncio.sleep(sleep_secs)
        task.complete()
        print(f'\t\t Service Task {task.id} - {kwargs.get("wf_id")} Completed in {sleep_secs:.2f} seconds.')

    async def _notify_manual_task_to_user(self, task: SpiffTask, **kwargs):
        # TODO: this logic for testing purpose onlye
        # I notify to other api, to sleep for a while, then that api will send to this service a message like user completed the task
        wf_id = kwargs.get("wf_id")
        res = await httpx_client.get(
            url=manual_task_notification_url,
            params={
                "t_id": str(task.id),
                "wf_id": wf_id,
            },
        )
        print(f'\t\t Manual Task {task.id}[{wf_id}] notified to user, response status: {res.status_code}')

    def _all_available_tasks(self, workflow: BpmnWorkflow) -> List[SpiffTask]:
        return workflow.get_tasks(state=TaskState.READY, manual=False)
    
    def _all_available_events(self, workflow: BpmnWorkflow) -> List[SpiffTask]:
        return workflow.get_tasks(state=TaskState.READY, spec_class=CatchingEvent)
    
    def _all_available_manual_tasks(self, workflow: BpmnWorkflow) -> List[SpiffTask]:
        return workflow.get_tasks(state=TaskState.READY, manual=True)

    async def _run_all_available_tasks_and_events(self, workflow: BpmnWorkflow, **kwargs):
        # run tasks which are not user/ manual tasks or event need to wait for external trigger
        tasks = self._all_available_tasks(workflow)
        while tasks:
            # TODO: should use gather here to run tasks concurrently
            # but run sequentially for now for simplicity
            for task in tasks:
                if isinstance(task.task_spec, (ServiceTask, )):
                    await self._run_service_task(task, **kwargs)
                    continue
                else:
                    result = task.run()
                    if not result:  # for testing, auto-complete tasks if no result
                        task.complete()
                # after running tasks, run events
                await self._run_ready_events(workflow)

            # re-check available tasks
            tasks = self._all_available_tasks(workflow)

        manual_tasks = self._all_available_manual_tasks(workflow)
        for manual_task in manual_tasks:
            # for loadtest purpose
            await self._notify_manual_task_to_user(manual_task, **kwargs)

        return workflow

    async def _run_ready_events(self, workflow: BpmnWorkflow):
        workflow.refresh_waiting_tasks()
        events = self._all_available_events(workflow)
        while events:
            for event in events:
                result = event.run()
                # for testing, auto-complete events if no result
                if not result:
                    event.complete()
            events = self._all_available_events(workflow)
