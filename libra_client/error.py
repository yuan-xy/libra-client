
class LibraError(Exception):
    pass


class AccountError(LibraError):
    pass


class TransactionError(LibraError):
    @property
    def error_code(self):
        code, _ = self.args
        return code

    @property
    def error_msg(self):
        _, msg = self.args
        return msg


class AdmissionControlError(TransactionError):
    pass


class VMError(TransactionError):
    pass


class MempoolError(TransactionError):
    pass


class TransactionTimeoutError(LibraError):
    pass


class LibraNetError(LibraError):
    pass
