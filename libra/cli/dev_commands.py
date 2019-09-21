from command import *

class DevCommand(Command):
    def get_aliases(self):
        return ["dev"]

    def get_description(self):
        return "Local move development"

    def execute(self, client, params):
        pass