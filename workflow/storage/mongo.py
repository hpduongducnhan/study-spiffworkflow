from umongo import Document
from .base import BaseStorage, AbsWorkflowState, AbsWorkflowConfig


class MongoStorage(BaseStorage):
    def __init__(
        self,
        workflow_config_model_class: Document,
        workflow_instance_model_class: Document,
    ):
        for cls in [workflow_config_model_class, workflow_instance_model_class]:
            if not isinstance(cls, type):
                raise ValueError(f"Model classes must be class types. -> {cls} | {type(cls)}")

        self.config_collection_cls: AbsWorkflowConfig = workflow_config_model_class
        self.state_collection_cls: AbsWorkflowState = workflow_instance_model_class

    async def load_workflow_from_configuration(self, wf_config_id: str, **kwargs) -> dict:
        workflow_config_model = await self.config_collection_cls.get_by_wf_id(wf_config_id)
        if workflow_config_model:
            # creat new instance of workflow configuration
            workflow_instance = await self.state_collection_cls.new_workflow_instance(workflow_config_model)
            return workflow_instance
        else:
            raise ValueError(f"Workflow configuration with id {wf_config_id} not found. Select from {self.config_collection_cls}")

    async def load_workflow_runtime_state(self, wf_id: str) -> str:
        record = await self.state_collection_cls.get_by_wf_id(wf_id)
        if record:
            return record
        else:
            raise ValueError(f"Workflow state with id {wf_id} not found.")

    async def save_workflow_runtime_state(self, wf_id: str, state: str, **kwargs):
        return await self.state_collection_cls.update_runtime_state(wf_id, state, **kwargs)