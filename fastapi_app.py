from fastapi import FastAPI
from workflow import WorkflowRunner, MongoStorage
from models import WorkflowConfigurationModel, WorkflowInstanceModel
from worker import tiq_broker
from tiq_tasks.say_hello import say_hello as say_hello_task
from tiq_tasks.workflow_task import workflow_task_handler


mongo_storage = MongoStorage(
    WorkflowConfigurationModel,
    WorkflowInstanceModel
)
workflow_runner = WorkflowRunner()
workflow_runner.set_storage(mongo_storage)
workflow_runner.validate()


async def start_up_tiq_broker():
    if not tiq_broker.is_worker_process:
        await tiq_broker.startup()
        print("TaskIq broker started")

app = FastAPI(on_startup=[start_up_tiq_broker])


@app.get("/api/say_hello")
async def say_hello(name: str):
    result = await say_hello_task.kiq(name)
    return {"message": str(result)}

@app.get('/api/start_workflow')
async def start_workflow(wf_config_id: str):
    wf_id, wf_config_id, workflow = await workflow_runner.init_workflow(
        wf_config_id=wf_config_id,
    )
    result = await workflow_task_handler.kiq(
        wf_id=wf_id,
        wf_config_id=wf_config_id,
    )
    return {'success': True, 'task_id': result.task_id}

@app.get("/api/manual_trigger")
async def manual_trigger(wf_id: str, t_id: str, approval: bool = None, comments: str = None, sleep_secs: float = 0):
    # Here you would implement the logic to trigger the manual task
    result = await workflow_task_handler.kiq(
        wf_id=wf_id,
        task_id=t_id,
        task_data={               # optional, data to set for the user task
            'approval': approval,
            'comments': comments,
            'sleep_secs': sleep_secs
        }
    )
    return {'success': True, 'message': f'Manual task {t_id} for workflow {wf_id} triggered.', 'task_id': result.task_id}
    
    