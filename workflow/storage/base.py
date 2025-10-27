from typing import Any


class AbsWorkflowConfig:
    @classmethod
    async def get_by_wf_id(cls, wf_id: str, tenant: str='1') -> "AbsWorkflowConfig":
        raise NotImplementedError("Method not implemented.")
    
class AbsWorkflowState:
    async def get_workflow_id(self) -> str:
        raise NotImplementedError("Method not implemented.")
    
    async def get_workflow_config_id(self) -> str:
        raise NotImplementedError("Method not implemented.")
    
    async def get_workflow_state(self) -> str:
        raise NotImplementedError("Method not implemented.")
    
    async def get_workflow_config(self) -> str:
        raise NotImplementedError("Method not implemented.")
    
    @classmethod
    async def new_workflow_instance(self, workflow_config: Any, **kwargs) -> "AbsWorkflowState":
        raise NotImplementedError("Method not implemented.")
    
    @classmethod
    async def get_by_wf_id(cls, wf_id: str, **kwargs) -> "AbsWorkflowState":
        raise NotImplementedError("Method not implemented.")
    
    @classmethod
    async def update_runtime_state(cls, wf_id: str, runtime_state: str, **kwargs) -> "AbsWorkflowState":
        raise NotImplementedError("Method not implemented.")


class BaseStorage:
    async def load_workflow_from_configuration(self, wf_id: str) -> AbsWorkflowState:
        raise NotImplementedError("Save method not implemented.")

    async def load_workflow_runtime_state(self, wf_id: str) -> AbsWorkflowState:
        raise NotImplementedError("Load method not implemented.")

    async def save_workflow_runtime_state(self, wf_id: str, state: Any) -> None:
        raise NotImplementedError("Save method not implemented.")

