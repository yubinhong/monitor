#!/usr/bin/env python
#-*- coding:utf-8 -*-
from web_models import models
def update_alert(hostname,trigger,fail_count,message):
    alertobj=models.Alert.objects.get(hostname=hostname,trigger=trigger)
    alertobj.fail_count=fail_count
    alertobj.message=message
    alertobj.save()
    return alertobj.id
