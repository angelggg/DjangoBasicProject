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
from django.urls import path, include, re_path
from ciudades.geostats.views import login_view, do_login_view, sign_up_view, create_entity_view, user_entity_detail,\
    logout_view, create_entities_view, user_home_view, entities_list, user_stats
from ciudades.geostats.routers import apirouter

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', view=user_home_view, name="user_home_view"),
    re_path(r'^login/$', view=login_view, name="login_view"),
    re_path(r'^do_login/$', view=do_login_view, name="do_login_view"),
    re_path(r'^create_entities/$', view=create_entities_view, name="create_entities"),
    re_path(r'^signup/$', view=sign_up_view, name="sign_up"),
    re_path(r'^create_entity/$', view=create_entity_view, name="create_entity"),
    re_path(r'^logout/$', view=logout_view, name="logout_view"),
    re_path(r'^user-stats/$', view=user_stats, name="user_stats"),
    path(r'entity/<int:pk>/', user_entity_detail),
    path(r'entities-list/<str:kind>/', entities_list),
    path(r'api/', include(apirouter.urls)),
]
