#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basedir)

user_home = "%s/home"%basedir
user_info = "%s/db"%basedir
log_dir = os.path.join(basedir,"logs")
 
HOST = "localhost"
PORT = 9999