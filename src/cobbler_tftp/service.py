#!/usr/bin/env python3
# This source code is licensed under the MIT license

#!/usr/bin/env python3
"""
Set up file for the cbl_tftp daemon
"""

import daemon
from cbl_tftp import main

with daemon.DaemonContext():
    main()
