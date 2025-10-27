import os
import sys
import logging
import asyncio
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow



# for name in ('spiff.workflow', 'spiff.task'):
#     logger = logging.getLogger(name)
#     log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     stream_handler = logging.StreamHandler(stream=sys.stdout)
#     stream_handler.setFormatter(log_format)
#     stream_handler.setLevel(logging.DEBUG)
#     logger.addHandler(stream_handler)
#     logger.setLevel(logging.DEBUG)

async def run_workflow():
    from workflow import WorkflowRunner, MongoStorage
    from models import ensure_indexes, WorkflowConfigurationModel, WorkflowInstanceModel
    from models.initializer import initialize_models

    await ensure_indexes()
    await initialize_models()   

    mongo_storage = MongoStorage(
        WorkflowConfigurationModel,
        WorkflowInstanceModel
    )
    workflow_runner = WorkflowRunner()
    workflow_runner.set_storage(mongo_storage)
    workflow_runner.validate()

    # To run workflow by wf_config_id
    # it will create a new workflow instance internally
    wf_config_id = '8865a29d-7b8a-4766-86f5-48ea9b958cf2'
    await workflow_runner.run(
        wf_config_id=wf_config_id
    )

    # To run workflow by wf_id
    # it will load existing workflow instance internally
    wf_id = '812b4f6d-f897-4f2b-bea8-3203005593c7'
    # await workflow_runner.run(
    #     wf_id=wf_id,
    #     wf_config_id=wf_config_id
    # )

    # To run user task 
    user_task_id = '33a06b23-3635-45aa-9823-572dbfb8fa0a'  # example user task id
    # await workflow_runner.run(
    #     wf_id=wf_id,
    #     wf_config_id=wf_config_id,
    #     task_id=user_task_id,   # user task id
    #     task_data={               # optional, data to set for the user task
    #         'approval': True,
    #         'comments': 'Approved by user.'
    #     }
    # )

async def simulate_workflows():
    from workflow import WorkflowRunner, MongoStorage
    from models import ensure_indexes, WorkflowConfigurationModel, WorkflowInstanceModel
    from models.initializer import initialize_models

    await ensure_indexes()
    await initialize_models()   

    mongo_storage = MongoStorage(
        WorkflowConfigurationModel,
        WorkflowInstanceModel
    )
    workflow_runner = WorkflowRunner()
    workflow_runner.set_storage(mongo_storage)
    workflow_runner.validate()

    wf_config_id = '8865a29d-7b8a-4766-86f5-48ea9b958cf2'

    
    async def worker(wfcid: int, sem: asyncio.Semaphore):
        async with sem:
            await workflow_runner.run(
                wf_config_id=wfcid
            )

    sem = asyncio.Semaphore(200)  # chỉ cho phép 200 task chạy đồng thời
    tasks = [asyncio.create_task(worker(wf_config_id, sem)) for i in range(10000)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    # asyncio.run(run_workflow())
    asyncio.run(simulate_workflows())