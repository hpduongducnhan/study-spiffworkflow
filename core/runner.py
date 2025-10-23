import os
from typing import Dict
from SpiffWorkflow.task import Task
from SpiffWorkflow.bpmn.specs import BpmnTaskSpec, BpmnProcessSpec
from SpiffWorkflow.bpmn.specs.mixins.events.event_types import CatchingEvent
from SpiffWorkflow.util.task import TaskState
from SpiffWorkflow.bpmn.parser import BpmnParser
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow
from SpiffWorkflow.bpmn.serializer import BpmnWorkflowSerializer
from SpiffWorkflow.bpmn.serializer.config import DEFAULT_CONFIG as SPIFF_CONFIG
from SpiffWorkflow.serializer.json import JSONSerializer, DictionarySerializer

from .storage import Storage
from .node_manager import NodeManager


class CoreRunner:
    def __init__(self, storage: Storage, node_manager: NodeManager):
        self.storage = storage
        self.node_manager = node_manager

    def _parse_bpmn(self, bpmn_file_content: str) -> BpmnParser:
        bpmn_parser = BpmnParser()
        bpmn_parser.add_bpmn_str(bpmn_file_content.encode("utf-8"))
        return bpmn_parser
    
    def _get_main_spec(self, bpmn_parser: BpmnParser):
        bpmn_specs = bpmn_parser.find_all_specs()
        main_process_id = list(bpmn_specs.keys())[0]
        main_spec = bpmn_specs[main_process_id]
        return main_spec

    def _show_info_tasks(self, tasks, prefix: str = ''):
        for task in tasks:
            task: Task
            task_spec: BpmnTaskSpec = task.task_spec
            print(f"{prefix}Task ID: {task.id}, Name: {task_spec.name}, State: {TaskState.get_name(task.state)}, Spec: {task_spec.task_info(task)}")

    def _show_wf_state(self, workflow: BpmnWorkflow):
        wf_spec: BpmnProcessSpec = workflow.spec
        print("Workflow Spec:", wf_spec)
        print("Workflow Is complete:", workflow.is_completed())
        ready_tasks = workflow.get_tasks(state=TaskState.READY)
        print("Ready Tasks:", len(ready_tasks))
        self._show_info_tasks(ready_tasks, '\t')
        waiting_tasks = workflow.get_tasks(state=TaskState.WAITING)
        print("Waiting Tasks:", len(waiting_tasks))
        self._show_info_tasks(waiting_tasks, '\t')
        
    def _wf_get_ready_waiting_tasks(self, workflow: BpmnWorkflow):
        ready_tasks = workflow.get_tasks(state=TaskState.READY)
        waiting_tasks = workflow.get_tasks(state=TaskState.WAITING)
        return ready_tasks, waiting_tasks

    def _wf_get_ready_auto_tasks(self, workflow: BpmnWorkflow):
        ready_auto_tasks = workflow.get_tasks(state=TaskState.READY, manual=False)
        return ready_auto_tasks
    
    def _wf_get_ready_event_tasks(self, workflow: BpmnWorkflow):
        ready_event_tasks = workflow.get_tasks(state=TaskState.READY, spec_class=CatchingEvent)
        return ready_event_tasks
    
    def _run_until_user_input_required(self, workflow: BpmnWorkflow):
        BpmnTaskSpec
        task = workflow.get_next_task(state=TaskState.READY, manual=False)
        while task is not None:
            print('get ready auto task:', task.id, task.task_spec.name, type(task.task_spec))
            result = task.run()
            if not result:
                task.complete()
            print('\t task result:', result, TaskState.get_name(task.state))
            self._run_ready_events(workflow)
            task = workflow.get_next_task(state=TaskState.READY, manual=False)
        return workflow

    def _run_ready_events(self, workflow: BpmnWorkflow):
        workflow.refresh_waiting_tasks()
        task = workflow.get_next_task(state=TaskState.READY, spec_class=CatchingEvent)
        while task is not None:
            print('get ready event task:', task.id, task.task_spec.name, type(task.task_spec))
            result = task.run()
            print('\t event result:', result, TaskState.get_name(task.state))
            task = workflow.get_next_task(state=TaskState.READY, spec_class=CatchingEvent)

    def run(self, wf_file: str = None, wf_id: str = None):
        """
        wf_file: đường dẫn file BPMN (ví dụ: '1.xml')
        wf_id: id của workflow snapshot (ví dụ: '1')
        Nếu wf_id có, cần truyền kèm wf_file để load lại BPMN spec khi resume.
        """
        if not wf_id:
            return self._run_new_workflow(wf_file)
        else:
            if wf_file is None:
                raise ValueError("wf_file (BPMN config) must be provided when resuming workflow!")
            return self._resume_workflow(wf_file, wf_id)

    def _resume_workflow(self, bpmn_config_file: str, wf_id: str):
        # Load lại BPMN spec từ file BPMN gốc
        wf_content = self.storage.load_bpmn_config(bpmn_config_file)
        bpmn_parser = self._parse_bpmn(wf_content)
        main_spec = self._get_main_spec(bpmn_parser)

        wf = BpmnWorkflow(main_spec)

        # Lấy dữ liệu runtime đã snapshot
        wf_runtime = self.storage.get_snapshot_workflow(wf_id)
        print('type of wf_runtime:', type(wf_runtime))
        # Deserialize với spec context
        # wf = BpmnWorkflow.deserialize(JSONSerializer(), wf_runtime)
        wf.deserialize(JSONSerializer(), wf_runtime)
        wf = self._run_until_user_input_required(wf)

        if wf.is_completed():
            print("Workflow completed.")
        else:
            next_task = wf.get_next_task(state=TaskState.READY, manual=True)
            if next_task:
                print(f"Workflow paused, waiting for user input on task ID: {next_task.id}, Name: {next_task.task_spec.name}, Type: {type(next_task.task_spec)}")
            return

    def _run_new_workflow(self, bpmn_config_file: str):
        wf_content = self.storage.load_bpmn_config(bpmn_config_file)
        bpmn_parser = self._parse_bpmn(wf_content)
        main_process = self._get_main_spec(bpmn_parser)

        wf = BpmnWorkflow(main_process)
        self._show_info_tasks(wf.get_tasks())
        self._show_wf_state(wf)

        wf = self._run_until_user_input_required(wf)

        if wf.is_completed():
            print("Workflow completed.")
        else:
            next_task = wf.get_next_task(state=TaskState.READY, manual=True)
            if next_task:
                print(f"Workflow paused, waiting for user input on task ID: {next_task.id}, Name: {next_task.task_spec.name}, Type: {type(next_task.task_spec)}")
            # print("Workflow runtime data:", wf.serialize(DictionarySerializer()))
            self.storage.snapshot_workflow('1', wf)
            return