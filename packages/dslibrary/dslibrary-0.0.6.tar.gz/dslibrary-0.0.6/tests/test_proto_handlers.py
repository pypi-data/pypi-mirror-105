import os
import io
import unittest

from dslibrary import DSLibrary
from dslibrary.proto_handlers import load_protocol_handler, ProtocolHandler


class TestProtoHandlers(unittest.TestCase):

    def test_load_protocol_handler(self):
        """
        The basic idea: set an environment variable telling us how to handle a given protocol.
        """
        os.environ["DSLIBRARY_PROTO_ZZZ"] = "tests.test_proto_handlers.MyProtoZZZ:v=hello"
        handler = load_protocol_handler("zzz://host/etc")
        assert handler
        assert handler.open_resource("x", "rb").read() == b'hello'

    def test_through_open_resource(self):
        os.environ["DSLIBRARY_PROTO_ZZZ"] = "tests.test_proto_handlers.MyProtoZZZ:v=hello2"
        handler = load_protocol_handler("zzz://host/etc")
        with DSLibrary().open_resource("x", "rb", uri="zzz://x") as f:
            assert f.read() == b'hello2'

    def test_through_get_filesystem(self):
        # TODO access a filesystem over the 'zzz' protocol
        pass


class MyProtoZZZ(ProtocolHandler):
    def __init__(self, v="zzz"):
        self.v = v

    def open_resource(self, url: str, mode: str, **kwargs):
        return io.BytesIO(self.v.encode("utf-8"))
