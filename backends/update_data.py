#!/usr/bin/env python
#-*- coding:utf-8 -*-
from web_models import models
def update_alert(hostname,trigger,fail_count):
    alertobj=models.Alert.objects.get(hostname=hostname,trigger=trigger)
    temp=alertobj.fail_count
    alertobj.fail_count=temp+1
    alertobj.save()
