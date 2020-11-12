from rest_framework import viewsets
from ciudades.geostats.models import Country, Town, Region
from ciudades.geostats.serializers import CountrySerializer, RegionSerializer, TownSerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class TownViewSet(viewsets.ModelViewSet):
    queryset = Town.objects.all()
    serializer_class = TownSerializer

class getGeoPlaces(viewsets.GenericViewSet):
    pass