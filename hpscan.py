# /usr/bin/env python
# _*_ coding:utf-8 _*_
# author: smelond
# blog: https://smelond.com


import socket, socks
import requests
from ftplib import FTP
import re
from IPy import IP
import threading
import time, datetime
import argparse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # 解决requests发送HTTPS请求时出现的报错信息


class server_banner:
    def __init__(self, args):
        self.ports = list(map(int, str(args.PORT).split(",")))
        self.ports.append(80)
        self.ports = list(set(self.ports))
        self.overtime = args.OVERTIME
        self.min_time = args.FILE
        self.proxy = args.PROXY
        self.ftp = FTP()
        self.proxy = {
            'http': self.proxy,
            'https': self.proxy
        }

    def issocks(self, socks5):
        if socks5:
            return socks5
        return None

    def html_template(self):
        html = """
        <a href="%s">%s\t%s\t%s</a>
        """

    def banner_info(self, ip):
        ftp_port = [2121, 21]  # 这里可以添加你认为目标服务器会开启的FTP端口
        http = ['http://', 'https://']
        for h in http:
            for port in self.ports:
                if port in ftp_port:
                    if args.PROXY:
                        s, p = str(args.PROXY).split("//")[-1].split(":")
                        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, s, p)
                    socket.socket = socks.socksocket
                    socket.setdefaulttimeout(int(self.overtime))  # 超时时间
                    try:
                        banner = self.ftp.connect(str(ip), int(port))
                    except:
                        continue
                    banner = str(banner).split("\n")[0]  # 获取ftp信息
                    banner_port = port
                    self.ftp.quit()
                    print(ip, banner_port, banner)
                    with open(self.min_time, "a") as file:
                        file.write(
                            """<a href="ftp://%s"  target="_blank">ftp://%s</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%s:%s<br />""" % (
                                ip, ip, banner_port, banner) + "\n")
                try:
                    url = "%s%s:%s" % (h, ip, str(port))
                    #print(url)
                    try:
                        # r = requests.get(url, timeout=int(self.overtime))  # 超时时间
                        s = requests.Session()
                        r = s.get(url, proxies=self.issocks(self.proxy), timeout=int(self.overtime),
                                  verify=False, allow_redirects=True)  # 超时时间
                    except:
                        continue
                    r.encoding = 'utf-8'
                    content = r.text
                    status = r.status_code
                    content = str(content).replace("\r", "").replace("\n", "")  # \r\n 替换为空
                    title = re.search(r'<title>(.*)</title>', content)
                    if title:
                        title = title.group(1).strip("\t").strip("\r").strip("\n")
                        # title = title.group(1).strip().strip("\r").strip("\n")[:30]
                    else:
                        title = title
                    banner = r.headers['Server'][:20]
                    print("%s %s %s %s" % (url, status, title, banner))
                    with open(self.min_time, "a") as file:
                        file.write(
                            """<a href="%s"  target="_blank">%s</a>&nbsp;&nbsp;&nbsp;&nbsp;%s&nbsp;&nbsp;&nbsp;%s:%s<br />""" % (
                                url, url, status, title, banner) + "\n")
                except:
                    continue

    def other_banner_info(self):
        pass


def call_c(numbers, ip):
    with SEM:
        try:
            print('当前进度 : %s ' % ip, end='\r')
            # lock.acquire()  # 上锁
            # print("%s -> %s" % (ip, str(numbers)))
            Ser_Ban = server_banner(args)
            Ser_Ban.banner_info(ip)
            # lock.release()  # 释放锁
        except:
            pass


def ip_handle(all_ip):
    try:
        all_ip = IP(all_ip)
        ip_len = all_ip.len()
        ip_list = []
        for line in all_ip:
            ip_list.append(line)
        return ip_list, ip_len
    except Exception as e:
        print(e)


def main(args):
    ip_list, ip_len = ip_handle(args.IP)
    start_time = time.ctime()
    print("starting at: %s" % start_time)
    threads = []
    for i in range(ip_len):
        t = threading.Thread(target=call_c, args=(i, ip_list[i]))
        t.start()
        threads.append(t)  # 将每次循环的对象加入到列表
    for t in threads:  # 等待
        t.join()  # 线程完成
    print("all Done at: %s" % time.ctime())


if __name__ == '__main__':
    min_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # 当前天，时，分，秒
    __version__ = "v.1.0 --- author: smelond"
    parser = argparse.ArgumentParser(description='服务探测，端口扫描')
    parser.add_argument('-V', '--version', help="version", action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-i', dest="IP", type=str,
                        help="IP地址: 172.16.0.0/16 || 192.168.1.0/24 || 172.16.16.0/20 ||172.16.16.0-172.16.31.255==172.16.16.0/20",
                        required=True)
    parser.add_argument('-p', dest="PORT", type=str, help="端口: 默认21,8000,8080,8081,8088,9000,10000",
                        default="21,80,88,8000,8080,8081,8088,9000,10000")
    parser.add_argument('-t', dest='THREAD', help='线程数量，默认为20', default=20)
    parser.add_argument('-o', dest='OVERTIME', help='超时时间 time out 默认为3', default=3)
    parser.add_argument('-f', dest='FILE', help='输出文件', default="result_%s.html" % min_time)
    parser.add_argument('--proxy', dest='PROXY',
                        help='proxy-server -> "socks5://127.0.0.1:1080"')
    args = parser.parse_args()
    SEM = threading.Semaphore(int(args.THREAD))  # 线程数默认为10
    lock = threading.Lock()
    main(args)
