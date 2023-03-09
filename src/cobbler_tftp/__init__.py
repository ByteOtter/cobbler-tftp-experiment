#!/usr/bin/env python3
# This source code is licensed under the MIT license

from cobbler_tftp.srv.cbl_tftp import TftpServer, LISTEN_ON, PORT, RETRIES, TIMEOUT


def create_server():
    server = TftpServer(LISTEN_ON, PORT, RETRIES, TIMEOUT)
    return server
