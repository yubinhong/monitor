from django.shortcuts import render,HttpResponse
#from web_models import models
from backends.insert_data import insert_report_data
from backends.select_data import select_config_data,select_email
from backends.check_data import check_report_data
from backends.alert import send_mail
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
        result=check_report_data(service_name,hostname,data)
        if result['status']:
            email=select_email(hostname)
            for content in result['message']:
                send_mail([email],'alert',content)
    except Exception as e:
        result['status']=1
        result['message']=str(e)
        print(e)
    return HttpResponse(json.dumps(result))