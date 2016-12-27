#!/usr/bin/env python
#-*- coding:utf-8 -*-
from web_models import models
from backends.insert_data import insert_alert
import time
def select_config_data(hostname):
    #hostobj = models.Host.objects.get(name=hostname)
    #monitorgroup = hostobj.monitor_groups
    #template = monitorgroup.templates
    #services_list = template.services.select_related()
    services_list=models.Host.objects.get(name=hostname).monitor_groups.templates.services.select_related()
    data = {}
    for service in services_list:
        data[service.service_type.name] = [service.service_type.plugin, service.interval]
    return data


def select_email(hostname):
    email=models.Host.objects.get(name=hostname).monitor_groups.user.email
    return email

def select_failcount(hostname,triggerobj):
    try:
        alertobj=models.Alert.objects.get(hostname=hostname,trigger=triggerobj)
        fail_count=int(alertobj.fail_count)
    except Exception as e:
        fail_count=0
        insert_alert(hostname=hostname, trigger=triggerobj,fail_count=fail_count)

    return fail_count


def select_graph(host_id):
    result={}
    hostobj=models.Host.objects.get(id=host_id)
    cpu_list=models.CPUInfo.objects.filter(host=hostobj)
    mem_list=models.MemoryInfo.objects.filter(host=hostobj)
    trigger_list=hostobj.monitor_groups.templates.trigger.select_related()
    for trigger in trigger_list:
        data={}
        data[trigger.item.key] = []
        if trigger.service.name=='CPU':
            for i in cpu_list:
                data[trigger.item.key].append([int(i.create_date)*1000,getattr(i,trigger.item.key)])
            result[trigger.service.name]=data
        elif trigger.service.name=='Memory':
            for i in mem_list:
                data[trigger.item.key].append([int(i.create_date)*1000,getattr(i, trigger.item.key)])
            result[trigger.service.name] = data
    return result