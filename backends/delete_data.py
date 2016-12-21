#!/usr/bin/env python
#-*- coding:utf-8 -*-
from web_models import models
def delete_alert(hostname,trigger):
    try:
        alertobj=models.Alert.objects.get(hostname=hostname,trigger=trigger)
        alertobj.delete()
        return 'ok'
    except Exception as e:
        return str(e)
