import json
import os
import uuid
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow
from SpiffWorkflow.bpmn.parser import BpmnParser
from SpiffWorkflow.serializer.json import JSONSerializer
from SpiffWorkflow.bpmn.specs.defaults import ServiceTask
from SpiffWorkflow.operators import Attrib
from SpiffWorkflow.bpmn.serializer import DEFAULT_CONFIG
from SpiffWorkflow.bpmn.serializer.workflow import BpmnWorkflowSerializer
from SpiffWorkflow.bpmn.serializer.default.workflow import BpmnWorkflowConverter, BpmnSubWorkflowConverter
from SpiffWorkflow.bpmn.serializer.default.process_spec import BpmnProcessSpecConverter
from SpiffWorkflow.bpmn.specs.mixins.subworkflow_task import SubWorkflowTask
from SpiffWorkflow.bpmn.specs import BpmnProcessSpec
from SpiffWorkflow.bpmn.specs.defaults import ServiceTask
from SpiffWorkflow.bpmn.serializer.default.task_spec import ScriptTaskConverter
from SpiffWorkflow.bpmn.serializer.default import BpmnTaskSpecConverter

class CustomJSONSerializer(JSONSerializer):
    def _default(self, obj):
        if isinstance(obj, ServiceTask):
            # Serialize ServiceTask thành dictionary với các thuộc tính cần thiết
            return {
                '__service_task__': {
                    'name': obj.name,
                    'bpmn_id': obj.bpmn_id,
                    'bpmn_name': obj.bpmn_name,
                    'inputs': obj.inputs,
                    'outputs': obj.outputs,
                    'description': obj.description,
                    'manual': obj.manual,
                    'lookahead': obj.lookahead,
                    'lane': obj.lane,
                    'documentation': obj.documentation,
                    'data_input_associations': obj.data_input_associations,
                    'data_output_associations': obj.data_output_associations,
                    'io_specification': obj.io_specification,
                }
            }
        if isinstance(obj, uuid.UUID):
            return {'__uuid__': obj.hex}
        if isinstance(obj, bytes):
            return {'__bytes__': obj.decode('ascii')}
        if isinstance(obj, Attrib):
            return {'__attrib__': obj.name}
        raise TypeError(f'{obj!r} is not JSON serializable')

    def _object_hook(self, dct):
        if '__service_task__' in dct:
            task_data = dct['__service_task__']
            # Tạo lại ServiceTask với các thuộc tính cơ bản
            service_task = ServiceTask()
            service_task.name = task_data['name']
            service_task.bpmn_id = task_data['bpmn_id']
            service_task.bpmn_name = task_data['bpmn_name']
            service_task.inputs = task_data['inputs']
            service_task.outputs = task_data['outputs']
            service_task.description = task_data['description']
            service_task.manual = task_data['manual']
            service_task.lookahead = task_data['lookahead']
            service_task.lane = task_data['lane']
            service_task.documentation = task_data['documentation']
            service_task.data_input_associations = task_data['data_input_associations']
            service_task.data_output_associations = task_data['data_output_associations']
            service_task.io_specification = task_data['io_specification']
            return service_task
        if '__uuid__' in dct:
            return uuid.UUID(dct['__uuid__'])
        if '__bytes__' in dct:
            return dct['__bytes__'].encode('ascii')
        if '__attrib__' in dct:
            return Attrib(dct['__attrib__'])
        return dct
    


class WorkflowConverter(BpmnWorkflowConverter):

    def to_dict(self, workflow):
        dct = super(BpmnWorkflowConverter, self).to_dict(workflow)
        dct['bpmn_events'] = self.registry.convert(workflow.bpmn_events)
        dct['subprocesses'] = {}
        dct['tasks'] = list(dct['tasks'].values())
        return dct

class SubworkflowConverter(BpmnSubWorkflowConverter):

    def to_dict(self, workflow):
        dct = super().to_dict(workflow)
        dct['tasks'] = list(dct['tasks'].values())
        return dct

class WorkflowSpecConverter(BpmnProcessSpecConverter):

    def to_dict(self, spec):
        dct = super().to_dict(spec)
        dct['task_specs'] = list(dct['task_specs'].values())
        return dct


class ServiceTaskConverter(BpmnTaskSpecConverter):
    """The default converter for `ScriptTask`"""

    def to_dict(self, spec):
        dct = self.get_default_attributes(spec)
        print('ServiceTaskConverter to_dict spec:', spec)
        return dct

MySerializerConfig = DEFAULT_CONFIG.copy()
MySerializerConfig.update({
    # BpmnWorkflow: WorkflowConverter,
    # SubWorkflowTask: SubworkflowConverter,
    # BpmnProcessSpec: WorkflowSpecConverter,
    ServiceTask: ServiceTaskConverter,
})
