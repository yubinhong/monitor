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
from django.conf.urls import url
from web_api import views
urlpatterns = [
    url(r'^get_config/',views.get_config),
    url(r'^report_server_data/',views.report_server_data2),
    url(r'graphs/$', views.graphs_gerator, name='get_graphs'),
    url(r'get_hosts_status/$',views.get_hosts_status,name='get_hosts_status'),
]