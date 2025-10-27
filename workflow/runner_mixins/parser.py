from typing import Any, Dict, List
from SpiffWorkflow.bpmn.parser import BpmnParser


class BpmnParserMixin:
    def parse_bpmn(self, bpmn_file_content: str) -> BpmnParser:
        bpmn_parser = BpmnParser()
        bpmn_parser.add_bpmn_str(bpmn_file_content.encode("utf-8"))
        return bpmn_parser
    
    def _get_main_spec(self, bpmn_parser: BpmnParser):
        bpmn_specs = bpmn_parser.find_all_specs()
        main_process_id = list(bpmn_specs.keys())[0]
        main_spec = bpmn_specs[main_process_id]
        return main_spec