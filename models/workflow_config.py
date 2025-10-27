# -*- coding: utf-8 -*-
import time
from datetime import datetime
from typing import  Optional
from bson import ObjectId
from umongo import Document, fields
from connections import db_conn  


@db_conn.register
class WorkflowConfigurationModel(Document):
    tenant = fields.StringField(required=True)
    wf_id = fields.StringField(required=True, unique=True)
    name = fields.StringField(required=True)
    description = fields.StringField(required=False)
    config = fields.DictField(default=dict)  # Cấu hình workflow cho swiffworkflow
    bpmn_xml = fields.StringField(required=True)  # Lưu file BPMN XML để load lên bpmn.js
    bpmn_json = fields.DictField(required=False, allow_none=True)  # Lưu file BPMN JSON để khởi tạo swiffworkflow
    
    is_active = fields.BooleanField(default=True)  # Kích hoạt workflow
    created_date = fields.DateTimeField(default=lambda: datetime.now())  # Ngày tạo
    updated_date = fields.DateTimeField(allow_none=True)  # Thời gian cập nhật gần nhất
    
    class Meta:
        collection_name = "WorkflowConfiguration"
        indexes = (
            {'key': ('wf_id', )},
            {
                'key': ('tenant', 'wf_id', ),
                'unique': True
            },
        )

    @classmethod
    async def get_by_wf_id(cls, wf_id: str, tenant: str='1') -> Optional["WorkflowConfigurationModel"]:
        _start = time.time_ns()
        """Lấy workflow theo wf_id và tenant."""
        condition = {'tenant': tenant, 'wf_id': wf_id}
        # print(f' query condition: {condition} with cls: {cls}')
        workflow = await cls.find_one(condition)
        # print(f' found workflow: {workflow}')
        print(f'\t\t\t\t: WorkflowConfigurationModel.get_by_wf_id - {(time.time_ns() - _start) / 1e6} ms.')
        return workflow
    
    async def get_workflow_config_id(self) -> str:
        """Lấy wf_config_id của workflow instance."""
        return str(self.wf_config_id)

    async def get_workflow_config(self) -> dict:
        """Lấy cấu hình workflow."""
        return self.config