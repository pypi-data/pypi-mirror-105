# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: flyteidl/core/workflow_closure.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from flyteidl.core import workflow_pb2 as flyteidl_dot_core_dot_workflow__pb2
from flyteidl.core import tasks_pb2 as flyteidl_dot_core_dot_tasks__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='flyteidl/core/workflow_closure.proto',
  package='flyteidl.core',
  syntax='proto3',
  serialized_options=_b('Z4github.com/flyteorg/flyteidl/gen/pb-go/flyteidl/core'),
  serialized_pb=_b('\n$flyteidl/core/workflow_closure.proto\x12\rflyteidl.core\x1a\x1c\x66lyteidl/core/workflow.proto\x1a\x19\x66lyteidl/core/tasks.proto\"p\n\x0fWorkflowClosure\x12\x31\n\x08workflow\x18\x01 \x01(\x0b\x32\x1f.flyteidl.core.WorkflowTemplate\x12*\n\x05tasks\x18\x02 \x03(\x0b\x32\x1b.flyteidl.core.TaskTemplateB6Z4github.com/flyteorg/flyteidl/gen/pb-go/flyteidl/coreb\x06proto3')
  ,
  dependencies=[flyteidl_dot_core_dot_workflow__pb2.DESCRIPTOR,flyteidl_dot_core_dot_tasks__pb2.DESCRIPTOR,])




_WORKFLOWCLOSURE = _descriptor.Descriptor(
  name='WorkflowClosure',
  full_name='flyteidl.core.WorkflowClosure',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='workflow', full_name='flyteidl.core.WorkflowClosure.workflow', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tasks', full_name='flyteidl.core.WorkflowClosure.tasks', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=112,
  serialized_end=224,
)

_WORKFLOWCLOSURE.fields_by_name['workflow'].message_type = flyteidl_dot_core_dot_workflow__pb2._WORKFLOWTEMPLATE
_WORKFLOWCLOSURE.fields_by_name['tasks'].message_type = flyteidl_dot_core_dot_tasks__pb2._TASKTEMPLATE
DESCRIPTOR.message_types_by_name['WorkflowClosure'] = _WORKFLOWCLOSURE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

WorkflowClosure = _reflection.GeneratedProtocolMessageType('WorkflowClosure', (_message.Message,), dict(
  DESCRIPTOR = _WORKFLOWCLOSURE,
  __module__ = 'flyteidl.core.workflow_closure_pb2'
  # @@protoc_insertion_point(class_scope:flyteidl.core.WorkflowClosure)
  ))
_sym_db.RegisterMessage(WorkflowClosure)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
