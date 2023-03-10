#!/usr/bin/env python3
# This source code is licensed under the MIT license

"""
Initialize server
"""

from cobbler_tftp import create_server

server = create_server()

if __name__ == "__main__":
    try:
        server.run()
    except KeyboardInterrupt:
        server.close()
