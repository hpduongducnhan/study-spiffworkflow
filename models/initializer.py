from .workflow_config import WorkflowConfigurationModel


async def initialize_workflow_configuration_model():
    if await WorkflowConfigurationModel.get_by_wf_id('8865a29d-7b8a-4766-86f5-48ea9b958cf2', tenant='1'):
        return  # already initialized
    
    new = WorkflowConfigurationModel(
        tenant='1',
        wf_id='8865a29d-7b8a-4766-86f5-48ea9b958cf2',
        name='Initialization Test Workflow',
        description='A workflow created to test model initialization.',
        bpmn_xml='''<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" xmlns:camunda="http://camunda.org/schema/1.0/bpmn" id="Definitions_1" targetNamespace="http://bpmn.io/schema/bpmn">
  <bpmn:process id="Process_1" name="Validate Alert" isExecutable="true" camunda:jobPriority="">
    <bpmn:extensionElements>
      <camunda:executionListener expression="" event="end" />
      <camunda:properties>
        <camunda:property name="" value="" />
      </camunda:properties>
    </bpmn:extensionElements>
    <bpmn:startEvent id="Event_06wyuuc" name="Start" camunda:exclusive="false">
      <bpmn:extensionElements />
      <bpmn:outgoing>Flow_19aqx5z</bpmn:outgoing>
    </bpmn:startEvent>
    <bpmn:sequenceFlow id="Flow_19aqx5z" sourceRef="Event_06wyuuc" targetRef="Activity_150lkk4" />
    <bpmn:serviceTask id="Activity_150lkk4" name="Validate Alert" camunda:delegateExpression="">
      <bpmn:extensionElements>
        <camunda:inputOutput>
          <camunda:inputParameter name="json_schema">{
  "$schema": "http://json-schema.org/draft/2020-12/schema",
  "title": "AlertGroup",
  "type": "object",
  "properties": {
    "group_root_eventdatetime": {
      "type": "string",
      "format": "date-time"
    },
    "group_root_hostname": {
      "type": "string"
    },
    "group_root_servicename": {
      "type": "string"
    },
    "group_time": {
      "type": "string",
      "format": "date-time"
    },
    "group_detail": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "hostname": { "type": "string" },
          "servicestate": { "type": "string", "enum": ["critical", "warning", "ok", "unknown", "None"] },
          "eventdatetime": { "type": "string", "format": "date-time" },
          "servicename": { "type": "string" },
          "alert_index": { "type": "string" },
          "hoststate": { "type": ["string", "null"] },
          "output": { "type": "string" }
        },
        "required": ["hostname", "servicestate", "eventdatetime", "servicename", "alert_index", "output"]
      }
    },
    "group_root_output": {
      "type": "string"
    },
    "group_id": {
      "type": "string",
      "format": "uuid"
    },
    "noofbroadbandcustomer": {
      "type": "integer",
      "minimum": 0
    },
    "noofpaytvcustomer": {
      "type": "integer",
      "minimum": 0
    }
  },
  "required": [
    "group_root_eventdatetime",
    "group_root_hostname",
    "group_root_servicename",
    "group_time",
    "group_detail",
    "group_root_output",
    "group_id",
    "noofbroadbandcustomer",
    "noofpaytvcustomer"
  ]
}</camunda:inputParameter>
        </camunda:inputOutput>
      </bpmn:extensionElements>
      <bpmn:incoming>Flow_19aqx5z</bpmn:incoming>
      <bpmn:outgoing>Flow_1ogfz44</bpmn:outgoing>
    </bpmn:serviceTask>
    <bpmn:endEvent id="Event_15vmvzz" name="End">
      <bpmn:incoming>Flow_04b63jc</bpmn:incoming>
      <bpmn:incoming>Flow_1qpgy38</bpmn:incoming>
      <bpmn:incoming>Flow_1ux1fta</bpmn:incoming>
    </bpmn:endEvent>
    <bpmn:exclusiveGateway id="Gateway_1mgityt" name="Is alert valid">
      <bpmn:incoming>Flow_1ogfz44</bpmn:incoming>
      <bpmn:outgoing>Flow_13d7xmf</bpmn:outgoing>
      <bpmn:outgoing>Flow_0kcg53h</bpmn:outgoing>
    </bpmn:exclusiveGateway>
    <bpmn:userTask id="Activity_01d9t81" name="User Check">
      <bpmn:incoming>Flow_0w7nav9</bpmn:incoming>
      <bpmn:outgoing>Flow_04b63jc</bpmn:outgoing>
    </bpmn:userTask>
    <bpmn:sequenceFlow id="Flow_04b63jc" sourceRef="Activity_01d9t81" targetRef="Event_15vmvzz" />
    <bpmn:sequenceFlow id="Flow_13d7xmf" name="Error" sourceRef="Gateway_1mgityt" targetRef="Gateway_1jzhhrx">
      <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">0</bpmn:conditionExpression>
    </bpmn:sequenceFlow>
    <bpmn:sequenceFlow id="Flow_0w7nav9" sourceRef="Gateway_1jzhhrx" targetRef="Activity_01d9t81" />
    <bpmn:parallelGateway id="Gateway_1jzhhrx" name="">
      <bpmn:incoming>Flow_13d7xmf</bpmn:incoming>
      <bpmn:incoming>Flow_12h5wbw</bpmn:incoming>
      <bpmn:incoming>Flow_0n82swa</bpmn:incoming>
      <bpmn:incoming>Flow_0nwxzmv</bpmn:incoming>
      <bpmn:incoming>Flow_1vhz8m1</bpmn:incoming>
      <bpmn:outgoing>Flow_0w7nav9</bpmn:outgoing>
      <bpmn:outgoing>Flow_1bkuq5i</bpmn:outgoing>
    </bpmn:parallelGateway>
    <bpmn:sequenceFlow id="Flow_1bkuq5i" sourceRef="Gateway_1jzhhrx" targetRef="Activity_0ezuwbz" />
    <bpmn:serviceTask id="Activity_0ezuwbz" name="Send Chat">
      <bpmn:incoming>Flow_1bkuq5i</bpmn:incoming>
      <bpmn:outgoing>Flow_1qpgy38</bpmn:outgoing>
    </bpmn:serviceTask>
    <bpmn:sequenceFlow id="Flow_1qpgy38" sourceRef="Activity_0ezuwbz" targetRef="Event_15vmvzz" />
    <bpmn:sequenceFlow id="Flow_1ogfz44" sourceRef="Activity_150lkk4" targetRef="Gateway_1mgityt" />
    <bpmn:sequenceFlow id="Flow_0kcg53h" name="ok" sourceRef="Gateway_1mgityt" targetRef="Activity_1kqhxlp">
      <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">1</bpmn:conditionExpression>
    </bpmn:sequenceFlow>
    <bpmn:exclusiveGateway id="Gateway_0vl806i" name="Is map infras success">
      <bpmn:incoming>Flow_1thowb1</bpmn:incoming>
      <bpmn:outgoing>Flow_12h5wbw</bpmn:outgoing>
      <bpmn:outgoing>Flow_1jmhg0d</bpmn:outgoing>
    </bpmn:exclusiveGateway>
    <bpmn:sequenceFlow id="Flow_1thowb1" sourceRef="Activity_1kqhxlp" targetRef="Gateway_0vl806i" />
    <bpmn:sequenceFlow id="Flow_12h5wbw" name="Error" sourceRef="Gateway_0vl806i" targetRef="Gateway_1jzhhrx">
      <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">0</bpmn:conditionExpression>
    </bpmn:sequenceFlow>
    <bpmn:sequenceFlow id="Flow_1jmhg0d" name="ok" sourceRef="Gateway_0vl806i" targetRef="Activity_0fjnsck">
      <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">1</bpmn:conditionExpression>
    </bpmn:sequenceFlow>
    <bpmn:exclusiveGateway id="Gateway_0g01clt" name="is map queue success">
      <bpmn:incoming>Flow_1bgz2b8</bpmn:incoming>
      <bpmn:outgoing>Flow_0n82swa</bpmn:outgoing>
      <bpmn:outgoing>Flow_1lxm869</bpmn:outgoing>
    </bpmn:exclusiveGateway>
    <bpmn:sequenceFlow id="Flow_1bgz2b8" sourceRef="Activity_0fjnsck" targetRef="Gateway_0g01clt" />
    <bpmn:sequenceFlow id="Flow_0n82swa" name="Error" sourceRef="Gateway_0g01clt" targetRef="Gateway_1jzhhrx">
      <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">0</bpmn:conditionExpression>
    </bpmn:sequenceFlow>
    <bpmn:sequenceFlow id="Flow_1lxm869" name="ok" sourceRef="Gateway_0g01clt" targetRef="Activity_0icavw9">
      <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">1</bpmn:conditionExpression>
    </bpmn:sequenceFlow>
    <bpmn:exclusiveGateway id="Gateway_0c5sjrz" name="build ticket body success">
      <bpmn:extensionElements />
      <bpmn:incoming>Flow_0maer6z</bpmn:incoming>
      <bpmn:outgoing>Flow_0nwxzmv</bpmn:outgoing>
      <bpmn:outgoing>Flow_0d7yfq2</bpmn:outgoing>
    </bpmn:exclusiveGateway>
    <bpmn:sequenceFlow id="Flow_0maer6z" sourceRef="Activity_0icavw9" targetRef="Gateway_0c5sjrz" />
    <bpmn:sequenceFlow id="Flow_0nwxzmv" name="Error" sourceRef="Gateway_0c5sjrz" targetRef="Gateway_1jzhhrx">
      <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">0</bpmn:conditionExpression>
    </bpmn:sequenceFlow>
    <bpmn:sequenceFlow id="Flow_0d7yfq2" sourceRef="Gateway_0c5sjrz" targetRef="Activity_1p3gf66">
      <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">1</bpmn:conditionExpression>
    </bpmn:sequenceFlow>
    <bpmn:exclusiveGateway id="Gateway_13gxoiw" name="is ok">
      <bpmn:incoming>Flow_125k6wx</bpmn:incoming>
      <bpmn:outgoing>Flow_1vhz8m1</bpmn:outgoing>
      <bpmn:outgoing>Flow_04x025v</bpmn:outgoing>
    </bpmn:exclusiveGateway>
    <bpmn:sequenceFlow id="Flow_125k6wx" sourceRef="Activity_1p3gf66" targetRef="Gateway_13gxoiw" />
    <bpmn:sequenceFlow id="Flow_1vhz8m1" name="Error" sourceRef="Gateway_13gxoiw" targetRef="Gateway_1jzhhrx">
      <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">0</bpmn:conditionExpression>
    </bpmn:sequenceFlow>
    <bpmn:sequenceFlow id="Flow_04x025v" name="OK" sourceRef="Gateway_13gxoiw" targetRef="Activity_0m66uv6">
      <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">1</bpmn:conditionExpression>
    </bpmn:sequenceFlow>
    <bpmn:serviceTask id="Activity_0m66uv6" name="Notify Customer">
      <bpmn:incoming>Flow_04x025v</bpmn:incoming>
      <bpmn:outgoing>Flow_193mmd3</bpmn:outgoing>
    </bpmn:serviceTask>
    <bpmn:serviceTask id="Activity_1p3gf66" name="Send To Ticket">
      <bpmn:incoming>Flow_0d7yfq2</bpmn:incoming>
      <bpmn:outgoing>Flow_125k6wx</bpmn:outgoing>
    </bpmn:serviceTask>
    <bpmn:serviceTask id="Activity_1kqhxlp" name="Mapping Infrastructure">
      <bpmn:incoming>Flow_0kcg53h</bpmn:incoming>
      <bpmn:outgoing>Flow_1thowb1</bpmn:outgoing>
    </bpmn:serviceTask>
    <bpmn:serviceTask id="Activity_0fjnsck" name="Map Queue">
      <bpmn:incoming>Flow_1jmhg0d</bpmn:incoming>
      <bpmn:outgoing>Flow_1bgz2b8</bpmn:outgoing>
    </bpmn:serviceTask>
    <bpmn:serviceTask id="Activity_0icavw9" name="Build Ticket Request Body">
      <bpmn:incoming>Flow_1lxm869</bpmn:incoming>
      <bpmn:outgoing>Flow_0maer6z</bpmn:outgoing>
    </bpmn:serviceTask>
    <bpmn:sequenceFlow id="Flow_193mmd3" sourceRef="Activity_0m66uv6" targetRef="Activity_15bqdy8" />
    <bpmn:userTask id="Activity_15bqdy8" name="Customer Check">
      <bpmn:incoming>Flow_193mmd3</bpmn:incoming>
      <bpmn:outgoing>Flow_1ux1fta</bpmn:outgoing>
    </bpmn:userTask>
    <bpmn:sequenceFlow id="Flow_1ux1fta" sourceRef="Activity_15bqdy8" targetRef="Event_15vmvzz" />
  </bpmn:process>
  <bpmndi:BPMNDiagram id="BPMNDiagram_1">
    <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="Process_1">
      <bpmndi:BPMNShape id="Event_06wyuuc_di" bpmnElement="Event_06wyuuc">
        <dc:Bounds x="322" y="142" width="36" height="36" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="328" y="185" width="25" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_0pnnca7_di" bpmnElement="Activity_150lkk4">
        <dc:Bounds x="410" y="120" width="100" height="80" />
        <bpmndi:BPMNLabel />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Event_15vmvzz_di" bpmnElement="Event_15vmvzz">
        <dc:Bounds x="1052" y="142" width="36" height="36" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="1060" y="112" width="20" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Gateway_1mgityt_di" bpmnElement="Gateway_1mgityt" isMarkerVisible="true">
        <dc:Bounds x="435" y="245" width="50" height="50" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="350" y="260" width="60" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_0zjol34_di" bpmnElement="Activity_01d9t81">
        <dc:Bounds x="820" y="230" width="100" height="80" />
        <bpmndi:BPMNLabel />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Gateway_1n16gxd_di" bpmnElement="Gateway_1jzhhrx">
        <dc:Bounds x="705" y="245" width="50" height="50" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_1sfqt89_di" bpmnElement="Activity_0ezuwbz">
        <dc:Bounds x="820" y="120" width="100" height="80" />
        <bpmndi:BPMNLabel />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Gateway_0vl806i_di" bpmnElement="Gateway_0vl806i" isMarkerVisible="true">
        <dc:Bounds x="435" y="495" width="50" height="50" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="349" y="510" width="63" height="27" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Gateway_0g01clt_di" bpmnElement="Gateway_0g01clt" isMarkerVisible="true">
        <dc:Bounds x="565" y="615" width="50" height="50" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="557" y="585" width="67" height="27" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Gateway_0c5sjrz_di" bpmnElement="Gateway_0c5sjrz" isMarkerVisible="true">
        <dc:Bounds x="705" y="725" width="50" height="50" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="690" y="782" width="80" height="27" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Gateway_13gxoiw_di" bpmnElement="Gateway_13gxoiw" isMarkerVisible="true">
        <dc:Bounds x="845" y="615" width="50" height="50" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="859" y="585" width="24" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_1kuaw2q_di" bpmnElement="Activity_0m66uv6">
        <dc:Bounds x="1020" y="600" width="100" height="80" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_0enfnw9_di" bpmnElement="Activity_1p3gf66">
        <dc:Bounds x="820" y="710" width="100" height="80" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_0wwbp6c_di" bpmnElement="Activity_1kqhxlp">
        <dc:Bounds x="410" y="350" width="100" height="80" />
        <bpmndi:BPMNLabel />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_14dxcq3_di" bpmnElement="Activity_0fjnsck">
        <dc:Bounds x="410" y="600" width="100" height="80" />
        <bpmndi:BPMNLabel />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_1qupali_di" bpmnElement="Activity_0icavw9">
        <dc:Bounds x="540" y="710" width="100" height="80" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Activity_0eigc3x_di" bpmnElement="Activity_15bqdy8">
        <dc:Bounds x="1020" y="430" width="100" height="80" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNEdge id="Flow_19aqx5z_di" bpmnElement="Flow_19aqx5z">
        <di:waypoint x="358" y="160" />
        <di:waypoint x="410" y="160" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_04b63jc_di" bpmnElement="Flow_04b63jc">
        <di:waypoint x="920" y="270" />
        <di:waypoint x="1070" y="270" />
        <di:waypoint x="1070" y="178" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_13d7xmf_di" bpmnElement="Flow_13d7xmf">
        <di:waypoint x="485" y="270" />
        <di:waypoint x="705" y="270" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="582" y="252" width="26" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_0w7nav9_di" bpmnElement="Flow_0w7nav9">
        <di:waypoint x="755" y="270" />
        <di:waypoint x="820" y="270" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_1bkuq5i_di" bpmnElement="Flow_1bkuq5i">
        <di:waypoint x="730" y="245" />
        <di:waypoint x="730" y="160" />
        <di:waypoint x="820" y="160" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_1qpgy38_di" bpmnElement="Flow_1qpgy38">
        <di:waypoint x="920" y="160" />
        <di:waypoint x="1052" y="160" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_1ogfz44_di" bpmnElement="Flow_1ogfz44">
        <di:waypoint x="460" y="200" />
        <di:waypoint x="460" y="245" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_0kcg53h_di" bpmnElement="Flow_0kcg53h">
        <di:waypoint x="460" y="295" />
        <di:waypoint x="460" y="350" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="469" y="320" width="13" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_1thowb1_di" bpmnElement="Flow_1thowb1">
        <di:waypoint x="460" y="430" />
        <di:waypoint x="460" y="495" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_12h5wbw_di" bpmnElement="Flow_12h5wbw">
        <di:waypoint x="485" y="520" />
        <di:waypoint x="730" y="520" />
        <di:waypoint x="730" y="295" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="596" y="502" width="26" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_1jmhg0d_di" bpmnElement="Flow_1jmhg0d">
        <di:waypoint x="460" y="545" />
        <di:waypoint x="460" y="600" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="469" y="569" width="13" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_1bgz2b8_di" bpmnElement="Flow_1bgz2b8">
        <di:waypoint x="510" y="640" />
        <di:waypoint x="565" y="640" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_0n82swa_di" bpmnElement="Flow_0n82swa">
        <di:waypoint x="615" y="640" />
        <di:waypoint x="730" y="640" />
        <di:waypoint x="730" y="295" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="647" y="623" width="26" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_1lxm869_di" bpmnElement="Flow_1lxm869">
        <di:waypoint x="590" y="665" />
        <di:waypoint x="590" y="710" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="599" y="685" width="13" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_0maer6z_di" bpmnElement="Flow_0maer6z">
        <di:waypoint x="640" y="750" />
        <di:waypoint x="705" y="750" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_0nwxzmv_di" bpmnElement="Flow_0nwxzmv">
        <di:waypoint x="730" y="725" />
        <di:waypoint x="730" y="295" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="737" y="685" width="26" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_0d7yfq2_di" bpmnElement="Flow_0d7yfq2">
        <di:waypoint x="755" y="750" />
        <di:waypoint x="820" y="750" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_125k6wx_di" bpmnElement="Flow_125k6wx">
        <di:waypoint x="870" y="710" />
        <di:waypoint x="870" y="665" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_1vhz8m1_di" bpmnElement="Flow_1vhz8m1">
        <di:waypoint x="845" y="640" />
        <di:waypoint x="730" y="640" />
        <di:waypoint x="730" y="295" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="775" y="622" width="26" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_04x025v_di" bpmnElement="Flow_04x025v">
        <di:waypoint x="895" y="640" />
        <di:waypoint x="1020" y="640" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="949" y="622" width="18" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_193mmd3_di" bpmnElement="Flow_193mmd3">
        <di:waypoint x="1070" y="600" />
        <di:waypoint x="1070" y="510" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_1ux1fta_di" bpmnElement="Flow_1ux1fta">
        <di:waypoint x="1070" y="430" />
        <di:waypoint x="1070" y="178" />
      </bpmndi:BPMNEdge>
    </bpmndi:BPMNPlane>
  </bpmndi:BPMNDiagram>
</bpmn:definitions>
''',
        config={},
        is_active=True,
    )
    await new.commit()


async def initialize_models():
    # This function can be expanded to initialize other models if needed
    await initialize_workflow_configuration_model()