from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


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
    capital = models.OneToOneField(to="Town", null=True, blank=True, related_name="capital_of",
                                   on_delete=models.CASCADE)


class Region(GeoEntity):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class Town(GeoEntity):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)


class UserEntityManager(models.Manager):

    town_content_type = None
    region_content_type = None
    country_content_type = None

    def get_towns(self, get_entity:bool=False):
        if self.town_content_type is None:
            self.town_content_type = ContentType.objects.get(model="town")
        return super().get_queryset().filter(content_type=self.town_content_type)

    def get_regions(self):
        if self.region_content_type is None:
            self.region_content_type = ContentType.objects.get(model="region")
        return super().get_queryset().filter(content_type=self.region_content_type)

    def get_countries(self):
        if self.country_content_type is None:
            self.country_content_type = ContentType.objects.get(model="country")
        return super().get_queryset().filter(content_type=self.country_content_type)


class UserEntity(models.Model):

    objects = UserEntityManager()

    # We'll use it as a relation between user and places selected by
    choices = models.Q(app_label='geostats', model='town') | \
              models.Q(app_label='geostats', model='region') | \
              models.Q(app_label='geostats', model='country')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="entities")
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=choices)
    entity = GenericForeignKey()

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

