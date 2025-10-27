# -*- coding: utf-8 -*-
import time
from uuid import uuid4
from datetime import datetime
from typing import  Optional
from umongo import Document, fields
from connections import db_conn  
from .workflow_config import WorkflowConfigurationModel


@db_conn.register
class WorkflowInstanceModel(Document):
    tenant = fields.StringField(required=True)
    wf_id = fields.StringField(required=True, unique=True)
    wf_config_id = fields.ObjectIdField(required=True)

    name = fields.StringField(required=True)
    description = fields.StringField(required=False)


    bpmn_xml = fields.StringField(required=True)  # Cấu hình workflow
    runtime_state = fields.StringField(required=False)  # Dữ liệu khởi tạo workflow instance
    runtime_config = fields.DictField(default=dict)  # Cấu hình runtime (nếu có)
    status = fields.StringField(default="initialized")  # Trạng thái hiện tại của workflow instance

    is_completed = fields.BooleanField(default=False)  # Đánh dấu workflow đã hoàn thành

    created_date = fields.DateTimeField(default=lambda: datetime.now())  # Ngày tạo
    updated_date = fields.DateTimeField(allow_none=True)  # Thời gian cập nhật gần nhất
    
    class Meta:
        collection_name = "WorkflowInstance"
        indexes = (
            {
                'key': ('tenant', 'wf_id', ),
                'unique': True
            },
        )

    @classmethod
    async def new_workflow_instance(cls, workflow_config: WorkflowConfigurationModel, **kwargs) -> Optional["WorkflowInstanceModel"]:
        """Tạo một workflow instance mới."""
        _start = time.time_ns()
        tenant = kwargs.get("tenant", '1')
        runtime_state = kwargs.get("runtime_state", "")
        workflow_instance = cls(
            tenant=tenant,
            wf_id=str(uuid4()),
            wf_config_id=workflow_config.id,
            name=workflow_config.name,
            description=workflow_config.description,

            bpmn_xml=workflow_config.bpmn_xml,
            runtime_state=runtime_state,
            runtime_config=workflow_config.config,
        )
        await workflow_instance.commit()
        print(f'\t\t\t\t: WorkflowInstanceModel.new_workflow_instance - {(time.time_ns() - _start) / 1e6} ms.')
        return workflow_instance
    
    @classmethod
    async def get_by_wf_id(cls, wf_id: str, **kwargs) -> Optional["WorkflowInstanceModel"]:
        """Lấy workflow instance theo wf_id và tenant."""
        _start = time.time_ns()
        tenant = kwargs.get("tenant", '1')
        condition = {'tenant': tenant, 'wf_id': wf_id}
        # print(f' query condition: {condition} with cls: {cls}')
        workflow_instance = await cls.find_one(condition)
        # print(f' found workflow instance: {workflow_instance.id}')
        print(f'\t\t\t\t: WorkflowInstanceModel.get_by_wf_id - {(time.time_ns() - _start) / 1e6} ms.')
        return workflow_instance
    
    @classmethod
    async def update_runtime_state(cls, wf_id: str, runtime_state: str, **kwargs) -> Optional["WorkflowInstanceModel"]:
        """Cập nhật runtime_state của workflow instance."""
        _start = time.time_ns()
        tenant = kwargs.get("tenant", '1')
        workflow_instance = await cls.get_by_wf_id(wf_id, tenant=tenant)
        if not workflow_instance:
            return None
        workflow_instance.runtime_state = runtime_state
        workflow_instance.updated_date = datetime.now()
        if kwargs.get("is_completed"):
            workflow_instance.status = "completed"
        else:
            workflow_instance.status = "in_progress"
            
        await workflow_instance.commit()
        print(f'\t\t\t\t: WorkflowInstanceModel.update_runtime_state - {(time.time_ns() - _start) / 1e6} ms.')
        return workflow_instance
    
    async def get_workflow_id(self) -> str:
        """Lấy wf_id của workflow instance."""
        return self.wf_id

    async def get_workflow_config_id(self) -> str:
        """Lấy wf_config_id của workflow instance."""
        return str(self.wf_config_id)
    
    async def get_workflow_state(self) -> str:
        """Lấy runtime_state của workflow instance."""
        return self.runtime_state

    async def get_workflow_config(self) -> str:
        """Lấy configuration của workflow instance."""
        return self.bpmn_xml
    
    async def get_workflow_runtime_config(self) -> dict:
        """Lấy runtime_config của workflow instance."""
        return self.runtime_config