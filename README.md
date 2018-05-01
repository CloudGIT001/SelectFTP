##### 作业要求

```
使用SELECT或SELECTORS模块实现并发简单版FTP
允许多用户并发上传下载文件
```

##### 程序的功能实现

```
1、用户登录注册（测试用户：xiaoyu；密码123456）
2、上传/下载文件
3、查看不同用户自己家得目录下文件
4、使用了selector模块，实现单线程下并发效果
```

##### 脚本文件介绍

```
D:.
├─SelectFTPClient       # FTP客户端文件夹
│  │  client_start.py   # ftp客户端启动文件
│  │  __init__.py
│  │
│  └─SampleFolder       # FTP客户端文件存放目录
│          Cloud_VNC.exe
│          empty
│          ip.txt
│
└─SelectFTPServer       # FTP服务端文件夹
    │  __init__.py
    │
    ├─bin
    │      server_start.py   # FTP服务端启动文件
    │      __init__.py
    │
    ├─conf
    │  │  settings.py        # 目录配置文件脚本
    │  │  __init__.py
    │  │
    │  └─__pycache__
    │          settings.cpython-36.pyc
    │          __init__.cpython-36.pyc
    │
    ├─db                    # 用户登记文件目录
    │      xiaoyu
    │
    ├─home                  # 用户文件存放目录
    │  └─xiaoyu
    │      │  empty_file
    │      │  ip.txt
    │      │
    │      └─others
    ├─logs              
    │      client_sys.log   # 客户端操作日志
    │      server_sys.log   # 服务端操作日志
    │
    └─src
        │  common.py        # 日志生成脚本
        │  main.py          # 程序主函数脚本
        │  user.py          # 用户类及方法
        │  __init__.py
        │
        └─__pycache__
                common.cpython-36.pyc
                main.cpython-36.pyc
                user.cpython-36.pyc
                __init__.cpython-36.pyc
```


##### 程序使用示例

一、FTP用户注册

```
------- SelectFTP User login Interface -------
    1: user landing
    2: user registration
    3: user exit
    
Input user choice>>>:2
Input Your register username>>>:xiess
Input Your register password>>>:123456
User[xiess] Register Success....
```

二、用户登陆上传文件

```
------- SelectFTP User login Interface -------
    1: user landing
    2: user registration
    3: user exit
    
Input user choice>>>:1
Input Your Login username>>>:xiaoyu
Input Your Login password>>>:123456
User[xiaoyu] login success....
------[xiaoyu]operation command ------
    1: uploading file
    2: download file
    3: exit operation
     
Input Your operation>>>:1
---- uploading file ----
1: Cloud_VNC.exe
2: empty
3: ip.txt
Input uploading file number>>>:2
file upload success....
```

三、用户登陆下载文件

```
 ------- SelectFTP User login Interface -------
    1: user landing
    2: user registration
    3: user exit
    
Input user choice>>>:1
Input Your Login username>>>:xiaoyu
Input Your Login password>>>:123456
User[xiaoyu] login success....
------[xiaoyu]operation command ------
    1: uploading file
    2: download file
    3: exit operation
     
Input Your operation>>>:2
---- downloading file ----
1：empty 
2：empty_file 
3：ip 
Input downloading file number>>>:3
ready to start downloading files....
file downloading success....
```

四、退出程序

```
 ------- SelectFTP User login Interface -------
    1: user landing
    2: user registration
    3: user exit
    
Input user choice>>>:3
Exit SelectFTP Success....
```
