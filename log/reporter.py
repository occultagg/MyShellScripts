#!/usr/bin/env Python
# -*- coding=utf-8 -*-

import datetime
import smtplib
import subprocess
# 改变编码支持中文
from email.header import Header
from email.mime.application import MIMEApplication
# 附件支持
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# 格式化发件人、收件人
from email.utils import parseaddr, formataddr


def getYesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return str(yesterday)


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def sent_mail(yesterday):
    from_addr = 'panweijian@e-car.cn'
    password = '7705My00'
    to_addr = ['panweijian@e-car.cn', 'yuguoxing@e-car.cn', 'zenglingfeng@e-car.cn', 'xuwenju@e-car.cn',
               'houmingbo@e-car.cn', 'chenjinqiu@e-car.cn', 'zhongying@e-car.cn']
    # to_addr = ['panweijian@e-car.cn', '419397705@qq.com', '1540060183@qq.com']
    smtp_server = 'smtp.exmail.qq.com'
    # 建立MIMEmultipart对象
    msg = MIMEMultipart()
    msg['From'] = _format_addr(from_addr)
    msg['To'] = _format_addr(to_addr)
    msg['Subject'] = Header(yesterday + 'nginx接口分析统计', 'utf-8').encode()
    text = MIMEText('你们好，附件为昨天的nginx接口分析统计。', 'plain', 'utf-8')
    msg.attach(text)
    filename = '/root/log-report/' + yesterday + '.zip'
    atta = MIMEApplication(open(filename, 'rb').read())
    atta.add_header('Content-Disposition', 'attachment', filename=yesterday + '.zip')
    msg.attach(atta)

    server = smtplib.SMTP(smtp_server, 25)
    # 打印出和smtp交互的信息
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()


def main():
    yesterday = getYesterday()
    sh_path = '/root/log-report/report.sh'
    p = subprocess.Popen(sh_path, shell=True)
    ret = p.wait()
    if ret != 0:
        print('脚本执行错误')
    else:
        sent_mail(yesterday)


if __name__ == '__main__':
    main()
