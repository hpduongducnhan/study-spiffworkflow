import os
import sys
import logging
import asyncio
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow
from core import (
    CoreRunner,
    NodeManager,
    Storage,
)


# for name in ('spiff.workflow', 'spiff.task'):
#     logger = logging.getLogger(name)
#     log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     stream_handler = logging.StreamHandler(stream=sys.stdout)
#     stream_handler.setFormatter(log_format)
#     stream_handler.setLevel(logging.DEBUG)
#     logger.addHandler(stream_handler)
#     logger.setLevel(logging.DEBUG)


def main():
    storage = Storage()
    node_manager = NodeManager()
    core_runner = CoreRunner(storage, node_manager)

    bpmn_file = os.path.join(
        os.getcwd(),
        'data',
        '1.xml'
    )

    # core_runner.run(bpmn_file)


    core_runner.run(bpmn_file, wf_id='1_1')


if __name__ == "__main__":
    main()