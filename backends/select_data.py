#!/usr/bin/env python
#-*- coding:utf-8 -*-
from web_models import models


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