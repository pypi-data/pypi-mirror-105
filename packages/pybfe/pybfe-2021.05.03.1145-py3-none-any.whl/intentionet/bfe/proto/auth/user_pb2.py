# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: intentionet/bfe/proto/auth/user.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from intentionet.bfe.proto.auth import credentials_pb2 as intentionet_dot_bfe_dot_proto_dot_auth_dot_credentials__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='intentionet/bfe/proto/auth/user.proto',
  package='com.intentionet.bfe.proto.auth',
  syntax='proto3',
  serialized_options=b'\n\036com.intentionet.bfe.proto.authP\001Z\036intentionet.com/bfe/proto/auth',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n%intentionet/bfe/proto/auth/user.proto\x12\x1e\x63om.intentionet.bfe.proto.auth\x1a,intentionet/bfe/proto/auth/credentials.proto\"\x18\n\x06UserId\x12\x0e\n\x02id\x18\x01 \x01(\x04R\x02id\"\x1e\n\x08Username\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\"\xe6\x01\n\nUserRecord\x12\x38\n\x03uid\x18\x01 \x01(\x0b\x32&.com.intentionet.bfe.proto.auth.UserIdR\x03uid\x12\x44\n\x08username\x18\x02 \x01(\x0b\x32(.com.intentionet.bfe.proto.auth.UsernameR\x08username\x12X\n\x10web_access_token\x18\x03 \x01(\x0b\x32..com.intentionet.bfe.proto.auth.WebAccessTokenR\x0ewebAccessTokenBB\n\x1e\x63om.intentionet.bfe.proto.authP\x01Z\x1eintentionet.com/bfe/proto/authb\x06proto3'
  ,
  dependencies=[intentionet_dot_bfe_dot_proto_dot_auth_dot_credentials__pb2.DESCRIPTOR,])




_USERID = _descriptor.Descriptor(
  name='UserId',
  full_name='com.intentionet.bfe.proto.auth.UserId',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='com.intentionet.bfe.proto.auth.UserId.id', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='id', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=119,
  serialized_end=143,
)


_USERNAME = _descriptor.Descriptor(
  name='Username',
  full_name='com.intentionet.bfe.proto.auth.Username',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='com.intentionet.bfe.proto.auth.Username.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='name', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=145,
  serialized_end=175,
)


_USERRECORD = _descriptor.Descriptor(
  name='UserRecord',
  full_name='com.intentionet.bfe.proto.auth.UserRecord',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='com.intentionet.bfe.proto.auth.UserRecord.uid', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='uid', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='username', full_name='com.intentionet.bfe.proto.auth.UserRecord.username', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='username', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='web_access_token', full_name='com.intentionet.bfe.proto.auth.UserRecord.web_access_token', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='webAccessToken', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=178,
  serialized_end=408,
)

_USERRECORD.fields_by_name['uid'].message_type = _USERID
_USERRECORD.fields_by_name['username'].message_type = _USERNAME
_USERRECORD.fields_by_name['web_access_token'].message_type = intentionet_dot_bfe_dot_proto_dot_auth_dot_credentials__pb2._WEBACCESSTOKEN
DESCRIPTOR.message_types_by_name['UserId'] = _USERID
DESCRIPTOR.message_types_by_name['Username'] = _USERNAME
DESCRIPTOR.message_types_by_name['UserRecord'] = _USERRECORD
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UserId = _reflection.GeneratedProtocolMessageType('UserId', (_message.Message,), {
  'DESCRIPTOR' : _USERID,
  '__module__' : 'intentionet.bfe.proto.auth.user_pb2'
  # @@protoc_insertion_point(class_scope:com.intentionet.bfe.proto.auth.UserId)
  })
_sym_db.RegisterMessage(UserId)

Username = _reflection.GeneratedProtocolMessageType('Username', (_message.Message,), {
  'DESCRIPTOR' : _USERNAME,
  '__module__' : 'intentionet.bfe.proto.auth.user_pb2'
  # @@protoc_insertion_point(class_scope:com.intentionet.bfe.proto.auth.Username)
  })
_sym_db.RegisterMessage(Username)

UserRecord = _reflection.GeneratedProtocolMessageType('UserRecord', (_message.Message,), {
  'DESCRIPTOR' : _USERRECORD,
  '__module__' : 'intentionet.bfe.proto.auth.user_pb2'
  # @@protoc_insertion_point(class_scope:com.intentionet.bfe.proto.auth.UserRecord)
  })
_sym_db.RegisterMessage(UserRecord)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
