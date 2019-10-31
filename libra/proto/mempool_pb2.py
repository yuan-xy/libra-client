# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mempool.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import transaction_pb2 as transaction__pb2
import mempool_status_pb2 as mempool__status__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='mempool.proto',
  package='mempool',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\rmempool.proto\x12\x07mempool\x1a\x11transaction.proto\x1a\x14mempool_status.proto\"\xa3\x01\n#AddTransactionWithValidationRequest\x12-\n\x0btransaction\x18\x01 \x01(\x0b\x32\x18.types.SignedTransaction\x12\x14\n\x0cmax_gas_cost\x18\x02 \x01(\x04\x12\x1e\n\x16latest_sequence_number\x18\x03 \x01(\x04\x12\x17\n\x0f\x61\x63\x63ount_balance\x18\x04 \x01(\x04\"|\n$AddTransactionWithValidationResponse\x12\x17\n\x0f\x63urrent_version\x18\x01 \x01(\x04\x12;\n\x06status\x18\x02 \x01(\x0b\x32+.mempool_status.MempoolAddTransactionStatus\"^\n\x0fGetBlockRequest\x12\x16\n\x0emax_block_size\x18\x01 \x01(\x04\x12\x33\n\x0ctransactions\x18\x02 \x03(\x0b\x32\x1d.mempool.TransactionExclusion\"A\n\x10GetBlockResponse\x12-\n\x05\x62lock\x18\x01 \x01(\x0b\x32\x1e.types.SignedTransactionsBlock\"?\n\x14TransactionExclusion\x12\x0e\n\x06sender\x18\x01 \x01(\x0c\x12\x17\n\x0fsequence_number\x18\x02 \x01(\x04\"o\n\x19\x43ommitTransactionsRequest\x12\x33\n\x0ctransactions\x18\x01 \x03(\x0b\x32\x1d.mempool.CommittedTransaction\x12\x1d\n\x15\x62lock_timestamp_usecs\x18\x02 \x01(\x04\"\x1c\n\x1a\x43ommitTransactionsResponse\"T\n\x14\x43ommittedTransaction\x12\x0e\n\x06sender\x18\x01 \x01(\x0c\x12\x17\n\x0fsequence_number\x18\x02 \x01(\x04\x12\x13\n\x0bis_rejected\x18\x03 \x01(\x08\"\x14\n\x12HealthCheckRequest\")\n\x13HealthCheckResponse\x12\x12\n\nis_healthy\x18\x01 \x01(\x08\x32\xf8\x02\n\x07Mempool\x12}\n\x1c\x41\x64\x64TransactionWithValidation\x12,.mempool.AddTransactionWithValidationRequest\x1a-.mempool.AddTransactionWithValidationResponse\"\x00\x12\x41\n\x08GetBlock\x12\x18.mempool.GetBlockRequest\x1a\x19.mempool.GetBlockResponse\"\x00\x12_\n\x12\x43ommitTransactions\x12\".mempool.CommitTransactionsRequest\x1a#.mempool.CommitTransactionsResponse\"\x00\x12J\n\x0bHealthCheck\x12\x1b.mempool.HealthCheckRequest\x1a\x1c.mempool.HealthCheckResponse\"\x00\x62\x06proto3')
  ,
  dependencies=[transaction__pb2.DESCRIPTOR,mempool__status__pb2.DESCRIPTOR,])




_ADDTRANSACTIONWITHVALIDATIONREQUEST = _descriptor.Descriptor(
  name='AddTransactionWithValidationRequest',
  full_name='mempool.AddTransactionWithValidationRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='transaction', full_name='mempool.AddTransactionWithValidationRequest.transaction', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='max_gas_cost', full_name='mempool.AddTransactionWithValidationRequest.max_gas_cost', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='latest_sequence_number', full_name='mempool.AddTransactionWithValidationRequest.latest_sequence_number', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='account_balance', full_name='mempool.AddTransactionWithValidationRequest.account_balance', index=3,
      number=4, type=4, cpp_type=4, label=1,
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
  serialized_start=68,
  serialized_end=231,
)


_ADDTRANSACTIONWITHVALIDATIONRESPONSE = _descriptor.Descriptor(
  name='AddTransactionWithValidationResponse',
  full_name='mempool.AddTransactionWithValidationResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='current_version', full_name='mempool.AddTransactionWithValidationResponse.current_version', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='mempool.AddTransactionWithValidationResponse.status', index=1,
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
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=233,
  serialized_end=357,
)


_GETBLOCKREQUEST = _descriptor.Descriptor(
  name='GetBlockRequest',
  full_name='mempool.GetBlockRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='max_block_size', full_name='mempool.GetBlockRequest.max_block_size', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='transactions', full_name='mempool.GetBlockRequest.transactions', index=1,
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
  serialized_start=359,
  serialized_end=453,
)


_GETBLOCKRESPONSE = _descriptor.Descriptor(
  name='GetBlockResponse',
  full_name='mempool.GetBlockResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='block', full_name='mempool.GetBlockResponse.block', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  ],
  serialized_start=455,
  serialized_end=520,
)


_TRANSACTIONEXCLUSION = _descriptor.Descriptor(
  name='TransactionExclusion',
  full_name='mempool.TransactionExclusion',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sender', full_name='mempool.TransactionExclusion.sender', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sequence_number', full_name='mempool.TransactionExclusion.sequence_number', index=1,
      number=2, type=4, cpp_type=4, label=1,
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
  serialized_start=522,
  serialized_end=585,
)


_COMMITTRANSACTIONSREQUEST = _descriptor.Descriptor(
  name='CommitTransactionsRequest',
  full_name='mempool.CommitTransactionsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='transactions', full_name='mempool.CommitTransactionsRequest.transactions', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='block_timestamp_usecs', full_name='mempool.CommitTransactionsRequest.block_timestamp_usecs', index=1,
      number=2, type=4, cpp_type=4, label=1,
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
  serialized_start=587,
  serialized_end=698,
)


_COMMITTRANSACTIONSRESPONSE = _descriptor.Descriptor(
  name='CommitTransactionsResponse',
  full_name='mempool.CommitTransactionsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
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
  serialized_start=700,
  serialized_end=728,
)


_COMMITTEDTRANSACTION = _descriptor.Descriptor(
  name='CommittedTransaction',
  full_name='mempool.CommittedTransaction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sender', full_name='mempool.CommittedTransaction.sender', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sequence_number', full_name='mempool.CommittedTransaction.sequence_number', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_rejected', full_name='mempool.CommittedTransaction.is_rejected', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=730,
  serialized_end=814,
)


_HEALTHCHECKREQUEST = _descriptor.Descriptor(
  name='HealthCheckRequest',
  full_name='mempool.HealthCheckRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
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
  serialized_start=816,
  serialized_end=836,
)


_HEALTHCHECKRESPONSE = _descriptor.Descriptor(
  name='HealthCheckResponse',
  full_name='mempool.HealthCheckResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='is_healthy', full_name='mempool.HealthCheckResponse.is_healthy', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=838,
  serialized_end=879,
)

_ADDTRANSACTIONWITHVALIDATIONREQUEST.fields_by_name['transaction'].message_type = transaction__pb2._SIGNEDTRANSACTION
_ADDTRANSACTIONWITHVALIDATIONRESPONSE.fields_by_name['status'].message_type = mempool__status__pb2._MEMPOOLADDTRANSACTIONSTATUS
_GETBLOCKREQUEST.fields_by_name['transactions'].message_type = _TRANSACTIONEXCLUSION
_GETBLOCKRESPONSE.fields_by_name['block'].message_type = transaction__pb2._SIGNEDTRANSACTIONSBLOCK
_COMMITTRANSACTIONSREQUEST.fields_by_name['transactions'].message_type = _COMMITTEDTRANSACTION
DESCRIPTOR.message_types_by_name['AddTransactionWithValidationRequest'] = _ADDTRANSACTIONWITHVALIDATIONREQUEST
DESCRIPTOR.message_types_by_name['AddTransactionWithValidationResponse'] = _ADDTRANSACTIONWITHVALIDATIONRESPONSE
DESCRIPTOR.message_types_by_name['GetBlockRequest'] = _GETBLOCKREQUEST
DESCRIPTOR.message_types_by_name['GetBlockResponse'] = _GETBLOCKRESPONSE
DESCRIPTOR.message_types_by_name['TransactionExclusion'] = _TRANSACTIONEXCLUSION
DESCRIPTOR.message_types_by_name['CommitTransactionsRequest'] = _COMMITTRANSACTIONSREQUEST
DESCRIPTOR.message_types_by_name['CommitTransactionsResponse'] = _COMMITTRANSACTIONSRESPONSE
DESCRIPTOR.message_types_by_name['CommittedTransaction'] = _COMMITTEDTRANSACTION
DESCRIPTOR.message_types_by_name['HealthCheckRequest'] = _HEALTHCHECKREQUEST
DESCRIPTOR.message_types_by_name['HealthCheckResponse'] = _HEALTHCHECKRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AddTransactionWithValidationRequest = _reflection.GeneratedProtocolMessageType('AddTransactionWithValidationRequest', (_message.Message,), {
  'DESCRIPTOR' : _ADDTRANSACTIONWITHVALIDATIONREQUEST,
  '__module__' : 'mempool_pb2'
  # @@protoc_insertion_point(class_scope:mempool.AddTransactionWithValidationRequest)
  })
_sym_db.RegisterMessage(AddTransactionWithValidationRequest)

AddTransactionWithValidationResponse = _reflection.GeneratedProtocolMessageType('AddTransactionWithValidationResponse', (_message.Message,), {
  'DESCRIPTOR' : _ADDTRANSACTIONWITHVALIDATIONRESPONSE,
  '__module__' : 'mempool_pb2'
  # @@protoc_insertion_point(class_scope:mempool.AddTransactionWithValidationResponse)
  })
_sym_db.RegisterMessage(AddTransactionWithValidationResponse)

GetBlockRequest = _reflection.GeneratedProtocolMessageType('GetBlockRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETBLOCKREQUEST,
  '__module__' : 'mempool_pb2'
  # @@protoc_insertion_point(class_scope:mempool.GetBlockRequest)
  })
_sym_db.RegisterMessage(GetBlockRequest)

GetBlockResponse = _reflection.GeneratedProtocolMessageType('GetBlockResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETBLOCKRESPONSE,
  '__module__' : 'mempool_pb2'
  # @@protoc_insertion_point(class_scope:mempool.GetBlockResponse)
  })
_sym_db.RegisterMessage(GetBlockResponse)

TransactionExclusion = _reflection.GeneratedProtocolMessageType('TransactionExclusion', (_message.Message,), {
  'DESCRIPTOR' : _TRANSACTIONEXCLUSION,
  '__module__' : 'mempool_pb2'
  # @@protoc_insertion_point(class_scope:mempool.TransactionExclusion)
  })
_sym_db.RegisterMessage(TransactionExclusion)

CommitTransactionsRequest = _reflection.GeneratedProtocolMessageType('CommitTransactionsRequest', (_message.Message,), {
  'DESCRIPTOR' : _COMMITTRANSACTIONSREQUEST,
  '__module__' : 'mempool_pb2'
  # @@protoc_insertion_point(class_scope:mempool.CommitTransactionsRequest)
  })
_sym_db.RegisterMessage(CommitTransactionsRequest)

CommitTransactionsResponse = _reflection.GeneratedProtocolMessageType('CommitTransactionsResponse', (_message.Message,), {
  'DESCRIPTOR' : _COMMITTRANSACTIONSRESPONSE,
  '__module__' : 'mempool_pb2'
  # @@protoc_insertion_point(class_scope:mempool.CommitTransactionsResponse)
  })
_sym_db.RegisterMessage(CommitTransactionsResponse)

CommittedTransaction = _reflection.GeneratedProtocolMessageType('CommittedTransaction', (_message.Message,), {
  'DESCRIPTOR' : _COMMITTEDTRANSACTION,
  '__module__' : 'mempool_pb2'
  # @@protoc_insertion_point(class_scope:mempool.CommittedTransaction)
  })
_sym_db.RegisterMessage(CommittedTransaction)

HealthCheckRequest = _reflection.GeneratedProtocolMessageType('HealthCheckRequest', (_message.Message,), {
  'DESCRIPTOR' : _HEALTHCHECKREQUEST,
  '__module__' : 'mempool_pb2'
  # @@protoc_insertion_point(class_scope:mempool.HealthCheckRequest)
  })
_sym_db.RegisterMessage(HealthCheckRequest)

HealthCheckResponse = _reflection.GeneratedProtocolMessageType('HealthCheckResponse', (_message.Message,), {
  'DESCRIPTOR' : _HEALTHCHECKRESPONSE,
  '__module__' : 'mempool_pb2'
  # @@protoc_insertion_point(class_scope:mempool.HealthCheckResponse)
  })
_sym_db.RegisterMessage(HealthCheckResponse)



_MEMPOOL = _descriptor.ServiceDescriptor(
  name='Mempool',
  full_name='mempool.Mempool',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=882,
  serialized_end=1258,
  methods=[
  _descriptor.MethodDescriptor(
    name='AddTransactionWithValidation',
    full_name='mempool.Mempool.AddTransactionWithValidation',
    index=0,
    containing_service=None,
    input_type=_ADDTRANSACTIONWITHVALIDATIONREQUEST,
    output_type=_ADDTRANSACTIONWITHVALIDATIONRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetBlock',
    full_name='mempool.Mempool.GetBlock',
    index=1,
    containing_service=None,
    input_type=_GETBLOCKREQUEST,
    output_type=_GETBLOCKRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='CommitTransactions',
    full_name='mempool.Mempool.CommitTransactions',
    index=2,
    containing_service=None,
    input_type=_COMMITTRANSACTIONSREQUEST,
    output_type=_COMMITTRANSACTIONSRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='HealthCheck',
    full_name='mempool.Mempool.HealthCheck',
    index=3,
    containing_service=None,
    input_type=_HEALTHCHECKREQUEST,
    output_type=_HEALTHCHECKRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_MEMPOOL)

DESCRIPTOR.services_by_name['Mempool'] = _MEMPOOL

# @@protoc_insertion_point(module_scope)
