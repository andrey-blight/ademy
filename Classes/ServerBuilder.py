from Data.Functions import load_environment_variable
from os import environ

"""
Class for create the server URI
"""


class ServerBuilder:
    COLON: str = ':'
    SLASH: str = '/'

    def __init__(self):
        load_environment_variable()
        self._string: str = ''
        self.host: str = environ.get("SERVER_HOST")
        self.port: str = str(environ.get("SERVER_PORT"))
        self.protocol: str = environ.get("SERVER_PROTOCOL")

    def _add_protocol(self):
        self._string += self.protocol
        return self

    def _add_colon(self):
        self._string += self.COLON
        return self

    def _add_slashes(self):
        self._string += self.SLASH + self.SLASH
        return self

    def _add_host(self):
        self._string += self.host
        return self

    def _add_port(self):
        self._string += self.port
        return self

    def get_server(self):
        self._add_protocol()._add_colon()._add_slashes()._add_host()._add_colon()._add_port()
        return self._string
