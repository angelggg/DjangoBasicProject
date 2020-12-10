from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from ciudades import settings
from ciudades.geostats.routers import apirouter
from ciudades.geostats.views import login_view, do_login_view, sign_up_view, create_entity_view, \
    user_entity_detail_view, \
    logout_view, create_entities_view, user_home_view, entities_list_view, user_stats_view, upload_detail_image

urlpatterns = [
                  re_path(r'^admin/', admin.site.urls),
                  re_path(r'^$', view=user_home_view, name="user_home_view"),
                  re_path(r'^login/$', view=login_view, name="login_view"),
                  re_path(r'^do_login/$', view=do_login_view, name="do_login_view"),
                  re_path(r'^create_entities/$', view=create_entities_view, name="create_entities"),
                  re_path(r'^signup/$', view=sign_up_view, name="sign_up"),
                  re_path(r'^create_entity/$', view=create_entity_view, name="create_entity"),
                  re_path(r'^logout/$', view=logout_view, name="logout_view"),
                  re_path(r'^user-stats/$', view=user_stats_view, name="user_stats"),
                  re_path(r'^upload-detail-image/$', view=upload_detail_image, name="upload_detail_image"),
                  path(r'entity/<int:pk>/', user_entity_detail_view),
                  path(r'entities-list/<str:kind>/', entities_list_view),
                  path(r'api/', include(apirouter.urls)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
