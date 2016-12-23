from django.shortcuts import render,redirect,HttpResponse
from web_models import models
from backends.select_data import select_config_data
from backends.check_data import check_alive
import json
# Create your views here.


def login_require(func):
    def _deco(request):
        if request.session.get('current_user_id'):
            return func(request)
        else:
            return redirect('/login/')

    return _deco


def login(request):
    ret={'message':''}
    if request.method=='POST':
        user=request.POST.get('username',None)
        pwd=request.POST.get('password',None)
        if user and pwd:
            try:
                userobj=models.Admin.objects.get(username=user,password=pwd)
                request.session["current_user_id"]=userobj.id
                return redirect('/index/')
            except Exception as e:
                ret['message']='用户名或密码错误'
    else:
        if request.session.get('current_user_id'):
            return redirect('/index/')
    return render(request,"login.html",ret)


def logout(request):
    del request.session['current_user_id']
    return redirect('/login/')


@login_require
def index(request):
    return render(request,"monitor/index.html")


def dashboard(request):
    return render(request,'monitor/dashboard.html')


def triggers(request):
    return render(request,'monitor/triggers.html')


def hosts(request):
    uid = request.session.get('current_user_id', None)
    host_list = models.Host.objects.filter(monitor_groups__user__admin__id=uid)
    return render(request,'monitor/hosts.html',{'host_list':host_list})


def host_detail(request,host_id):
    host_obj = models.Host.objects.get(id=host_id)
    config = select_config_data(host_obj.name)

    monitored_services = {
            "services":{},
            #"sub_services": {} #存储一个服务有好几个独立子服务 的监控,比如网卡服务 有好几个网卡
        }

    #template=host_obj.monitor_groups.templates

    monitored_services['services'] = config
    count=models.Alert.objects.filter(hostname=host_obj.name)

    return render(request,'monitor/host_detail.html',{'host_obj':host_obj,'monitored_services':monitored_services,'count':count})


def get_hosts_status(request):
    uid=request.session.get('current_user_id',None)
    data=[]
    if uid:
        #host_list=models.Admin.objects.get(id=uid).select_related().select_related()
        #userobj=models.Admin.objects.get(id=uid).user
        #monitorgroup=models.MonitorGroup.objects.get(user=userobj)
        host_list=models.Host.objects.filter(monitor_groups__user__admin__id=uid)
        for host in host_list:
            status=check_alive(host.ip_addr)
            data.append({'id':host.id,'status':status})
    return HttpResponse(json.dumps(data))


def trigger_list(request):
    hostname=request.GET.get('by_host_name')
    trigger_data=models.Alert.objects.filter(hostname=hostname)
    return render(request,'monitor/trigger_list.html',{'trigger_list':trigger_data})

