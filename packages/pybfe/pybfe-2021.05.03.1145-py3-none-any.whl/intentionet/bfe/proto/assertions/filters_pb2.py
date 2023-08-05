# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: intentionet/bfe/proto/assertions/filters.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from intentionet.bfe.proto.assertions import parameters_pb2 as intentionet_dot_bfe_dot_proto_dot_assertions_dot_parameters__pb2
from intentionet.bfe.proto.assertions import violations_pb2 as intentionet_dot_bfe_dot_proto_dot_assertions_dot_violations__pb2
from intentionet.bfe.proto.datamodel import device_pb2 as intentionet_dot_bfe_dot_proto_dot_datamodel_dot_device__pb2
from intentionet.bfe.proto.datamodel import flow_pb2 as intentionet_dot_bfe_dot_proto_dot_datamodel_dot_flow__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='intentionet/bfe/proto/assertions/filters.proto',
  package='com.intentionet.bfe.assertions',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n.intentionet/bfe/proto/assertions/filters.proto\x12\x1e\x63om.intentionet.bfe.assertions\x1a\x31intentionet/bfe/proto/assertions/parameters.proto\x1a\x31intentionet/bfe/proto/assertions/violations.proto\x1a,intentionet/bfe/proto/datamodel/device.proto\x1a*intentionet/bfe/proto/datamodel/flow.proto\"\xab\x03\n)CrossZonePolicyFiltersFlowsAssertionInput\x12N\n\tfirewalls\x18\x01 \x01(\x0b\x32\x30.com.intentionet.bfe.assertions.DeviceFilterExprR\tfirewalls\x12\x44\n\x05\x66lows\x18\x02 \x01(\x0b\x32..com.intentionet.bfe.assertions.FlowFilterExprR\x05\x66lows\x12M\n\x04\x66rom\x18\x03 \x01(\x0b\x32\x39.com.intentionet.bfe.assertions.FirewallLocationMatchExprR\x04\x66rom\x12I\n\x02to\x18\x04 \x01(\x0b\x32\x39.com.intentionet.bfe.assertions.FirewallLocationMatchExprR\x02to\x12N\n\x06\x65xpect\x18\x05 \x01(\x0b\x32\x36.com.intentionet.bfe.assertions.FirewallBehaviorExpectR\x06\x65xpect\"\xc6\x06\n*CrossZonePolicyFiltersFlowsAssertionResult\x12p\n\tviolators\x18\x01 \x03(\x0b\x32R.com.intentionet.bfe.assertions.CrossZonePolicyFiltersFlowsAssertionResult.ElementR\tviolators\x12r\n\nconformers\x18\x05 \x03(\x0b\x32R.com.intentionet.bfe.assertions.CrossZonePolicyFiltersFlowsAssertionResult.ElementR\nconformers\x12\x33\n\x15violator_descriptions\x18\x04 \x03(\tR\x14violatorDescriptions\x1a\x8c\x03\n\x07\x45lement\x12\x39\n\x06\x64\x65vice\x18\x01 \x01(\x0b\x32!.com.intentionet.datamodel.DeviceR\x06\x64\x65vice\x12\x33\n\x04\x66low\x18\x02 \x01(\x0b\x32\x1f.com.intentionet.datamodel.FlowR\x04\x66low\x12\x44\n\x06\x61\x63tion\x18\x03 \x01(\x0e\x32,.com.intentionet.bfe.assertions.FilterActionR\x06\x61\x63tion\x12\x16\n\x06\x66ilter\x18\x04 \x01(\tR\x06\x66ilter\x12T\n\x0ctest_filters\x18\x05 \x01(\x0b\x32\x31.com.intentionet.bfe.assertions.TestFiltersResultR\x0btestFilters\x12]\n\x11\x64\x65scription_index\x18\x06 \x01(\x0b\x32\x30.com.intentionet.bfe.assertions.DescriptionIndexR\x10\x64\x65scriptionIndex\x1a\x62\n\rFailureResult\x12\x39\n\x06\x64\x65vice\x18\x01 \x01(\x0b\x32!.com.intentionet.datamodel.DeviceR\x06\x64\x65vice\x12\x16\n\x06reason\x18\x02 \x01(\tR\x06reasonJ\x04\x08\x02\x10\x03J\x04\x08\x03\x10\x04\"\xc9\x02\n\x1c\x46ilterBehaviorAssertionInput\x12J\n\x07\x64\x65vices\x18\x01 \x01(\x0b\x32\x30.com.intentionet.bfe.assertions.DeviceFilterExprR\x07\x64\x65vices\x12I\n\x07\x66ilters\x18\x02 \x01(\x0b\x32/.com.intentionet.bfe.assertions.FilterMatchExprR\x07\x66ilters\x12\x44\n\x05\x66lows\x18\x03 \x01(\x0b\x32..com.intentionet.bfe.assertions.FlowFilterExprR\x05\x66lows\x12L\n\x06\x65xpect\x18\x04 \x01(\x0b\x32\x34.com.intentionet.bfe.assertions.FilterBehaviorExpectR\x06\x65xpect\"\xdf\x04\n\x1d\x46ilterBehaviorAssertionResult\x12\x63\n\tviolators\x18\x01 \x03(\x0b\x32\x45.com.intentionet.bfe.assertions.FilterBehaviorAssertionResult.ElementR\tviolators\x12\x65\n\nconformers\x18\x02 \x03(\x0b\x32\x45.com.intentionet.bfe.assertions.FilterBehaviorAssertionResult.ElementR\nconformers\x12\x33\n\x15violator_descriptions\x18\x03 \x03(\tR\x14violatorDescriptions\x1a\xbc\x02\n\x07\x45lement\x12\x39\n\x06\x66ilter\x18\x01 \x01(\x0b\x32!.com.intentionet.datamodel.FilterR\x06\x66ilter\x12\x33\n\x04\x66low\x18\x02 \x01(\x0b\x32\x1f.com.intentionet.datamodel.FlowR\x04\x66low\x12T\n\x0ctest_filters\x18\x04 \x01(\x0b\x32\x31.com.intentionet.bfe.assertions.TestFiltersResultR\x0btestFilters\x12]\n\x11\x64\x65scription_index\x18\x05 \x01(\x0b\x32\x30.com.intentionet.bfe.assertions.DescriptionIndexR\x10\x64\x65scriptionIndexJ\x04\x08\x03\x10\x04R\x06\x61\x63tion\"^\n\x11TestFiltersResult\x12!\n\x0cmatched_line\x18\x01 \x01(\tR\x0bmatchedLine\x12&\n\x0ftrace_tree_json\x18\x02 \x03(\tR\rtraceTreeJson*[\n\x0c\x46ilterAction\x12\x19\n\x15\x46ILTER_ACTION_UNKNOWN\x10\x00\x12\x18\n\x14\x46ILTER_ACTION_PERMIT\x10\x01\x12\x16\n\x12\x46ILTER_ACTION_DENY\x10\x02\x62\x06proto3'
  ,
  dependencies=[intentionet_dot_bfe_dot_proto_dot_assertions_dot_parameters__pb2.DESCRIPTOR,intentionet_dot_bfe_dot_proto_dot_assertions_dot_violations__pb2.DESCRIPTOR,intentionet_dot_bfe_dot_proto_dot_datamodel_dot_device__pb2.DESCRIPTOR,intentionet_dot_bfe_dot_proto_dot_datamodel_dot_flow__pb2.DESCRIPTOR,])

_FILTERACTION = _descriptor.EnumDescriptor(
  name='FilterAction',
  full_name='com.intentionet.bfe.assertions.FilterAction',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='FILTER_ACTION_UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FILTER_ACTION_PERMIT', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FILTER_ACTION_DENY', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=2583,
  serialized_end=2674,
)
_sym_db.RegisterEnumDescriptor(_FILTERACTION)

FilterAction = enum_type_wrapper.EnumTypeWrapper(_FILTERACTION)
FILTER_ACTION_UNKNOWN = 0
FILTER_ACTION_PERMIT = 1
FILTER_ACTION_DENY = 2



_CROSSZONEPOLICYFILTERSFLOWSASSERTIONINPUT = _descriptor.Descriptor(
  name='CrossZonePolicyFiltersFlowsAssertionInput',
  full_name='com.intentionet.bfe.assertions.CrossZonePolicyFiltersFlowsAssertionInput',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='firewalls', full_name='com.intentionet.bfe.assertions.CrossZonePolicyFiltersFlowsAssertionInput.firewalls', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='firewalls', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='flows', full_name='com.intentionet.bfe.assertions.CrossZonePolicyFiltersFlowsAssertionInput.flows', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='flows', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='from', full_name='com.intentionet.bfe.assertions.CrossZonePolicyFiltersFlowsAssertionInput.from', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='from', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='to', full_name='com.intentionet.bfe.assertions.CrossZonePolicyFiltersFlowsAssertionInput.to', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='to', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='expect', full_name='com.intentionet.bfe.assertions.CrossZonePolicyFiltersFlowsAssertionInput.expect', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='expect', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=275,
  serialized_end=702,
)


_CROSSZONEPOLICYFILTERSFLOWSASSERTIONRESULT_ELEMENT = _descriptor.Descriptor(
  name='Element',
  full_name='com.intentionet.bfe.assertions.CrossZonePolicyFiltersFlowsAssertionResult.Element',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='device', full_name='com.intentionet.bfe.assertions.CrossZonePolicyFiltersFlowsAssertionResult.Element.device', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='device', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='flow', full_name='com.intentionet.bfe.assertions.CrossZonePolicyFiltersFlowsAssertionResult.Element.flow', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='flow', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='action', full_name='com.intentionet.bfe.assertions.CrossZonePolicyFiltersFlowsAssertionResult.Element.action', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='action', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='filter', full_name='com.intentionet.bfe.assertions.CrossZonePolicyFiltersFlowsAssertionResult.Element.filter', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='filter', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='test_filters', full_name='com.intentionet.bfe.assertions.CrossZonePolicyFiltersFlowsAssertionResult.Element.test_filters', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='testFilters', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='description_index', full_name='com.intentionet.bfe.assertions.CrossZonePolicyFiltersFlowsAssertionResult.Element.description_index', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='descriptionIndex', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1035,
  serialized_end=1431,
)

_CROSSZONEPOLICYFILTERSFLOWSASSERTIONRESULT_FAILURERESULT = _descriptor.Descriptor(
  name='FailureResult',
  full_name='com.intentionet.bfe.assertions.CrossZonePolicyFiltersFlowsAssertionResult.FailureResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='device', full_name='com.intentionet.bfe.assertions.CrossZonePolicyFiltersFlowsAssertionResult.FailureResult.device', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='device', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='reason', full_name='com.intentionet.bfe.assertions.CrossZonePolicyFiltersFlowsAssertionResult.FailureResult.reason', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='reason', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1433,
  serialized_end=1531,
)

_CROSSZONEPOLICYFILTERSFLOWSASSERTIONRESULT = _descriptor.Descriptor(
  name='CrossZonePolicyFiltersFlowsAssertionResult',
  full_name='com.intentionet.bfe.assertions.CrossZonePolicyFiltersFlowsAssertionResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='violators', full_name='com.intentionet.bfe.assertions.CrossZonePolicyFiltersFlowsAssertionResult.violators', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='violators', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='conformers', full_name='com.intentionet.bfe.assertions.CrossZonePolicyFiltersFlowsAssertionResult.conformers', index=1,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='conformers', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='violator_descriptions', full_name='com.intentionet.bfe.assertions.CrossZonePolicyFiltersFlowsAssertionResult.violator_descriptions', index=2,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='violatorDescriptions', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_CROSSZONEPOLICYFILTERSFLOWSASSERTIONRESULT_ELEMENT, _CROSSZONEPOLICYFILTERSFLOWSASSERTIONRESULT_FAILURERESULT, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=705,
  serialized_end=1543,
)


_FILTERBEHAVIORASSERTIONINPUT = _descriptor.Descriptor(
  name='FilterBehaviorAssertionInput',
  full_name='com.intentionet.bfe.assertions.FilterBehaviorAssertionInput',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='devices', full_name='com.intentionet.bfe.assertions.FilterBehaviorAssertionInput.devices', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='devices', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='filters', full_name='com.intentionet.bfe.assertions.FilterBehaviorAssertionInput.filters', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='filters', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='flows', full_name='com.intentionet.bfe.assertions.FilterBehaviorAssertionInput.flows', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='flows', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='expect', full_name='com.intentionet.bfe.assertions.FilterBehaviorAssertionInput.expect', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='expect', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1546,
  serialized_end=1875,
)


_FILTERBEHAVIORASSERTIONRESULT_ELEMENT = _descriptor.Descriptor(
  name='Element',
  full_name='com.intentionet.bfe.assertions.FilterBehaviorAssertionResult.Element',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='filter', full_name='com.intentionet.bfe.assertions.FilterBehaviorAssertionResult.Element.filter', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='filter', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='flow', full_name='com.intentionet.bfe.assertions.FilterBehaviorAssertionResult.Element.flow', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='flow', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='test_filters', full_name='com.intentionet.bfe.assertions.FilterBehaviorAssertionResult.Element.test_filters', index=2,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='testFilters', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='description_index', full_name='com.intentionet.bfe.assertions.FilterBehaviorAssertionResult.Element.description_index', index=3,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='descriptionIndex', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=2169,
  serialized_end=2485,
)

_FILTERBEHAVIORASSERTIONRESULT = _descriptor.Descriptor(
  name='FilterBehaviorAssertionResult',
  full_name='com.intentionet.bfe.assertions.FilterBehaviorAssertionResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='violators', full_name='com.intentionet.bfe.assertions.FilterBehaviorAssertionResult.violators', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='violators', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='conformers', full_name='com.intentionet.bfe.assertions.FilterBehaviorAssertionResult.conformers', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='conformers', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='violator_descriptions', full_name='com.intentionet.bfe.assertions.FilterBehaviorAssertionResult.violator_descriptions', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='violatorDescriptions', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_FILTERBEHAVIORASSERTIONRESULT_ELEMENT, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1878,
  serialized_end=2485,
)


_TESTFILTERSRESULT = _descriptor.Descriptor(
  name='TestFiltersResult',
  full_name='com.intentionet.bfe.assertions.TestFiltersResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='matched_line', full_name='com.intentionet.bfe.assertions.TestFiltersResult.matched_line', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='matchedLine', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='trace_tree_json', full_name='com.intentionet.bfe.assertions.TestFiltersResult.trace_tree_json', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='traceTreeJson', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=2487,
  serialized_end=2581,
)

_CROSSZONEPOLICYFILTERSFLOWSASSERTIONINPUT.fields_by_name['firewalls'].message_type = intentionet_dot_bfe_dot_proto_dot_assertions_dot_parameters__pb2._DEVICEFILTEREXPR
_CROSSZONEPOLICYFILTERSFLOWSASSERTIONINPUT.fields_by_name['flows'].message_type = intentionet_dot_bfe_dot_proto_dot_assertions_dot_parameters__pb2._FLOWFILTEREXPR
_CROSSZONEPOLICYFILTERSFLOWSASSERTIONINPUT.fields_by_name['from'].message_type = intentionet_dot_bfe_dot_proto_dot_assertions_dot_parameters__pb2._FIREWALLLOCATIONMATCHEXPR
_CROSSZONEPOLICYFILTERSFLOWSASSERTIONINPUT.fields_by_name['to'].message_type = intentionet_dot_bfe_dot_proto_dot_assertions_dot_parameters__pb2._FIREWALLLOCATIONMATCHEXPR
_CROSSZONEPOLICYFILTERSFLOWSASSERTIONINPUT.fields_by_name['expect'].message_type = intentionet_dot_bfe_dot_proto_dot_assertions_dot_parameters__pb2._FIREWALLBEHAVIOREXPECT
_CROSSZONEPOLICYFILTERSFLOWSASSERTIONRESULT_ELEMENT.fields_by_name['device'].message_type = intentionet_dot_bfe_dot_proto_dot_datamodel_dot_device__pb2._DEVICE
_CROSSZONEPOLICYFILTERSFLOWSASSERTIONRESULT_ELEMENT.fields_by_name['flow'].message_type = intentionet_dot_bfe_dot_proto_dot_datamodel_dot_flow__pb2._FLOW
_CROSSZONEPOLICYFILTERSFLOWSASSERTIONRESULT_ELEMENT.fields_by_name['action'].enum_type = _FILTERACTION
_CROSSZONEPOLICYFILTERSFLOWSASSERTIONRESULT_ELEMENT.fields_by_name['test_filters'].message_type = _TESTFILTERSRESULT
_CROSSZONEPOLICYFILTERSFLOWSASSERTIONRESULT_ELEMENT.fields_by_name['description_index'].message_type = intentionet_dot_bfe_dot_proto_dot_assertions_dot_violations__pb2._DESCRIPTIONINDEX
_CROSSZONEPOLICYFILTERSFLOWSASSERTIONRESULT_ELEMENT.containing_type = _CROSSZONEPOLICYFILTERSFLOWSASSERTIONRESULT
_CROSSZONEPOLICYFILTERSFLOWSASSERTIONRESULT_FAILURERESULT.fields_by_name['device'].message_type = intentionet_dot_bfe_dot_proto_dot_datamodel_dot_device__pb2._DEVICE
_CROSSZONEPOLICYFILTERSFLOWSASSERTIONRESULT_FAILURERESULT.containing_type = _CROSSZONEPOLICYFILTERSFLOWSASSERTIONRESULT
_CROSSZONEPOLICYFILTERSFLOWSASSERTIONRESULT.fields_by_name['violators'].message_type = _CROSSZONEPOLICYFILTERSFLOWSASSERTIONRESULT_ELEMENT
_CROSSZONEPOLICYFILTERSFLOWSASSERTIONRESULT.fields_by_name['conformers'].message_type = _CROSSZONEPOLICYFILTERSFLOWSASSERTIONRESULT_ELEMENT
_FILTERBEHAVIORASSERTIONINPUT.fields_by_name['devices'].message_type = intentionet_dot_bfe_dot_proto_dot_assertions_dot_parameters__pb2._DEVICEFILTEREXPR
_FILTERBEHAVIORASSERTIONINPUT.fields_by_name['filters'].message_type = intentionet_dot_bfe_dot_proto_dot_assertions_dot_parameters__pb2._FILTERMATCHEXPR
_FILTERBEHAVIORASSERTIONINPUT.fields_by_name['flows'].message_type = intentionet_dot_bfe_dot_proto_dot_assertions_dot_parameters__pb2._FLOWFILTEREXPR
_FILTERBEHAVIORASSERTIONINPUT.fields_by_name['expect'].message_type = intentionet_dot_bfe_dot_proto_dot_assertions_dot_parameters__pb2._FILTERBEHAVIOREXPECT
_FILTERBEHAVIORASSERTIONRESULT_ELEMENT.fields_by_name['filter'].message_type = intentionet_dot_bfe_dot_proto_dot_datamodel_dot_device__pb2._FILTER
_FILTERBEHAVIORASSERTIONRESULT_ELEMENT.fields_by_name['flow'].message_type = intentionet_dot_bfe_dot_proto_dot_datamodel_dot_flow__pb2._FLOW
_FILTERBEHAVIORASSERTIONRESULT_ELEMENT.fields_by_name['test_filters'].message_type = _TESTFILTERSRESULT
_FILTERBEHAVIORASSERTIONRESULT_ELEMENT.fields_by_name['description_index'].message_type = intentionet_dot_bfe_dot_proto_dot_assertions_dot_violations__pb2._DESCRIPTIONINDEX
_FILTERBEHAVIORASSERTIONRESULT_ELEMENT.containing_type = _FILTERBEHAVIORASSERTIONRESULT
_FILTERBEHAVIORASSERTIONRESULT.fields_by_name['violators'].message_type = _FILTERBEHAVIORASSERTIONRESULT_ELEMENT
_FILTERBEHAVIORASSERTIONRESULT.fields_by_name['conformers'].message_type = _FILTERBEHAVIORASSERTIONRESULT_ELEMENT
DESCRIPTOR.message_types_by_name['CrossZonePolicyFiltersFlowsAssertionInput'] = _CROSSZONEPOLICYFILTERSFLOWSASSERTIONINPUT
DESCRIPTOR.message_types_by_name['CrossZonePolicyFiltersFlowsAssertionResult'] = _CROSSZONEPOLICYFILTERSFLOWSASSERTIONRESULT
DESCRIPTOR.message_types_by_name['FilterBehaviorAssertionInput'] = _FILTERBEHAVIORASSERTIONINPUT
DESCRIPTOR.message_types_by_name['FilterBehaviorAssertionResult'] = _FILTERBEHAVIORASSERTIONRESULT
DESCRIPTOR.message_types_by_name['TestFiltersResult'] = _TESTFILTERSRESULT
DESCRIPTOR.enum_types_by_name['FilterAction'] = _FILTERACTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CrossZonePolicyFiltersFlowsAssertionInput = _reflection.GeneratedProtocolMessageType('CrossZonePolicyFiltersFlowsAssertionInput', (_message.Message,), {
  'DESCRIPTOR' : _CROSSZONEPOLICYFILTERSFLOWSASSERTIONINPUT,
  '__module__' : 'intentionet.bfe.proto.assertions.filters_pb2'
  # @@protoc_insertion_point(class_scope:com.intentionet.bfe.assertions.CrossZonePolicyFiltersFlowsAssertionInput)
  })
_sym_db.RegisterMessage(CrossZonePolicyFiltersFlowsAssertionInput)

CrossZonePolicyFiltersFlowsAssertionResult = _reflection.GeneratedProtocolMessageType('CrossZonePolicyFiltersFlowsAssertionResult', (_message.Message,), {

  'Element' : _reflection.GeneratedProtocolMessageType('Element', (_message.Message,), {
    'DESCRIPTOR' : _CROSSZONEPOLICYFILTERSFLOWSASSERTIONRESULT_ELEMENT,
    '__module__' : 'intentionet.bfe.proto.assertions.filters_pb2'
    # @@protoc_insertion_point(class_scope:com.intentionet.bfe.assertions.CrossZonePolicyFiltersFlowsAssertionResult.Element)
    })
  ,

  'FailureResult' : _reflection.GeneratedProtocolMessageType('FailureResult', (_message.Message,), {
    'DESCRIPTOR' : _CROSSZONEPOLICYFILTERSFLOWSASSERTIONRESULT_FAILURERESULT,
    '__module__' : 'intentionet.bfe.proto.assertions.filters_pb2'
    # @@protoc_insertion_point(class_scope:com.intentionet.bfe.assertions.CrossZonePolicyFiltersFlowsAssertionResult.FailureResult)
    })
  ,
  'DESCRIPTOR' : _CROSSZONEPOLICYFILTERSFLOWSASSERTIONRESULT,
  '__module__' : 'intentionet.bfe.proto.assertions.filters_pb2'
  # @@protoc_insertion_point(class_scope:com.intentionet.bfe.assertions.CrossZonePolicyFiltersFlowsAssertionResult)
  })
_sym_db.RegisterMessage(CrossZonePolicyFiltersFlowsAssertionResult)
_sym_db.RegisterMessage(CrossZonePolicyFiltersFlowsAssertionResult.Element)
_sym_db.RegisterMessage(CrossZonePolicyFiltersFlowsAssertionResult.FailureResult)

FilterBehaviorAssertionInput = _reflection.GeneratedProtocolMessageType('FilterBehaviorAssertionInput', (_message.Message,), {
  'DESCRIPTOR' : _FILTERBEHAVIORASSERTIONINPUT,
  '__module__' : 'intentionet.bfe.proto.assertions.filters_pb2'
  # @@protoc_insertion_point(class_scope:com.intentionet.bfe.assertions.FilterBehaviorAssertionInput)
  })
_sym_db.RegisterMessage(FilterBehaviorAssertionInput)

FilterBehaviorAssertionResult = _reflection.GeneratedProtocolMessageType('FilterBehaviorAssertionResult', (_message.Message,), {

  'Element' : _reflection.GeneratedProtocolMessageType('Element', (_message.Message,), {
    'DESCRIPTOR' : _FILTERBEHAVIORASSERTIONRESULT_ELEMENT,
    '__module__' : 'intentionet.bfe.proto.assertions.filters_pb2'
    # @@protoc_insertion_point(class_scope:com.intentionet.bfe.assertions.FilterBehaviorAssertionResult.Element)
    })
  ,
  'DESCRIPTOR' : _FILTERBEHAVIORASSERTIONRESULT,
  '__module__' : 'intentionet.bfe.proto.assertions.filters_pb2'
  # @@protoc_insertion_point(class_scope:com.intentionet.bfe.assertions.FilterBehaviorAssertionResult)
  })
_sym_db.RegisterMessage(FilterBehaviorAssertionResult)
_sym_db.RegisterMessage(FilterBehaviorAssertionResult.Element)

TestFiltersResult = _reflection.GeneratedProtocolMessageType('TestFiltersResult', (_message.Message,), {
  'DESCRIPTOR' : _TESTFILTERSRESULT,
  '__module__' : 'intentionet.bfe.proto.assertions.filters_pb2'
  # @@protoc_insertion_point(class_scope:com.intentionet.bfe.assertions.TestFiltersResult)
  })
_sym_db.RegisterMessage(TestFiltersResult)


# @@protoc_insertion_point(module_scope)
