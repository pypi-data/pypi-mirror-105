# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: flyteidl/plugins/sagemaker/parameter_ranges.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='flyteidl/plugins/sagemaker/parameter_ranges.proto',
  package='flyteidl.plugins.sagemaker',
  syntax='proto3',
  serialized_options=_b('Z7github.com/flyteorg/flyteidl/gen/pb-go/flyteidl/plugins'),
  serialized_pb=_b('\n1flyteidl/plugins/sagemaker/parameter_ranges.proto\x12\x1a\x66lyteidl.plugins.sagemaker\"c\n\x19HyperparameterScalingType\"F\n\x05Value\x12\x08\n\x04\x41UTO\x10\x00\x12\n\n\x06LINEAR\x10\x01\x12\x0f\n\x0bLOGARITHMIC\x10\x02\x12\x16\n\x12REVERSELOGARITHMIC\x10\x03\"\x93\x01\n\x18\x43ontinuousParameterRange\x12\x11\n\tmax_value\x18\x01 \x01(\x01\x12\x11\n\tmin_value\x18\x02 \x01(\x01\x12Q\n\x0cscaling_type\x18\x03 \x01(\x0e\x32;.flyteidl.plugins.sagemaker.HyperparameterScalingType.Value\"\x90\x01\n\x15IntegerParameterRange\x12\x11\n\tmax_value\x18\x01 \x01(\x03\x12\x11\n\tmin_value\x18\x02 \x01(\x03\x12Q\n\x0cscaling_type\x18\x03 \x01(\x0e\x32;.flyteidl.plugins.sagemaker.HyperparameterScalingType.Value\"+\n\x19\x43\x61tegoricalParameterRange\x12\x0e\n\x06values\x18\x01 \x03(\t\"\xbd\x02\n\x13ParameterRangeOneOf\x12Z\n\x1a\x63ontinuous_parameter_range\x18\x01 \x01(\x0b\x32\x34.flyteidl.plugins.sagemaker.ContinuousParameterRangeH\x00\x12T\n\x17integer_parameter_range\x18\x02 \x01(\x0b\x32\x31.flyteidl.plugins.sagemaker.IntegerParameterRangeH\x00\x12\\\n\x1b\x63\x61tegorical_parameter_range\x18\x03 \x01(\x0b\x32\x35.flyteidl.plugins.sagemaker.CategoricalParameterRangeH\x00\x42\x16\n\x14parameter_range_type\"\xdd\x01\n\x0fParameterRanges\x12_\n\x13parameter_range_map\x18\x01 \x03(\x0b\x32\x42.flyteidl.plugins.sagemaker.ParameterRanges.ParameterRangeMapEntry\x1ai\n\x16ParameterRangeMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12>\n\x05value\x18\x02 \x01(\x0b\x32/.flyteidl.plugins.sagemaker.ParameterRangeOneOf:\x02\x38\x01\x42\x39Z7github.com/flyteorg/flyteidl/gen/pb-go/flyteidl/pluginsb\x06proto3')
)



_HYPERPARAMETERSCALINGTYPE_VALUE = _descriptor.EnumDescriptor(
  name='Value',
  full_name='flyteidl.plugins.sagemaker.HyperparameterScalingType.Value',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='AUTO', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LINEAR', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LOGARITHMIC', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REVERSELOGARITHMIC', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=110,
  serialized_end=180,
)
_sym_db.RegisterEnumDescriptor(_HYPERPARAMETERSCALINGTYPE_VALUE)


_HYPERPARAMETERSCALINGTYPE = _descriptor.Descriptor(
  name='HyperparameterScalingType',
  full_name='flyteidl.plugins.sagemaker.HyperparameterScalingType',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _HYPERPARAMETERSCALINGTYPE_VALUE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=81,
  serialized_end=180,
)


_CONTINUOUSPARAMETERRANGE = _descriptor.Descriptor(
  name='ContinuousParameterRange',
  full_name='flyteidl.plugins.sagemaker.ContinuousParameterRange',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='max_value', full_name='flyteidl.plugins.sagemaker.ContinuousParameterRange.max_value', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='min_value', full_name='flyteidl.plugins.sagemaker.ContinuousParameterRange.min_value', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='scaling_type', full_name='flyteidl.plugins.sagemaker.ContinuousParameterRange.scaling_type', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=183,
  serialized_end=330,
)


_INTEGERPARAMETERRANGE = _descriptor.Descriptor(
  name='IntegerParameterRange',
  full_name='flyteidl.plugins.sagemaker.IntegerParameterRange',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='max_value', full_name='flyteidl.plugins.sagemaker.IntegerParameterRange.max_value', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='min_value', full_name='flyteidl.plugins.sagemaker.IntegerParameterRange.min_value', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='scaling_type', full_name='flyteidl.plugins.sagemaker.IntegerParameterRange.scaling_type', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=333,
  serialized_end=477,
)


_CATEGORICALPARAMETERRANGE = _descriptor.Descriptor(
  name='CategoricalParameterRange',
  full_name='flyteidl.plugins.sagemaker.CategoricalParameterRange',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='values', full_name='flyteidl.plugins.sagemaker.CategoricalParameterRange.values', index=0,
      number=1, type=9, cpp_type=9, label=3,
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
  serialized_start=479,
  serialized_end=522,
)


_PARAMETERRANGEONEOF = _descriptor.Descriptor(
  name='ParameterRangeOneOf',
  full_name='flyteidl.plugins.sagemaker.ParameterRangeOneOf',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='continuous_parameter_range', full_name='flyteidl.plugins.sagemaker.ParameterRangeOneOf.continuous_parameter_range', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='integer_parameter_range', full_name='flyteidl.plugins.sagemaker.ParameterRangeOneOf.integer_parameter_range', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='categorical_parameter_range', full_name='flyteidl.plugins.sagemaker.ParameterRangeOneOf.categorical_parameter_range', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
    _descriptor.OneofDescriptor(
      name='parameter_range_type', full_name='flyteidl.plugins.sagemaker.ParameterRangeOneOf.parameter_range_type',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=525,
  serialized_end=842,
)


_PARAMETERRANGES_PARAMETERRANGEMAPENTRY = _descriptor.Descriptor(
  name='ParameterRangeMapEntry',
  full_name='flyteidl.plugins.sagemaker.ParameterRanges.ParameterRangeMapEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='flyteidl.plugins.sagemaker.ParameterRanges.ParameterRangeMapEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='flyteidl.plugins.sagemaker.ParameterRanges.ParameterRangeMapEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=961,
  serialized_end=1066,
)

_PARAMETERRANGES = _descriptor.Descriptor(
  name='ParameterRanges',
  full_name='flyteidl.plugins.sagemaker.ParameterRanges',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='parameter_range_map', full_name='flyteidl.plugins.sagemaker.ParameterRanges.parameter_range_map', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_PARAMETERRANGES_PARAMETERRANGEMAPENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=845,
  serialized_end=1066,
)

_HYPERPARAMETERSCALINGTYPE_VALUE.containing_type = _HYPERPARAMETERSCALINGTYPE
_CONTINUOUSPARAMETERRANGE.fields_by_name['scaling_type'].enum_type = _HYPERPARAMETERSCALINGTYPE_VALUE
_INTEGERPARAMETERRANGE.fields_by_name['scaling_type'].enum_type = _HYPERPARAMETERSCALINGTYPE_VALUE
_PARAMETERRANGEONEOF.fields_by_name['continuous_parameter_range'].message_type = _CONTINUOUSPARAMETERRANGE
_PARAMETERRANGEONEOF.fields_by_name['integer_parameter_range'].message_type = _INTEGERPARAMETERRANGE
_PARAMETERRANGEONEOF.fields_by_name['categorical_parameter_range'].message_type = _CATEGORICALPARAMETERRANGE
_PARAMETERRANGEONEOF.oneofs_by_name['parameter_range_type'].fields.append(
  _PARAMETERRANGEONEOF.fields_by_name['continuous_parameter_range'])
_PARAMETERRANGEONEOF.fields_by_name['continuous_parameter_range'].containing_oneof = _PARAMETERRANGEONEOF.oneofs_by_name['parameter_range_type']
_PARAMETERRANGEONEOF.oneofs_by_name['parameter_range_type'].fields.append(
  _PARAMETERRANGEONEOF.fields_by_name['integer_parameter_range'])
_PARAMETERRANGEONEOF.fields_by_name['integer_parameter_range'].containing_oneof = _PARAMETERRANGEONEOF.oneofs_by_name['parameter_range_type']
_PARAMETERRANGEONEOF.oneofs_by_name['parameter_range_type'].fields.append(
  _PARAMETERRANGEONEOF.fields_by_name['categorical_parameter_range'])
_PARAMETERRANGEONEOF.fields_by_name['categorical_parameter_range'].containing_oneof = _PARAMETERRANGEONEOF.oneofs_by_name['parameter_range_type']
_PARAMETERRANGES_PARAMETERRANGEMAPENTRY.fields_by_name['value'].message_type = _PARAMETERRANGEONEOF
_PARAMETERRANGES_PARAMETERRANGEMAPENTRY.containing_type = _PARAMETERRANGES
_PARAMETERRANGES.fields_by_name['parameter_range_map'].message_type = _PARAMETERRANGES_PARAMETERRANGEMAPENTRY
DESCRIPTOR.message_types_by_name['HyperparameterScalingType'] = _HYPERPARAMETERSCALINGTYPE
DESCRIPTOR.message_types_by_name['ContinuousParameterRange'] = _CONTINUOUSPARAMETERRANGE
DESCRIPTOR.message_types_by_name['IntegerParameterRange'] = _INTEGERPARAMETERRANGE
DESCRIPTOR.message_types_by_name['CategoricalParameterRange'] = _CATEGORICALPARAMETERRANGE
DESCRIPTOR.message_types_by_name['ParameterRangeOneOf'] = _PARAMETERRANGEONEOF
DESCRIPTOR.message_types_by_name['ParameterRanges'] = _PARAMETERRANGES
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

HyperparameterScalingType = _reflection.GeneratedProtocolMessageType('HyperparameterScalingType', (_message.Message,), dict(
  DESCRIPTOR = _HYPERPARAMETERSCALINGTYPE,
  __module__ = 'flyteidl.plugins.sagemaker.parameter_ranges_pb2'
  # @@protoc_insertion_point(class_scope:flyteidl.plugins.sagemaker.HyperparameterScalingType)
  ))
_sym_db.RegisterMessage(HyperparameterScalingType)

ContinuousParameterRange = _reflection.GeneratedProtocolMessageType('ContinuousParameterRange', (_message.Message,), dict(
  DESCRIPTOR = _CONTINUOUSPARAMETERRANGE,
  __module__ = 'flyteidl.plugins.sagemaker.parameter_ranges_pb2'
  # @@protoc_insertion_point(class_scope:flyteidl.plugins.sagemaker.ContinuousParameterRange)
  ))
_sym_db.RegisterMessage(ContinuousParameterRange)

IntegerParameterRange = _reflection.GeneratedProtocolMessageType('IntegerParameterRange', (_message.Message,), dict(
  DESCRIPTOR = _INTEGERPARAMETERRANGE,
  __module__ = 'flyteidl.plugins.sagemaker.parameter_ranges_pb2'
  # @@protoc_insertion_point(class_scope:flyteidl.plugins.sagemaker.IntegerParameterRange)
  ))
_sym_db.RegisterMessage(IntegerParameterRange)

CategoricalParameterRange = _reflection.GeneratedProtocolMessageType('CategoricalParameterRange', (_message.Message,), dict(
  DESCRIPTOR = _CATEGORICALPARAMETERRANGE,
  __module__ = 'flyteidl.plugins.sagemaker.parameter_ranges_pb2'
  # @@protoc_insertion_point(class_scope:flyteidl.plugins.sagemaker.CategoricalParameterRange)
  ))
_sym_db.RegisterMessage(CategoricalParameterRange)

ParameterRangeOneOf = _reflection.GeneratedProtocolMessageType('ParameterRangeOneOf', (_message.Message,), dict(
  DESCRIPTOR = _PARAMETERRANGEONEOF,
  __module__ = 'flyteidl.plugins.sagemaker.parameter_ranges_pb2'
  # @@protoc_insertion_point(class_scope:flyteidl.plugins.sagemaker.ParameterRangeOneOf)
  ))
_sym_db.RegisterMessage(ParameterRangeOneOf)

ParameterRanges = _reflection.GeneratedProtocolMessageType('ParameterRanges', (_message.Message,), dict(

  ParameterRangeMapEntry = _reflection.GeneratedProtocolMessageType('ParameterRangeMapEntry', (_message.Message,), dict(
    DESCRIPTOR = _PARAMETERRANGES_PARAMETERRANGEMAPENTRY,
    __module__ = 'flyteidl.plugins.sagemaker.parameter_ranges_pb2'
    # @@protoc_insertion_point(class_scope:flyteidl.plugins.sagemaker.ParameterRanges.ParameterRangeMapEntry)
    ))
  ,
  DESCRIPTOR = _PARAMETERRANGES,
  __module__ = 'flyteidl.plugins.sagemaker.parameter_ranges_pb2'
  # @@protoc_insertion_point(class_scope:flyteidl.plugins.sagemaker.ParameterRanges)
  ))
_sym_db.RegisterMessage(ParameterRanges)
_sym_db.RegisterMessage(ParameterRanges.ParameterRangeMapEntry)


DESCRIPTOR._options = None
_PARAMETERRANGES_PARAMETERRANGEMAPENTRY._options = None
# @@protoc_insertion_point(module_scope)
