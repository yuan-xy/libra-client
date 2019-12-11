
class MempoolAddTransactionStatusCode:

    @classmethod
    def get_name(cls, status):
        for name, code in cls.__dict__.items():
            if code == status:
                return name
        raise f"mempool error code:{status} not exsits."

    # Transaction was sent to Mempool
    Valid = 0
    # The sender does not have enough balance for the transaction.
    InsufficientBalance = 1
    # Sequence number is old, etc.
    InvalidSeqNumber = 2
    # Mempool is full (reached max global capacity)
    MempoolIsFull = 3
    # Account reached max capacity per account
    TooManyTransactions = 4
    # Invalid update. Only gas price increase is allowed
    InvalidUpdate = 5