# hpscan.py
一款简单的python版web服务探测脚本,可以快速探测web端口是否开放,获取对应的title,服务信息

注意这是python3写的,请使用python3运行

### 安装模块
``` bash
pip3 install PySocks
pip3 install requests
pip3 install IPy
```

### 使用:
``` bash
python hpscan.py -i 192.168.3.0/24
python hpscan.py -i 192.168.3.0/25
python hpscan.py -i 192.168.3.128/25
```

