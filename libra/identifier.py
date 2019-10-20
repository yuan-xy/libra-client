from canoser import DelegateT

#! An identifier is the name of an entity (module, resource, function, etc) in Move.
#!
#! Among other things, identifiers are used to:
#! * specify keys for lookups in storage
#! * do cross-module lookups while executing transactions

class Identifier(DelegateT):
    delegate_type = str


class IdentStr(DelegateT):
    delegate_type = str