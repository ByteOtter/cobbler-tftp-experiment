#!/usr/bin/env python3
# This source code is licensed under the MIT license

"""
Initializing the TFTP server
"""

from cobbler_tftp.srv.cbl_tftp import LISTEN_ON, PORT, RETRIES, TIMEOUT, TftpServer


def create_server():
    server = TftpServer(LISTEN_ON, PORT, RETRIES, TIMEOUT)
    return server
