from rest_framework.routers import DefaultRouter

from ciudades.geostats.viewsets import CountryViewSet, TownViewSet, RegionViewSet, UserEntitiesViewSet

apirouter = DefaultRouter()

apirouter.register(r'country', viewset=CountryViewSet)
apirouter.register(r'region', viewset=RegionViewSet)
apirouter.register(r'town', viewset=TownViewSet)
apirouter.register(r'userentities', viewset=UserEntitiesViewSet)
