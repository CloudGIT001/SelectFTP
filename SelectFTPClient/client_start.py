#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import time
import socket

Basedir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"SelectFTPServer")
updir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"SampleFolder")
sys.path.append(Basedir)
print(Basedir)
print(updir)

from src.common import client_show


def upload(client,user_info,name):
    client_show("---- uploading file ----","info")
    dic = {}
    for root,dirs,files in os.walk(updir):
        for i,j in enumerate(files):
            k = i + 1
            dic[k] = j
            client_show("%s: %s"%(k,j),"info")
    choice = input("Input uploading file number>>>:").strip()
    command = "upload+" + user_info
    client.send(bytes(command,encoding="utf-8"))
    res = client.recv(1024)
    if str(res,encoding="utf-8") == "True":
        dir = os.path.join(updir,dic[int(choice)])
        f = open(dir,"rb")
        data = f.read()
        length = str(len(data))
        command2 = "uploadfile+"+user_info+"+"+length+"+"+dic[int(choice)]
        client.send(command2.encode("utf-8"))
        client.recv(1024)
        client.sendall(data)
        time.sleep(1)
        client_show("file upload success....","info")
        f.close()
    else:
        client_show("file upload error....","error")


def download(client,user_info,name):
    client_show("---- downloading file ----","info")
    dic = {}
    command = "download+" + user_info
    client.sendall(bytes(command, encoding="utf-8"))
    data = client.recv(4096)
    res = eval(str(data, encoding="utf-8"))
    if len(res) == 0:
        client_show("no file in the current directory....","info")
    else:
        for i,j in enumerate(res):
            k = i + 1
            dic[k] = j
            client_show("%s：%s " % (k, j),"info")
    choice = input("Input downloading file number>>>:").strip()
    command2 = "downloadfile+" + user_info + "+" + dic[int(choice)]
    client.send(bytes(command2 , encoding="utf-8"))
    client_show("ready to start downloading files....","info")
    dir = os.path.join(updir, dic[int(choice)])
    res_length = str(client.recv(1024).decode())
    length = 0
    f = open(dir, "wb")
    while length < int(res_length):
        if int(res_length) - length > 1024:
            size = 1024
        else:
            size = int(res_length) - length
        data = client.recv(size)
        length += len(data)
        f.write(data)
    if length == int(res_length):
        time.sleep(1)
        client_show("file downloading success....","info")
        f.close()
    else:
        client_show("file downloading error....","error")


def view_file(client,user_info,name):
    command = "view+" + user_info
    client.sendall(bytes(command, encoding="utf-8"))
    data = client.recv(1024)
    res = eval(str(data, encoding="utf-8"))
    if len(res) == 0:
        client_show("no file in the current directory....", "info")
    else:
        for i in res:
            client_show("%s "%i, "info")


def operate(client, user_info, name):
    info = """------[%s]operation command ------
    1: uploading file
    2: download file
    3: exit operation
    """%name
    while True:
        client_show("%s "%info,"info")
        choice = input("Input Your operation>>>:").strip()
        if choice == "0":
            break
        if choice == "1":
            upload(client,user_info,name)
            continue
        if choice == "2":
            download(client,user_info,name)
            continue
        if choice == "3":
            break
        else:
            client_show("Input error....","error")


def com_parse(client,com):
    client.sendall(com.encode("utf-8"))
    re = client.recv(4096)
    if str(re,encoding="utf-8") == "Success":
        return True
    else:
        return False


def login(client,data):
    name = input("Input Your Login username>>>:").strip()
    pawd = input("Input Your Login password>>>:").strip()
    user_info = name + "+" + pawd
    com = "login+" + name + "+" +pawd
    if com_parse(client,com):
        client_show("User[%s] login success...."%name,"info")
        operate(client,user_info,name)
    else:
        client_show("User[%s] login error...."%name,"error")


def register(client,data):
    name = input("Input Your register username>>>:").strip()
    pawd = input("Input Your register password>>>:").strip()
    com = "register+" + name + "+" + pawd
    if com_parse(client,com):
        user_info = name + "+" + pawd
        client_show("User[%s] Register Success...."%name,"info")
        operate(client,user_info,name)
    else:
        client_show("User[%s] Register Error...."%name,"error")


def quit():
    client_show("Exit SelectFTP Success....","info")
    exit()


def main_func(client):
    data = "FTP connect success......"
    info = """ ------- SelectFTP User login Interface -------
    1: user landing
    2: user registration
    3: user exit
    """
    while True:
        client_show("%s"%info,"info")
        choice = input("Input user choice>>>:").strip()
        if choice == "1":
            login(client,data)
            continue
        if choice == "2":
            register(client,data)
            continue
        if choice == "3":
            quit()
        else:
            client_show("Input error,plaese again....","error")


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 9999
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((HOST,PORT))
    main_func(client)
    client.close()


