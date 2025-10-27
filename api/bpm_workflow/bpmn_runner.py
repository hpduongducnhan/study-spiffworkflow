from fastapi import HTTPException, Header
from models import WorkflowConfigurationModel
from SpiffWorkflow.bpmn.parser.BpmnParser import BpmnParser

from .router import api_router


@api_router.post("/run", response_model=dict)
async def run_bpmn_workflow(workflow_id: str, tenant_id: str = Header(None)):
    if not tenant_id:
        tenant_id = '1'

    existing: WorkflowConfigurationModel = await WorkflowConfigurationModel.find_one({"tenant": tenant_id, 'wf_id': workflow_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Workflow not found.")
	
    bpmn_parser = BpmnParser()
    bpmn_parser.add_bpmn_xml(existing.bpmn_xml)