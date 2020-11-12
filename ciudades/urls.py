"""ciudades URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from ciudades.geostats.views import login_view, do_login_view, sign_up, test1, test2, logout_view
from ciudades.geostats.routers import apirouter

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', view=login_view, name="login_view"),
    url(r'^do_login/$', view=do_login_view, name="do_login_view"),
    url(r'^signup/$', view=sign_up, name="sign_up"),
    url(r'^test1/$', view=test1, name="test1"),
    url(r'^test2/$', view=test2, name="test2"),
    url(r'^logout/$', view=logout_view, name="logout_view"),
    path('api-auth/', include('rest_framework.urls')),
    path(r'api/', include(apirouter.urls)),
]
