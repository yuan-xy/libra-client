from canoser import Struct, RustEnum, Uint64, RustOptional
# The minimum status code for validation statuses
VALIDATION_STATUS_MIN_CODE = 0

# The maximum status code for validation statuses
VALIDATION_STATUS_MAX_CODE = 999

# The minimum status code for verification statuses
VERIFICATION_STATUS_MIN_CODE = 1000

# The maximum status code for verification statuses
VERIFICATION_STATUS_MAX_CODE = 1999

# The minimum status code for invariant violation statuses
INVARIANT_VIOLATION_STATUS_MIN_CODE = 2000

# The maximum status code for invariant violation statuses
INVARIANT_VIOLATION_STATUS_MAX_CODE = 2999

# The minimum status code for deserialization statuses
DESERIALIZATION_STATUS_MIN_CODE = 3000

# The maximum status code for deserialization statuses
DESERIALIZATION_STATUS_MAX_CODE = 3999

# The minimum status code for runtime statuses
EXECUTION_STATUS_MIN_CODE = 4000

# The maximum status code for runtim statuses
EXECUTION_STATUS_MAX_CODE = 4999

class OptionUInt64(RustOptional):
    _type = Uint64


class OptionStr(RustOptional):
    _type = str


class VMStatus(Struct):
    """
    A `VMStatus` is represented as a required major status that is semantic coupled with with
    an optional sub status and message.
    """
    _fields = [
        ('major_status', Uint64),
        ('sub_status', OptionUInt64),
        ('message', OptionStr)
    ]

    def err_msg(self):
        if self.message.value is not None:
            return self.message.value
        else:
            return StatusCode.get_name(self.major_status)

    @classmethod
    def from_proto(cls, proto):
        ret = cls()
        ret.major_status = proto.major_status
        if proto.has_sub_status:
            ret.sub_status = OptionUInt64(proto.sub_status)
        else:
            ret.sub_status = OptionUInt64(None)
        if proto.has_message:
            ret.message = OptionStr(proto.message)
        else:
            ret.message = OptionStr(None)
        return ret




class StatusType(RustEnum):
    """
    A status type is one of 5 different variants along with a fallback variant in the case that we
    don't recognize the status code.
    """
    _enums = [
        ('Validation', None),
        ('Verification', None),
        ('InvariantViolation', None),
        ('Deserialization', None),
        ('Execution', None),
        ('Unknown', None)
    ]





class StatusCode:

    @classmethod
    def get_name(cls, status):
        for name, code in cls.__dict__.items():
            if code == status:
                return name
        raise f"vm error code:{status} not exsits."

    # The status of a transaction as determined by the prologue.
    # Validation Errors: 0-999
    # We don't want the default value to be valid
    UNKNOWN_VALIDATION_STATUS = 0
    # The transaction has a bad signature
    INVALID_SIGNATURE = 1
    # Bad account authentication key
    INVALID_AUTH_KEY = 2
    # Sequence number is too old
    SEQUENCE_NUMBER_TOO_OLD = 3
    # Sequence number is too new
    SEQUENCE_NUMBER_TOO_NEW = 4
    # Insufficient balance to pay minimum transaction fee
    INSUFFICIENT_BALANCE_FOR_TRANSACTION_FEE = 5
    # The transaction has expired
    TRANSACTION_EXPIRED = 6
    # The sending account does not exist
    SENDING_ACCOUNT_DOES_NOT_EXIST = 7
    # This write set transaction was rejected because it did not meet the
    # requirements for one.
    REJECTED_WRITE_SET = 8
    # This write set transaction cannot be applied to the current state.
    INVALID_WRITE_SET = 9
    # Length of program field in raw transaction exceeded max length
    EXCEEDED_MAX_TRANSACTION_SIZE = 10
    # This script is not on our whitelist of script.
    UNKNOWN_SCRIPT = 11
    # Transaction is trying to publish a new module.
    UNKNOWN_MODULE = 12
    # Max gas units submitted with transaction exceeds max gas units bound
    # in VM
    MAX_GAS_UNITS_EXCEEDS_MAX_GAS_UNITS_BOUND = 13
    # Max gas units submitted with transaction not enough to cover the
    # intrinsic cost of the transaction.
    MAX_GAS_UNITS_BELOW_MIN_TRANSACTION_GAS_UNITS = 14
    # Gas unit price submitted with transaction is below minimum gas price
    # set in the VM.
    GAS_UNIT_PRICE_BELOW_MIN_BOUND = 15
    # Gas unit price submitted with the transaction is above the maximum
    # gas price set in the VM.
    GAS_UNIT_PRICE_ABOVE_MAX_BOUND = 16

    # When a code module/script is published it is verified. These are the
    # possible errors that can arise from the verification process.
    # Verification Errors: 1000-1999
    UNKNOWN_VERIFICATION_ERROR = 1000
    INDEX_OUT_OF_BOUNDS = 1001
    RANGE_OUT_OF_BOUNDS = 1002
    INVALID_SIGNATURE_TOKEN = 1003
    INVALID_FIELD_DEF = 1004
    RECURSIVE_STRUCT_DEFINITION = 1005
    INVALID_RESOURCE_FIELD = 1006
    INVALID_FALL_THROUGH = 1007
    JOIN_FAILURE = 1008
    NEGATIVE_STACK_SIZE_WITHIN_BLOCK = 1009
    UNBALANCED_STACK = 1010
    INVALID_MAIN_FUNCTION_SIGNATURE = 1011
    DUPLICATE_ELEMENT = 1012
    INVALID_MODULE_HANDLE = 1013
    UNIMPLEMENTED_HANDLE = 1014
    INCONSISTENT_FIELDS = 1015
    UNUSED_FIELD = 1016
    LOOKUP_FAILED = 1017
    VISIBILITY_MISMATCH = 1018
    TYPE_RESOLUTION_FAILURE = 1019
    TYPE_MISMATCH = 1020
    MISSING_DEPENDENCY = 1021
    POP_REFERENCE_ERROR = 1022
    POP_RESOURCE_ERROR = 1023
    RELEASEREF_TYPE_MISMATCH_ERROR = 1024
    BR_TYPE_MISMATCH_ERROR = 1025
    ABORT_TYPE_MISMATCH_ERROR = 1026
    STLOC_TYPE_MISMATCH_ERROR = 1027
    STLOC_UNSAFE_TO_DESTROY_ERROR = 1028
    RET_UNSAFE_TO_DESTROY_ERROR = 1029
    RET_TYPE_MISMATCH_ERROR = 1030
    RET_BORROWED_MUTABLE_REFERENCE_ERROR = 1031
    FREEZEREF_TYPE_MISMATCH_ERROR = 1032
    FREEZEREF_EXISTS_MUTABLE_BORROW_ERROR = 1033
    BORROWFIELD_TYPE_MISMATCH_ERROR = 1034
    BORROWFIELD_BAD_FIELD_ERROR = 1035
    BORROWFIELD_EXISTS_MUTABLE_BORROW_ERROR = 1036
    COPYLOC_UNAVAILABLE_ERROR = 1037
    COPYLOC_RESOURCE_ERROR = 1038
    COPYLOC_EXISTS_BORROW_ERROR = 1039
    MOVELOC_UNAVAILABLE_ERROR = 1040
    MOVELOC_EXISTS_BORROW_ERROR = 1041
    BORROWLOC_REFERENCE_ERROR = 1042
    BORROWLOC_UNAVAILABLE_ERROR = 1043
    BORROWLOC_EXISTS_BORROW_ERROR = 1044
    CALL_TYPE_MISMATCH_ERROR = 1045
    CALL_BORROWED_MUTABLE_REFERENCE_ERROR = 1046
    PACK_TYPE_MISMATCH_ERROR = 1047
    UNPACK_TYPE_MISMATCH_ERROR = 1048
    READREF_TYPE_MISMATCH_ERROR = 1049
    READREF_RESOURCE_ERROR = 1050
    READREF_EXISTS_MUTABLE_BORROW_ERROR = 1051
    WRITEREF_TYPE_MISMATCH_ERROR = 1052
    WRITEREF_RESOURCE_ERROR = 1053
    WRITEREF_EXISTS_BORROW_ERROR = 1054
    WRITEREF_NO_MUTABLE_REFERENCE_ERROR = 1055
    INTEGER_OP_TYPE_MISMATCH_ERROR = 1056
    BOOLEAN_OP_TYPE_MISMATCH_ERROR = 1057
    EQUALITY_OP_TYPE_MISMATCH_ERROR = 1058
    EXISTS_RESOURCE_TYPE_MISMATCH_ERROR = 1059
    BORROWGLOBAL_TYPE_MISMATCH_ERROR = 1060
    BORROWGLOBAL_NO_RESOURCE_ERROR = 1061
    MOVEFROM_TYPE_MISMATCH_ERROR = 1062
    MOVEFROM_NO_RESOURCE_ERROR = 1063
    MOVETOSENDER_TYPE_MISMATCH_ERROR = 1064
    MOVETOSENDER_NO_RESOURCE_ERROR = 1065
    CREATEACCOUNT_TYPE_MISMATCH_ERROR = 1066
    # The self address of a module the transaction is publishing is not the sender address
    MODULE_ADDRESS_DOES_NOT_MATCH_SENDER = 1067
    # The module does not have any module handles. Each module or script must have at least one
    # module handle.
    NO_MODULE_HANDLES = 1068
    POSITIVE_STACK_SIZE_AT_BLOCK_END = 1069
    MISSING_ACQUIRES_RESOURCE_ANNOTATION_ERROR = 1070
    EXTRANEOUS_ACQUIRES_RESOURCE_ANNOTATION_ERROR = 1071
    DUPLICATE_ACQUIRES_RESOURCE_ANNOTATION_ERROR = 1072
    INVALID_ACQUIRES_RESOURCE_ANNOTATION_ERROR = 1073
    GLOBAL_REFERENCE_ERROR = 1074
    CONTRAINT_KIND_MISMATCH = 1075
    NUMBER_OF_TYPE_ACTUALS_MISMATCH = 1076
    LOOP_IN_INSTANTIATION_GRAPH = 1077
    UNUSED_LOCALS_SIGNATURE = 1078
    UNUSED_TYPE_SIGNATURE = 1079
    ZERO_SIZED_STRUCT = 1080

    # These are errors that the VM might raise if a violation of internal
    # invariants takes place.
    # Invariant Violation Errors: 2000-2999
    UNKNOWN_INVARIANT_VIOLATION_ERROR = 2000
    OUT_OF_BOUNDS_INDEX = 2001
    OUT_OF_BOUNDS_RANGE = 2002
    EMPTY_VALUE_STACK = 2003
    EMPTY_CALL_STACK = 2004
    PC_OVERFLOW = 2005
    LINKER_ERROR = 2006
    LOCAL_REFERENCE_ERROR = 2007
    STORAGE_ERROR = 2008
    INTERNAL_TYPE_ERROR = 2009
    EVENT_KEY_MISMATCH = 2010
    UNREACHABLE = 2011
    VM_STARTUP_FAILURE = 2012

    # Errors that can arise from binary decoding (deserialization)
    # Deserializtion Errors: 3000-3999
    UNKNOWN_BINARY_ERROR = 3000
    MALFORMED = 3001
    BAD_MAGIC = 3002
    UNKNOWN_VERSION = 3003
    UNKNOWN_TABLE_TYPE = 3004
    UNKNOWN_SIGNATURE_TYPE = 3005
    UNKNOWN_SERIALIZED_TYPE = 3006
    UNKNOWN_OPCODE = 3007
    BAD_HEADER_TABLE = 3008
    UNEXPECTED_SIGNATURE_TYPE = 3009
    DUPLICATE_TABLE = 3010
    VERIFIER_INVARIANT_VIOLATION = 3011

    # Errors that can arise at runtime
    # Runtime Errors: 4000-4999
    UNKNOWN_RUNTIME_STATUS = 4000
    EXECUTED = 4001
    OUT_OF_GAS = 4002
    # We tried to access a resource that does not exist under the account.
    RESOURCE_DOES_NOT_EXIST = 4003
    # We tried to create a resource under an account where that resource
    # already exists.
    RESOURCE_ALREADY_EXISTS = 4004
    # We accessed an account that is evicted.
    EVICTED_ACCOUNT_ACCESS = 4005
    # We tried to create an account at an address where an account already exists.
    ACCOUNT_ADDRESS_ALREADY_EXISTS = 4006
    TYPE_ERROR = 4007
    MISSING_DATA = 4008
    DATA_FORMAT_ERROR = 4009
    INVALID_DATA = 4010
    REMOTE_DATA_ERROR = 4011
    CANNOT_WRITE_EXISTING_RESOURCE = 4012
    VALUE_SERIALIZATION_ERROR = 4013
    VALUE_DESERIALIZATION_ERROR = 4014
    # The sender is trying to publish a module named `M` but the sender's account already
    # contains a module with this name.
    DUPLICATE_MODULE_NAME = 4015
    ABORTED = 4016
    ARITHMETIC_ERROR = 4017
    DYNAMIC_REFERENCE_ERROR = 4018
    CODE_DESERIALIZATION_ERROR = 4019
    EXECUTION_STACK_OVERFLOW = 4020
    CALL_STACK_OVERFLOW = 4021
    NATIVE_FUNCTION_ERROR = 4022
    GAS_SCHEDULE_ERROR = 4023

    # A reserved status to represent an unknown vm status.
    UNKNOWN_STATUS = Uint64.max_value



class SubStatus:
    # Arithmetic sub status sub-codes
    AEU_UNKNOWN_ARITHMETIC_ERROR = 0
    AEU_UNDERFLOW = 1
    AEO_OVERFLOW = 2
    AED_DIVISION_BY_ZERO = 3

    VSF_GAS_SCHEDULE_NOT_FOUND = 0

    # Dynamic Reference status sub-codes
    DRE_UNKNOWN_DYNAMIC_REFERENCE_ERROR = 0
    DRE_MOVE_OF_BORROWED_RESOURCE = 1
    DRE_GLOBAL_REF_ALREADY_RELEASED = 2
    DRE_MISSING_RELEASEREF = 3
    DRE_GLOBAL_ALREADY_BORROWED = 4

    # Native Function Error sub-codes
    NFE_VECTOR_ERROR_BASE = 0

    GSE_UNABLE_TO_LOAD_MODULE = 0
    GSE_UNABLE_TO_LOAD_RESOURCE = 1
    GSE_UNABLE_TO_DESERIALIZE = 2

