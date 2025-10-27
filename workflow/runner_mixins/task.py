from typing import List
from SpiffWorkflow.task import Task as SpiffTask
from SpiffWorkflow.bpmn.specs.defaults import UserTask, ManualTask
from SpiffWorkflow.util.task import TaskState
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow
from SpiffWorkflow.bpmn.specs.mixins.events.event_types import CatchingEvent


class RunnerTaskMixin:
    def _all_available_tasks(self, workflow: BpmnWorkflow) -> List[SpiffTask]:
        return workflow.get_tasks(state=TaskState.READY, manual=False)
    
    def _all_available_events(self, workflow: BpmnWorkflow) -> List[SpiffTask]:
        return workflow.get_tasks(state=TaskState.READY, spec_class=CatchingEvent)
    
    def _all_available_manual_tasks(self, workflow: BpmnWorkflow) -> List[SpiffTask]:
        return workflow.get_tasks(state=TaskState.READY, manual=True)

    async def _run_all_available_tasks_and_events(self, workflow: BpmnWorkflow, **kwargs):
        # run tasks which are not user tasks
        tasks = self._all_available_tasks(workflow)
        while tasks:
            # TODO: should use gather here to run tasks concurrently
            # but run sequentially for now for simplicity
            for task in tasks:
                result = task.run()

                # for testing, auto-complete tasks if no result
                if not result:
                    task.complete()
                # after running tasks, run events
                await self._run_ready_events(workflow)

            # re-check available tasks
            tasks = self._all_available_tasks(workflow)

        manual_tasks = self._all_available_manual_tasks(workflow)
        print(f' Found {len(manual_tasks)} manual tasks remaining. ')
        for mt in manual_tasks:
            print(f'  - Manual Task: {mt}, is user task {isinstance(mt.task_spec, (UserTask, ))}, is manual task {isinstance(mt.task_spec, (ManualTask, ))}')
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
