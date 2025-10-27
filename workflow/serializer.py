
from SpiffWorkflow.bpmn.serializer import DEFAULT_CONFIG
from SpiffWorkflow.bpmn.serializer.default import BpmnTaskSpecConverter
from SpiffWorkflow.bpmn.specs.defaults import ServiceTask


class ServiceTaskConverter(BpmnTaskSpecConverter):
    """The default converter for `ScriptTask`"""

    def to_dict(self, spec):
        dct = self.get_default_attributes(spec)
        return dct

MySerializerConfig = DEFAULT_CONFIG.copy()
MySerializerConfig.update({
    ServiceTask: ServiceTaskConverter,
})
