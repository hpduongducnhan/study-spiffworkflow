import uuid
from typing import Dict, Tuple, Optional
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow
from SpiffWorkflow.bpmn.specs import BpmnTaskSpec
from SpiffWorkflow.bpmn.specs.defaults import UserTask, ManualTask
from SpiffWorkflow.task import Task
from .storage import BaseStorage
from .runner_mixins import BpmnParserMixin, RunnerTaskMixin, SerializerMixin

class WorkflowRunner(
    SerializerMixin, 
    BpmnParserMixin,
    RunnerTaskMixin
):
    def __init__(self):
        self._validated: bool = False
        self._storage: BaseStorage = None

    def validate(self):
        # ensure run this before running workflow
        if not self._storage:
            raise ValueError("Storage is not set. Please set storage before running workflow.")
        
        self._validated = True

    @property
    def validated(self) -> bool:
        return self._validated

    @property
    def storage(self) -> BaseStorage:
        return self._storage
    
    def set_storage(self, storage: BaseStorage):
        if not isinstance(storage, BaseStorage):
            raise ValueError("Storage must be an instance of BaseStorage.")
        self._storage = storage
    
    
    async def _load_workflow_from_configuration(self, wf_config_id: str, **kwargs) -> Tuple[str, str, BpmnWorkflow]:
        wf_config_model = await self._storage.load_workflow_from_configuration(wf_config_id, **kwargs)
        bpmn_parser = self.parse_bpmn(await wf_config_model.get_workflow_config())
        main_spec = self._get_main_spec(bpmn_parser)    # get main process spec
        workflow = BpmnWorkflow(main_spec)              # create new BpmnWorkflow object
        return await wf_config_model.get_workflow_id(), wf_config_id, workflow

    async def _list_all_tasks_of_workflow(self, workflow: BpmnWorkflow, need_task_id: str=None):
        all_tasks = workflow.get_tasks()
        print('need_task_id:', need_task_id)
        for task in all_tasks:
            task_spec: BpmnTaskSpec = task.task_spec
            print(f' Task state: {task.state}, id: {task.id}[{type(task.id)}], is manual: {task_spec.manual}, task type: {type(task_spec)} ')
            if need_task_id and task.id == need_task_id:
                print(f'  >> Found needed task id: {need_task_id} ')
        return all_tasks
    
    async def _load_workflow(
        self, 
        wf_id: str=None,  
        wf_config_id: str=None, 
        data: Dict = {}, 
        **kwargs
    ) -> Tuple[str, str, BpmnWorkflow]:
        workflow: BpmnWorkflow = None

        # start new workflow
        if not wf_id and wf_config_id:
            return await self._load_workflow_from_configuration(wf_config_id, **kwargs)
        
        # resume existing workflow
        if wf_id: 
            wf_config_model = await self._storage.load_workflow_runtime_state(wf_id, **kwargs)
            wf_state = await wf_config_model.get_workflow_state()
            if wf_state:
                # deserialize workflow, create BpmnWorkflow object
                # TODO: should load workflow data when deserializing
                #       should add event listeners after deserializing
                return wf_id, wf_config_id, self._deserialize_workflow(wf_state)
            else:
                # maybe workflow is created from API but not run yet
                # in this case, we need to load from configuration
                return await self._load_workflow_from_configuration(wf_config_id, **kwargs)    

    async def _convert_task_id(self, task_id: Optional[str | uuid.UUID]) -> uuid.UUID:
        if not task_id:
            return None
        if isinstance(task_id, uuid.UUID):
            return task_id
        try:
            return uuid.UUID(task_id)
        except ValueError:
            raise ValueError(f"Invalid task_id format: {task_id}. Must be a valid UUID string or UUID object.")

    async def _run_workflow(
        self, 
        wf_id: str=None, 
        wf_config_id: str=None, 
        wf_data: Dict={}, 
        task_id: Optional[str | uuid.UUID]=None,  # to run specific user task / manual task
        task_data: Dict={}, # data for specific task
        **kwargs
    ):
        if not wf_id and not wf_config_id:
            raise ValueError("Either wf_id or wf_config_id must be provided to run a workflow.")

        # convert task id to UUID, becasuse SpiffWorkflow use UUID for task id
        task_id = await self._convert_task_id(task_id)
        # ensure task_data is dict if task_id is provided
        if task_id and not isinstance(task_data, dict):
            raise ValueError("task_data must be a dictionary if task_id is provided.")

        # should add try/except here
        wf_id, wf_config_id, workflow = await self._load_workflow(wf_id=wf_id, wf_config_id=wf_config_id, **kwargs)

        if task_id:
            workflow.do_engine_steps()  # ensure workflow is up-to-date
            await self._list_all_tasks_of_workflow(workflow, need_task_id=task_id)

            task: Task = workflow.get_task_from_id(task_id)
            if not task:
                raise ValueError(f"Task with id {task_id} not found in workflow {wf_id}.")
            
            task_spec: BpmnTaskSpec = task.task_spec
            if not isinstance(task_spec, (UserTask, ManualTask, )):
                raise ValueError(f"Task with id {task_id} is not a userTask or manualTask.")

            # set task data if provided
            if task_data:
                task.set_data(**task_data)

            # mark task as ready
            task.complete()

            # refresh waiting tasks
            workflow.refresh_waiting_tasks()


        workflow = await self._run_all_available_tasks_and_events(workflow, **kwargs)
        
        # always save snapshot after running
        await self._storage.save_workflow_runtime_state(
            wf_id=wf_id, 
            state=self._serialize_workflow(workflow),
            is_completed=workflow.is_completed()
        )
        return workflow

    async def run(self, wf_id: str=None,  wf_config_id: str=None, data: Dict={}, **kwargs):
        if not self.validated:
            raise ValueError("WorkflowRunner is not validated. Please call validate() before running workflow.")

        # should add global lock here for workflow instance to ensure no concurrent runs
        try:
            return await self._run_workflow(wf_id=wf_id, wf_config_id=wf_config_id, data=data, **kwargs)
        except Exception as e:
            # print("Error running workflow:", str(e))
            raise e
