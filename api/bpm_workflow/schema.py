# -*- coding: utf-8 -*-
from pydantic import BaseModel
from typing import Optional, Dict
from models import WorkflowConfigurationModel


class BpmnWorkflowCreate(BaseModel):
	wf_id: str
	name: str
	description: Optional[str] = None
	config: Optional[Dict] = None
	bpmn_xml: str
	is_active: Optional[bool] = True

class BpmnWorkflowUpdate(BaseModel):
	description: Optional[str] = None
	config: Optional[Dict] = None
	bpmn_xml: Optional[str] = None
	is_active: Optional[bool] = None

class BpmnWorkflowOut(BaseModel):
	id: str
	tenant: str
	wf_id: str
	name: str
	description: Optional[str] = None
	config: Optional[Dict] = None
	bpmn_xml: str
	is_active: bool
	created_date: Optional[str] = None
	updated_date: Optional[str] = None

	@classmethod
	def from_mongo(cls, obj: WorkflowConfigurationModel):
		return cls(
			id=str(obj.id),
			tenant=obj.tenant,
			wf_id=obj.wf_id,
			name=obj.name,
			description=getattr(obj, "description", None),
			config=getattr(obj, "config", None),
			bpmn_xml=obj.bpmn_xml,
			is_active=obj.is_active,
			created_date=str(getattr(obj, "created_date", "")),
			updated_date=str(getattr(obj, "updated_date", "")),
		)