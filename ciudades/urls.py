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
from ciudades.geostats.views import login_view, do_login_view, sign_up_view, create_entity_view, user_entity_detail,\
    logout_view, create_entities_view, user_home_view
from ciudades.geostats.routers import apirouter

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', view=user_home_view, name="user_home_view"),
    url(r'^login/$', view=login_view, name="login_view"),
    url(r'^do_login/$', view=do_login_view, name="do_login_view"),
    url(r'^create_entities/$', view=create_entities_view, name="create_entities"),
    url(r'^signup/$', view=sign_up_view, name="sign_up"),
    url(r'^create_entity/$', view=create_entity_view, name="create_entity"),
    url(r'^logout/$', view=logout_view, name="logout_view"),
    path(r'entity/<int:pk>/', user_entity_detail),
    path(r'api/', include(apirouter.urls)),
]
