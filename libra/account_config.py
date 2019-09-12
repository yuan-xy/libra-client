

class AccountConfig:
    # LibraCoin
    COIN_MODULE_NAME = "LibraCoin";
    COIN_STRUCT_NAME = "T";

    # Account
    ACCOUNT_MODULE_NAME = "LibraAccount";
    ACCOUNT_STRUCT_NAME = "T";

    # Hash
    HASH_MODULE_NAME = "Hash";

    #ACCOUNT_RESOURCE_PATH = [1, 33, 125, 166, 198, 179, 225, 159, 24, 37, 207, 178, 103, 109, 174, 204, 227, 191, 61, 224, 60, 242, 102, 71, 199, 141, 240, 11, 55, 27, 37, 204, 151]

    ACCOUNT_RESOURCE_PATH = bytes.fromhex(
        "01217da6c6b3e19f1825cfb2676daecce3bf3de03cf26647c78df00b371b25cc97"
    )

    @classmethod
    def account_sent_event_path(self):
        return self.ACCOUNT_RESOURCE_PATH + b"/sent_events_count/"


    @classmethod
    def account_received_event_path(self):
        return self.ACCOUNT_RESOURCE_PATH + b"/received_events_count/"


    @classmethod
    def association_address(self):
        return "000000000000000000000000000000000000000000000000000000000a550c18"
