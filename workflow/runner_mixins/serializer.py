
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow
from SpiffWorkflow.bpmn.serializer import BpmnWorkflowSerializer
from ..serializer import MySerializerConfig


class SerializerMixin:
    wf_registry: BpmnWorkflowSerializer = BpmnWorkflowSerializer.configure(
        config=MySerializerConfig
    )

    def _get_wf_serializer(self) -> BpmnWorkflowSerializer:
        return BpmnWorkflowSerializer(registry=self.wf_registry)
    
    def _serialize_workflow(self, wf: BpmnWorkflow) -> str:
        serializer = self._get_wf_serializer()
        res = serializer.serialize_json(wf)
        return res
    
    def _deserialize_workflow(self, serialized_workflow_data: str) -> BpmnWorkflow:
        serializer = self._get_wf_serializer()
        wf = serializer.deserialize_json(serialized_workflow_data)
        return wf