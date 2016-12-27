"""monitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from web_manage import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/',views.index),
    url(r'login/',views.login),
    url(r'^api/',include('web_api.urls')),
    url(r'dashboard/$',views.dashboard,name='dashboard'),
    url(r'triggers/$',views.triggers,name='triggers'),
    url(r'hosts/$',views.hosts ,name='hosts'),
    url(r'hosts/(\d+)/$',views.host_detail ,name='host_detail'),
    url(r'logout/$',views.logout),

    url(r'trigger_list/$',views.trigger_list ,name='trigger_list'),

]
