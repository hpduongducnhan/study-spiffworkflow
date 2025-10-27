import xmltodict
from fastapi import HTTPException, Header
from typing import  List
from models import WorkflowConfigurationModel
from .router import api_router
from .schema import BpmnWorkflowCreate, BpmnWorkflowOut


# list BPMN Workflows
@api_router.get("/", response_model=List[BpmnWorkflowOut])
async def list_bpmn_workflows(tenant_id: str = Header(None)):
	if not tenant_id:
		tenant_id = '1'
	workflows = WorkflowConfigurationModel.find({'tenant': tenant_id})
	return [BpmnWorkflowOut.from_mongo(wf) async for wf in workflows]

# create BPMN Workflows
@api_router.post("/", response_model=dict)
async def create_bpmn_workflow(data: BpmnWorkflowCreate, tenant_id: str = Header(None)):
	if not tenant_id:
		tenant_id = '1'
	# Check for existing workflow with same tenant and wf_id
	existing = await WorkflowConfigurationModel.find_one({"tenant": tenant_id, 'wf_id': data.wf_id})
	if existing:
		raise HTTPException(status_code=409, detail="Workflow with this tenant and name already exists.")
	bpmn_json = {}
	try:
		bpmn_json = xmltodict.parse(data.bpmn_xml) if data.bpmn_xml else {}
	except Exception as e:
		...
	workflow = WorkflowConfigurationModel(
		tenant=tenant_id,
		wf_id=data.wf_id,
		name=data.name,
		description=data.description,
		config=data.config or {},
		bpmn_xml=data.bpmn_xml,
		bpmn_json=bpmn_json,
		is_active=True
	)
	await workflow.commit()
	return {"id": str(workflow.id), "message": "Created successfully"}


# create BPMN Workflows
@api_router.put("/", response_model=dict)
async def create_bpmn_workflow(data: BpmnWorkflowCreate, tenant_id: str = Header(None)):
	if not tenant_id:
		tenant_id = '1'
	# Check for existing workflow with same tenant and wf_id
	existing: WorkflowConfigurationModel = await WorkflowConfigurationModel.find_one({"tenant": tenant_id, 'wf_id': data.wf_id})
	if not existing:
		raise HTTPException(status_code=404, detail="Workflow not found.")
	bpmn_json = {}
	try:
		bpmn_json = xmltodict.parse(data.bpmn_xml) if data.bpmn_xml else {}
	except Exception as e:
		...
	existing.name = data.name
	existing.description = data.description
	existing.config = data.config or {}
	existing.bpmn_xml = data.bpmn_xml
	existing.bpmn_json = bpmn_json
	existing.is_active = True
	await existing.commit()
	return {"id": str(existing.id), "message": "Updated successfully"}


@api_router.get("/{workflow_id}", response_model=BpmnWorkflowOut)
async def get_bpmn_workflow(workflow_id: str, tenant_id: str = Header(None)):
	if not tenant_id:
		tenant_id = '1'

	workflow = await WorkflowConfigurationModel.find_one({"tenant": tenant_id, "wf_id": workflow_id})
	if not workflow:
		raise HTTPException(status_code=404, detail="Workflow not found")
	return BpmnWorkflowOut.from_mongo(workflow)
