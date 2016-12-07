from django.shortcuts import render,HttpResponse
from web_models import models
import json
# Create your views here.
def index(request):
    print(type(request))
    return HttpResponse('ok')

def get_config(request):
    config={'message':""}
    hostname=request.GET.get('hostname',None)
    if hostname:
        try:
            hostobj=models.Host.objects.get(name=hostname)
            monitorgroup=hostobj.monitor_groups
            template=monitorgroup.templates
            service_list=template.services.select_related()
            data={}
            for item in service_list:
                data[item.name]="plugin_name:"+item.plugin+",interval:"+str(item.interval)
        except Exception as e:
            data=''
            message='the hostname is no exists.'
            config['message'] = message
        config['status']='0'
        config['data']=data
        config=json.dumps(config)
        return HttpResponse(config)
    else:
        config['status']='1'
        config['message']='you must input param:hostname'
        config=json.dumps(config)
        return HttpResponse(config)
def report_server_data(request):
    data=request.POST.get('data',None)
    return HttpResponse