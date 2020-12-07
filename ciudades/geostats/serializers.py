from django.contrib.auth.models import User
from rest_framework import serializers
from ciudades.geostats.models import GeoEntity, Country, Region, Town


class GeoEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoEntity
        fields = ('id', 'name', 'population', 'elevation', 'creator',)


class CountrySerializer(GeoEntitySerializer):
    class Meta:
        model = Country
        fields = GeoEntitySerializer.Meta.fields + ('country_code', 'capital',)


class RegionSerializer(GeoEntitySerializer):
    class Meta:
        model = Region
        fields = GeoEntitySerializer.Meta.fields + ('country',)


class TownSerializer(GeoEntitySerializer):
    class Meta:
        model = Town
        fields = GeoEntitySerializer.Meta.fields + ('country', 'region',)


class UserEntitiesSerializer(serializers.ModelSerializer):
    entities = serializers.SerializerMethodField()

    def get_entities(self, obj):
        return list(map(lambda x: {'id': x.entity.id, 'name': x.entity.name, 'ctype': x.content_type.model},
                        obj.entities.all()))

    class Meta:
        model = User
        fields = ('id', 'username', 'entities',)
