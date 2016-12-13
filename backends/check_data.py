#!/usr/bin/env python
#-*- coding:utf-8 -*-
from web_models import models
import operator
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
            result['message'].append('The host %s %s of %s is %s.' %
                                     (hostname,trigger.item.key,service_type,data[trigger.item.key]))

    if len(result['message'])>0:
        result['status']=1

    return result