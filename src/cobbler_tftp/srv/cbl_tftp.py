#!/usr/bin/env python3
# This source code is licensed under the MIT license

"""
tftp server with static file handling
"""

import os

import yaml
from fbtftp.base_handler import BaseHandler
from fbtftp.base_server import BaseServer
from jinja2 import Environment, FileSystemLoader, StrictUndefined

# TODO: settings file path read from arguments upon execution. If none: default.
with open("src/cobbler_tftp/config/settings.yml", "r", encoding="utf-8") as stream:
    try:
        SETTINGS = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


LISTEN_ON = SETTINGS["serverConfig"]["LISTEN_ON"]
TFTP_ROOT = SETTINGS["serverConfig"]["TFTP_ROOT"]
PORT = SETTINGS["serverConfig"]["SERVER_PORT"]
TEMPLATES_PATH = SETTINGS["serverConfig"]["TEMPLATES_PATH"]
RETRIES = SETTINGS["serverConfig"]["RETRIES"]
TIMEOUT = SETTINGS["serverConfig"]["TIMEOUT"]


class Settings:
    def __init__(self) -> None:
        self.cobbler_connection = CobblerConnection()
        self.retries = 5

    def load(self, settings: Dict[str, Any]):
        retries_env = os.environ["TFTP_SERVER_CONFIG_RETRIES"]
        if retries_env:
            self.retries = retries_env
        self.retries = settings.get("serverConfig", {}).get("retries", 5)


class CobblerConnection:
    def __init__(self) -> None:
        self.hostname = ""
        self.user = ""
        self.password = ""
        self.password_file = ""


# ResponseData
class TftpData:
    def __init__(self, filename):
        path = os.path.join(TFTP_ROOT, filename)
        self._size = os.stat(path).st_size
        self._reader = open(path, "rb")

    def read(self, data):
        return self._reader.read(data)

    def size(self):
        return self._size

    def close(self):
        self._reader.close()


class StaticHandler(BaseHandler):
    def get_response_data(self):
        return TftpData(self._path)


class TftpServer(BaseServer):
    def get_handler(self, server_addr, peer, path, options):
        return StaticHandler(server_addr, peer, path, options, session_stats)


TftpServer


# render config template
def render_template(template, **kwargs):
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_PATH),
        undefined=StrictUndefined,
        trim_blocks=True,
    )

    template = env.get_template(template)
    return template.render(**kwargs)


def session_stats(stats):
    print("")
    print("#" * 60)
    print("Peer: {} UDP/{}".format(stats.peer[0], stats.peer[1]))
    print("File: {}".format(stats.file_path))
    print("Sent Packets: {}".format(stats.packets_sent))
    print("#" * 60)
