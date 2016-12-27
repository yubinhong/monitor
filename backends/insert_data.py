#!/usr/bin/env python
#-*- coding:utf-8 -*-
from web_models import models
import time
def insert_report_data(hostname,service_name,data):
    hostobj = models.Host.objects.get(name=hostname)
    if service_name=='CPU':
       cpuobj=models.CPUInfo(host=hostobj,
                             system=data['system'],
                             steal=data['steal'],
                             idle=data['idle'],
                             iowait=data['iowait'],
                             user=data['user'],
                             nice=data['nice'],
                             create_date=time.time())
       cpuobj.save()
    elif service_name=='Memory':
        memobj=models.MemoryInfo(host=hostobj,
                                 MemFree=data['MemFree'],
                                 Cached=data['Cached'],
                                 Buffers=data['Buffers'],
                                 MemUsage=data['MemUsage'],
                                 MemUsage_p=data['MemUsage_p'],
                                 MemTotal=data['MemTotal'],
                                 create_date=time.time())
        memobj.save()


def insert_alert(hostname,trigger,fail_count):
    alertobj=models.Alert(hostname=hostname,trigger=trigger,fail_count=fail_count)
    alertobj.save()