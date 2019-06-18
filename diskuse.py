#!/usr/local/bin/python3

import os,psutil,smtplib,socket
from email.mime.text import MIMEText
from subprocess import Popen, PIPE

THRESHOLD = 95
partitions = psutil.disk_partitions(all=False)
message = 'WARNING: DISK(S) OVER ' + str(THRESHOLD) + '% FULL'
diskname = []
diskpercent = []
email_receiver = ""

#for loop to iterate through disks and monitor usage
for p in partitions:
        diskuse = (psutil.disk_usage(p.mountpoint).percent)
        if diskuse >= THRESHOLD:
                diskname.append(p.mountpoint)
                diskpercent.append(psutil.disk_usage(p.mountpoint).percent)

#if statement to email the disk name and percentage used
if diskuse >= THRESHOLD:
        msg = MIMEText(message + ' ' + (str(dict(zip(diskname,diskpercent)))))
        msg["To"] = email_receiver
        msg["Subject"] = '[' + (socket.gethostname()) + '] ' +  "DISK OVER THRESHOLD"
        P = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE, universal_newlines=True)
        P.communicate(msg.as_string())
