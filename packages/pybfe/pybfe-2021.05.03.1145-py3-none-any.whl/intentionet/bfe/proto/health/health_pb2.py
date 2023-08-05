# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: intentionet/bfe/proto/health/health.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='intentionet/bfe/proto/health/health.proto',
  package='com.intentionet.bfe.proto.health',
  syntax='proto3',
  serialized_options=b'\n com.intentionet.bfe.proto.healthP\001Z intentionet.com/bfe/proto/health',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n)intentionet/bfe/proto/health/health.proto\x12 com.intentionet.bfe.proto.health\".\n\x12HealthCheckRequest\x12\x18\n\x07service\x18\x01 \x01(\tR\x07service\"\xdb\x01\n\x13HealthCheckResponse\x12[\n\x06status\x18\x01 \x01(\x0e\x32\x43.com.intentionet.bfe.proto.health.HealthCheckResponse.ServingStatusR\x06status\"g\n\rServingStatus\x12\x1a\n\x16SERVING_STATUS_UNKNOWN\x10\x00\x12\x1a\n\x16SERVING_STATUS_SERVING\x10\x01\x12\x1e\n\x1aSERVING_STATUS_NOT_SERVING\x10\x02\x32\xf6\x01\n\x06Health\x12t\n\x05\x43heck\x12\x34.com.intentionet.bfe.proto.health.HealthCheckRequest\x1a\x35.com.intentionet.bfe.proto.health.HealthCheckResponse\x12v\n\x05Watch\x12\x34.com.intentionet.bfe.proto.health.HealthCheckRequest\x1a\x35.com.intentionet.bfe.proto.health.HealthCheckResponse0\x01\x42\x46\n com.intentionet.bfe.proto.healthP\x01Z intentionet.com/bfe/proto/healthb\x06proto3'
)



_HEALTHCHECKRESPONSE_SERVINGSTATUS = _descriptor.EnumDescriptor(
  name='ServingStatus',
  full_name='com.intentionet.bfe.proto.health.HealthCheckResponse.ServingStatus',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SERVING_STATUS_UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SERVING_STATUS_SERVING', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SERVING_STATUS_NOT_SERVING', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=244,
  serialized_end=347,
)
_sym_db.RegisterEnumDescriptor(_HEALTHCHECKRESPONSE_SERVINGSTATUS)


_HEALTHCHECKREQUEST = _descriptor.Descriptor(
  name='HealthCheckRequest',
  full_name='com.intentionet.bfe.proto.health.HealthCheckRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='service', full_name='com.intentionet.bfe.proto.health.HealthCheckRequest.service', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='service', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=79,
  serialized_end=125,
)


_HEALTHCHECKRESPONSE = _descriptor.Descriptor(
  name='HealthCheckResponse',
  full_name='com.intentionet.bfe.proto.health.HealthCheckResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='com.intentionet.bfe.proto.health.HealthCheckResponse.status', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='status', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _HEALTHCHECKRESPONSE_SERVINGSTATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=128,
  serialized_end=347,
)

_HEALTHCHECKRESPONSE.fields_by_name['status'].enum_type = _HEALTHCHECKRESPONSE_SERVINGSTATUS
_HEALTHCHECKRESPONSE_SERVINGSTATUS.containing_type = _HEALTHCHECKRESPONSE
DESCRIPTOR.message_types_by_name['HealthCheckRequest'] = _HEALTHCHECKREQUEST
DESCRIPTOR.message_types_by_name['HealthCheckResponse'] = _HEALTHCHECKRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

HealthCheckRequest = _reflection.GeneratedProtocolMessageType('HealthCheckRequest', (_message.Message,), {
  'DESCRIPTOR' : _HEALTHCHECKREQUEST,
  '__module__' : 'intentionet.bfe.proto.health.health_pb2'
  # @@protoc_insertion_point(class_scope:com.intentionet.bfe.proto.health.HealthCheckRequest)
  })
_sym_db.RegisterMessage(HealthCheckRequest)

HealthCheckResponse = _reflection.GeneratedProtocolMessageType('HealthCheckResponse', (_message.Message,), {
  'DESCRIPTOR' : _HEALTHCHECKRESPONSE,
  '__module__' : 'intentionet.bfe.proto.health.health_pb2'
  # @@protoc_insertion_point(class_scope:com.intentionet.bfe.proto.health.HealthCheckResponse)
  })
_sym_db.RegisterMessage(HealthCheckResponse)


DESCRIPTOR._options = None

_HEALTH = _descriptor.ServiceDescriptor(
  name='Health',
  full_name='com.intentionet.bfe.proto.health.Health',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=350,
  serialized_end=596,
  methods=[
  _descriptor.MethodDescriptor(
    name='Check',
    full_name='com.intentionet.bfe.proto.health.Health.Check',
    index=0,
    containing_service=None,
    input_type=_HEALTHCHECKREQUEST,
    output_type=_HEALTHCHECKRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Watch',
    full_name='com.intentionet.bfe.proto.health.Health.Watch',
    index=1,
    containing_service=None,
    input_type=_HEALTHCHECKREQUEST,
    output_type=_HEALTHCHECKRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_HEALTH)

DESCRIPTOR.services_by_name['Health'] = _HEALTH

# @@protoc_insertion_point(module_scope)
