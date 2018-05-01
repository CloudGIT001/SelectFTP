#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import socket
import selectors

Base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(Base_dir)

from conf import settings
from src.common import server_show
from src.user import User

sel = selectors.DefaultSelector()


def server_method(con,mask):
    cmd = con.recv(1024)
    if not cmd:
        sel.unregister(con)
        con.close()
    else:
        data = cmd.decode()
        res = data.split("+")
        name = res[1]
        pswd = res[2]
        if res[0] == "login":
            server_show("The request to receive the client landing is landing....", "msg")
            user = User(name, pswd)
            sign = user.login()
            if sign:
                con.sendall(bytes("Success", encoding="utf-8"))
            else:
                con.sendall(bytes("Failure", encoding="utf-8"))
        if res[0] == "register":
            server_show("The request to receive the client register is register....", "msg")
            user = User(name, pswd)
            if user.register():
                con.sendall(bytes("Success", encoding="utf-8"))
            else:
                con.sendall(bytes("Failure", encoding="utf-8"))
        if res[0] == "view":
            server_show("Request to view the list of files under the directory....", "msg")
            user = User(name, pswd)
            if user.view_file():
                con.sendall(bytes("Success", encoding="utf-8"))
            else:
                con.sendall(bytes("Failure", encoding="utf-8"))
        if res[0] == "upload":
            server_show("receiving a request from a client to upload a file....","msg")
            con.send(bytes("True", encoding="utf-8"))
        if res[0] == "uploadfile":
            res_length = res[3]
            filename = res[4]
            User.receive(filename, name, res_length, con)
        if res[0] == "download":
            server_show("receiving a request from a client to download a file....","msg")
            user = User(name, pswd)
            res = str(user.view_file())
            con.sendall(bytes(res, encoding="utf-8"))
        if res[0] == "downloadfile":
            filename = res[3]
            User.download_file(filename, name, con)
            server_show("file download success....", "info")


def accept(server,mask):
    server_show("listen in[%s]address[%s]port，waitting connect...." % (settings.HOST, settings.PORT), "info")
    con, addr = server.accept()
    server_show("receive the connection request of the {0}，now communication....".format(addr), "info")
    con.setblocking(False)
    sel.register(con, selectors.EVENT_READ, server_method)


def func():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((settings.HOST,settings.PORT))
    server.listen(100)
    server.setblocking(False)
    sel.register(server, selectors.EVENT_READ, accept)
    while True:
        events = sel.select()
        for key,mask in events:
            callback = key.data
            callback(key.fileobj,mask)