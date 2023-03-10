#!/usr/bin/env python3
# This source code is licensed under the MIT license

"""
Set up file for the cbl_tftp daemon
"""

import daemon

from main import main

with daemon.DaemonContext():
    main()
