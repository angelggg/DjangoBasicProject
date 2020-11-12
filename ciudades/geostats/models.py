from django.db import models
from django.contrib.auth.models import User


class GeoEntity(models.Model):
    name = models.TextField(max_length=250, null=False, blank=False)
    population = models.IntegerField()
    elevation = models.IntegerField()
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Country(GeoEntity):
    country_code = models.CharField(max_length=2, blank=False, null=False, db_index=True, unique=True)
    capital = models.OneToOneField(to="Town", null=True, blank=True, related_name="capital_of", on_delete=models.CASCADE)


class Region(GeoEntity):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class Town(GeoEntity):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)