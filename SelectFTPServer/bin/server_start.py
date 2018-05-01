#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from src.main import func
from src.common import server_show

if __name__ == "__main__":
    server_show("|----- Start Select FTP Server -----","info")
    func()