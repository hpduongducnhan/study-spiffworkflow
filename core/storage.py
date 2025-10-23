import json
from typing import Any
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow
from SpiffWorkflow.bpmn.serializer import BpmnWorkflowSerializer
from SpiffWorkflow.bpmn.serializer.config import DEFAULT_CONFIG as SPIFF_CONFIG
from SpiffWorkflow.serializer.json import JSONSerializer, DictionarySerializer


class Storage:
    def __init__(self):
        ...

    def load_bpmn_config(self, file_path: str) -> str:
        """Load configuration from a file."""
        with open(file_path, 'r') as file:
            data = file.read()
            if not data:
                raise ValueError("Configuration file is empty")
            data = data.replace('\n', '').replace('\r', '').replace('\t', '').strip()
            return data
        
    def save_bpmn_config(self, file_path: str, data: str) -> None:
        ...

    def save_node_result(self, wf_id: str, node_id: str, result: Any) -> None:
        ...

    def save_workflow_result(self, wf_id: str, result: Any) -> None:
        ...

    def snapshot_workflow(self, wf_id: str, wf: BpmnWorkflow) -> None:
        # registry = BpmnWorkflowSerializer.configure(SPIFF_CONFIG)
        # serializer = BpmnWorkflowSerializer(registry=registry)
        # wf_dict = serializer.to_dict(wf)
        # print("Snapshot workflow dict:", wf_dict)
        # wf_json = serializer.serialize_json(wf)
        # print("Snapshot workflow JSON:", wf_json)
        res = wf.serialize(JSONSerializer())
        with open(f"1_{wf_id}_snapshot.json", 'w') as file:
            file.write(res)

    def get_snapshot_workflow(self, wf_id: str) -> str:
        with open(f"{wf_id}_snapshot.json", 'r') as file:
            return file.read()
