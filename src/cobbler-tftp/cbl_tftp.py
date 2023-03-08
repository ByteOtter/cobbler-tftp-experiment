#!/usr/bin/env python3
# This source code is licensed under the MIT license

"""
tftp server with static file handling
"""

import os
import yaml

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from fbtftp.base_handler import BaseHandler
from fbtftp.base_server import BaseServer

# read settings file
with open("src/settings.yml", "r") as stream:
    try:
        settings = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

listen_on = settings["serverConfig"]["LISTEN_ON"]
tftp_root = settings["serverConfig"]["TFTP_ROOT"]
port = settings["serverConfig"]["SERVER_PORT"]
templates_path = settings["serverConfig"]["TEMPLATES_PATH"]
retries = settings["serverConfig"]["RETRIES"]
timeout = settings["serverConfig"]["TIMEOUT"]


# ResponseData
class TftpData:
    def __init__(self, filename):
        path = os.path.join(tftp_root, filename)
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


# render config template
def render_template(template, **kwargs):
    env = Environment(
        loader=FileSystemLoader(templates_path),
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


def main():
    server = TftpServer(listen_on, port, retries, timeout)
    try:
        server.run()
    except KeyboardInterrupt:
        server.close()


if __name__ == "__main__":
    main()
