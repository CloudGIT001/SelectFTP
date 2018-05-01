#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import time
import pickle
import socket

Base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(Base_dir)
from conf import settings
from src.common import server_show


class User(object):
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.home_path = settings.user_home + "/" +self.username

    def login(self):
        user_dic = User.info_read(self.username)
        if user_dic[self.username] == self.password:
            server_show("login success....","info")
            return True
        else:
            server_show("login error....","error")
            return False
    
    def register(self):
        dic = {}
        dic[self.username] = self.password
        if User.info_write(self.username,dic):
            server_show("register success....","info")
            os.mkdir(self.home_path)
            os.mkdir("%s/others" % self.home_path)
            with open("%s\empty_file" % self.home_path, "w") as f:
                f.write("empty_file")
            return True
        else:
            server_show("register error....","error")
            return False

    def view_file(self):
        if not os.path.exists(self.home_path):
            os.mkdir(self.home_path)
            with open("%s\one_file" % self.home_path, "w") as f:
                f.write("one_file")
        for root, dirs, files in os.walk(self.home_path):
            return files

    @staticmethod
    def download_file(filename,name,con):
        dir = os.path.join(os.path.join(os.path.join(Base_dir, "home"), name), filename)
        with open(dir,"rb") as f:
            data = f.read()
            length = str(len(data))
            con.sendall(bytes(length,encoding="utf-8"))
            time.sleep(1)
            con.sendall(data)

    @staticmethod
    def receive(filename,name,res_length,con):
        con.send("True".encode("utf-8"))
        time.sleep(0.5)
        dir = os.path.join(os.path.join(os.path.join(Base_dir,"home"),name),filename)
        length = 0
        f =  open(dir, "wb")
        while length < int(res_length):
            if int(res_length) - length > 1024:
                size = 1024
            else:
                size = int(res_length) - length
            data = con.recv(size)
            length += len(data)
            f.write(data)
        if length == int(res_length):
            time.sleep(0.5)
            server_show("file download success....","info")

    @staticmethod
    def info_read(name):
        user_dir = os.path.join(settings.user_info,name)
        if os.path.exists(user_dir):
            with open(user_dir,"rb") as f:
                dic = pickle.load(f)
                return dic
        else:
            server_show("user data is empty....","error")

    @staticmethod
    def info_write(name,dic):
        user_dir = os.path.join(settings.user_info, name)
        with open(user_dir,"wb") as f:
            pickle.dump(dic,f)
            return True