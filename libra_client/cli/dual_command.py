from libra_client.cli.command import Command


class DualCommand(Command):
    """
    All commands that can run both in libra_shell and linux shell should inherit this DualCommand
    """

    def get_real_client(self, client, **kwargs):
        if kwargs is not None and 'proxy' in kwargs:
            if kwargs['proxy']:
                return client.grpc_client
        return client
