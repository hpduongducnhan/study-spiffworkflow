# -*- coding: utf-8 -*-
from .workflow_config import WorkflowConfigurationModel
from .workflow_instance import WorkflowInstanceModel


async def ensure_indexes():
    for model in [WorkflowInstanceModel, WorkflowConfigurationModel]:
        await model.ensure_indexes()
        ...

__all__ = [
    "ensure_indexes",
    "WorkflowConfigurationModel",
    "WorkflowInstanceModel",
]