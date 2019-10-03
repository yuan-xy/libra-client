from canoser import DelegateT, Uint8

ADDRESS_LENGTH = 32

class Address(DelegateT):
    delegate_type = [Uint8, ADDRESS_LENGTH]