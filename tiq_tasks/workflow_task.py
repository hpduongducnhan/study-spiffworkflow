import uuid
import logging
from typing import Dict, Optional
from workflow import WorkflowRunner, MongoStorage
from models import WorkflowConfigurationModel, WorkflowInstanceModel
from worker import tiq_broker


mongo_storage = MongoStorage(
    WorkflowConfigurationModel,
    WorkflowInstanceModel
)
workflow_runner = WorkflowRunner()
workflow_runner.set_storage(mongo_storage)
workflow_runner.validate()


for name in ('spiff.workflow', 'spiff.task'):
    logger = logging.getLogger(name)
    # log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # stream_handler = logging.StreamHandler(stream=sys.stdout)
    # stream_handler.setFormatter(log_format)
    # stream_handler.setLevel(logging.DEBUG)
    # logger.addHandler(stream_handler)
    logger.setLevel(logging.ERROR)


@tiq_broker.task("workflow_task")
async def workflow_task_handler(
    wf_id: str=None, 
    wf_config_id: str=None, 
    wf_data: Dict={}, 
    task_id: Optional[str | uuid.UUID]=None,  # to run specific user task / manual task
    task_data: Dict={}, # data for specific task
    **kwargs
) -> str:
    await workflow_runner.run(
        wf_id=wf_id,
        wf_config_id=wf_config_id,
        data=wf_data,
        task_id=task_id,
        task_data=task_data,
        **kwargs
    )
    return {
        'wf_id': wf_id,
        'wf_config_id': wf_config_id,
        'wf_data': wf_data,
        'task_id': task_id,
        'task_data': task_data,
        'kwargs': kwargs,
        'success': True,
    }

