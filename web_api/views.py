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
            services_list=template.services.select_related()
            data={}
            for service in services_list:
                data[service.service_type.name]=[service.service_type.plugin,service.interval]
        except Exception as e:
            data=''
            message='the hostname is no exists.'
            config['message'] = message
            print(e)
        config['status']='0'
        config['services']=data
        config=json.dumps(config)
        return HttpResponse(config)
    else:
        config['status']='1'
        config['message']='you must input param:hostname'
        config=json.dumps(config)
        return HttpResponse(config)

def report_server_data(request):
    result={'status':0,'message':''}
    data=request.POST.get('data',None)
    service_name=request.POST.get('service_name',None)
    hostname=request.POST.get('hostname',None)
    data=eval(data)
    try:
        hostobj = models.Host.objects.get(name=hostname)
        if service_name=='CPU':
           cpuobj=models.CPUInfo(host=hostobj,
                                 system=data['system'],
                                 steal=data['steal'],
                                 idle=data['idle'],
                                 iowait=data['iowait'],
                                 user=data['user'],
                                 nice=data['nice'])
           cpuobj.save()
        elif service_name=='Memory':
            memobj=models.MemoryInfo(host=hostobj,
                                     MemFree=data['MemFree'],
                                     Cached=data['Cached'],
                                     Buffers=data['Buffers'],
                                     MemUsage=data['MemUsage'],
                                     MemUsage_p=data['MemUsage_p'],
                                     MemTotal=data['MemTotal'])
            memobj.save()

    except Exception as e:
        result['status']=1
        result['message']=str(e)
        print(e)
    return HttpResponse(json.dumps(result))