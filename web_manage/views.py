from django.shortcuts import render,redirect
from web_models import models
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
    host_list = models.Host.objects.all()
    print("hosts:",host_list)
    return render(request,'monitor/hosts.html',{'host_list':host_list})


def host_detail(request,host_id):
    host_obj = models.Host.objects.get(id=host_id)
    return render(request,'monitor/host_detail.html',{'host_obj':host_obj})