from django.shortcuts import render,HttpResponse
from web_models import models
from backends.insert_data import insert_report_data
from backends.select_data import select_config_data,select_email,select_graph,select_appkey
from backends.check_data import check_report_data
from backends.alert import send_mail,send_api
import json
from backends.check_data import check_alive
# Create your views here.

def get_config(request):
    config={'message':""}
    hostname=request.GET.get('hostname',None)
    if hostname:
        try:
            data=select_config_data(hostname)
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
    print(data)
    try:
        insert_report_data(hostname,service_name,data)
        re=check_report_data(service_name,hostname,data)
        if re['status']:
            #email=select_email(hostname)
            appkey=select_appkey(hostname)
            for content in re['message']:
                #send_mail([email],'alert',content)
                send_api(appkey,content,re['id'],hostname)

    except Exception as e:
        result['status']=1
        result['message']=str(e)
        print(e)
    return HttpResponse(json.dumps(result))

def graphs_gerator(request):
    host_id=request.GET.get('host_id')
    result=select_graph(host_id)
    return HttpResponse(json.dumps(result))

def get_hosts_status(request):
    uid=request.session.get('current_user_id',None)
    data=[]
    if uid:
        #host_list=models.Admin.objects.get(id=uid).select_related().select_related()
        #userobj=models.Admin.objects.get(id=uid).user
        #monitorgroup=models.MonitorGroup.objects.get(user=userobj)
        host_list=models.Host.objects.filter(monitor_groups__user__admin__id=uid)
        for host in host_list:
            data.append({'id':host.id,'status':host.status})
    return HttpResponse(json.dumps(data))