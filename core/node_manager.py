from SpiffWorkflow.bpmn.workflow import BpmnWorkflow
from SpiffWorkflow.task import Task


class NodeManager:
    def __init__(self):
        self._node_handlers = {}

    def _get_node_handler(self, name: str):
        handler = self._node_handlers.get(name)
        if not handler:
            raise ValueError(f"No handler registered for node: {name}")
        return handler


    def run_node(self, wf: BpmnWorkflow, node: Task, extra: dict):
        handler = self._get_node_handler(node.task_spec.name)
        return handler(wf, node, extra)