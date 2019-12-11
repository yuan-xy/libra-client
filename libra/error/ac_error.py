
class AdmissionControlStatusCode:

    @classmethod
    def get_name(cls, status):
        for name, code in cls.__dict__.items():
            if code == status:
                return name
        raise f"AdmissionControl error code:{status} not exsits."

    # Validator accepted the transaction.
    Accepted = 0
    # The sender is blacklisted.
    Blacklisted = 1
    # The transaction is rejected, e.g. due to incorrect signature.
    Rejected = 2

