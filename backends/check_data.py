#!/usr/bin/env python
#-*- coding:utf-8 -*-
from web_models import models
import operator
from backends.select_data import select_failcount
from backends.insert_data import insert_alert
from backends.update_data import update_alert
from backends.delete_data import delete_alert
def check_report_data(service_type,hostname,data):
    result={'status':0,'message':[]}
    #hostobj=models.Host.objects.get(name=hostname)
    #monitorgroup = hostobj.monitor_groups
    #template = monitorgroup.templates
    #trigger_list=template.trigger.select_related().filter(service__name=service_type)
    trigger_list=models.Host.objects.get(name=hostname).monitor_groups.templates.trigger.\
        select_related().filter(service__name=service_type)
    for trigger in trigger_list:
        cmp=getattr(operator,trigger.operator_type)
        status=cmp(float(data[trigger.item.key]),float(trigger.threshold))
        if status:
            fail_count=select_failcount(hostname,trigger)
            fail_count +=1
            message = 'The host %s %s of %s is %s%%.' % \
                      (hostname, trigger.item.key, service_type, data[trigger.item.key])
            update_alert(hostname=hostname, trigger=trigger, fail_count=fail_count, message=message)
            if fail_count >=trigger.count:
                result['message'].append(message)
        else:
            delete_alert(hostname=hostname, trigger=trigger)


    if len(result['message'])>0:
        result['status']=1

    return result