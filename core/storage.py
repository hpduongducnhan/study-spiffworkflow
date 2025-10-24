import json
from typing import Any
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow
from SpiffWorkflow.bpmn.serializer import BpmnWorkflowSerializer
from SpiffWorkflow.serializer.json import JSONSerializer, DictionarySerializer
from .custom_serializer import MySerializerConfig


class Storage:
    def __init__(self):
        self._bpmn_workflow_serializer_registry = BpmnWorkflowSerializer.configure(config=MySerializerConfig)

    def _get_bpmn_workflow_serializer(self) -> BpmnWorkflowSerializer:
        return BpmnWorkflowSerializer(registry=self._bpmn_workflow_serializer_registry)

    def _serialize_workflow(self, wf: BpmnWorkflow) -> str:
        serializer = self._get_bpmn_workflow_serializer()
        res = serializer.serialize_json(wf)
        return res

    def _deserialize_workflow(self, serialized_workflow_data: str) -> BpmnWorkflow:
        serializer = self._get_bpmn_workflow_serializer()
        wf = serializer.deserialize_json(serialized_workflow_data)
        return wf

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
        res = self._serialize_workflow(wf)
        with open(f"1_{wf_id}_snapshot.json", 'w') as file:
            file.write(res)

    def get_workflow_from_snapshot(self, wf_id: str) -> BpmnWorkflow:
        with open(f"{wf_id}_snapshot.json", 'r') as file:
            serialized_data = file.read()
            return self._deserialize_workflow(serialized_data)
