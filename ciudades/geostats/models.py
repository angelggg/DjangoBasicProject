from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# We'll use it as a relation between user and places selected by
choices = models.Q(app_label='geostats', model='town') | \
          models.Q(app_label='geostats', model='region') | \
          models.Q(app_label='geostats', model='country')


class GeoEntity(models.Model):
    """Generic to define all entities"""
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
    """
    Custom manager to ease operations with userentities
    """
    town_content_type = None
    region_content_type = None
    country_content_type = None

    def get_towns(self, user: User):
        if self.town_content_type is None:
            self.town_content_type = ContentType.objects.get(model="town")
        return super().get_queryset().filter(content_type=self.town_content_type, user=user)

    def get_regions(self, user: User):
        if self.region_content_type is None:
            self.region_content_type = ContentType.objects.get(model="region")
        return super().get_queryset().filter(content_type=self.region_content_type, user=user)

    def get_countries(self, user: User):
        if self.country_content_type is None:
            self.country_content_type = ContentType.objects.get(model="country")
        return super().get_queryset().filter(content_type=self.country_content_type, user=user)

    def get_relevant_query(self, entity: str, user: User):
        # Related functions
        return {
            'country': self.get_countries(user=user),
            'region': self.get_regions(user=user),
            'town': self.get_towns(user=user)}.get(entity)


class UserEntity(models.Model):
    objects = UserEntityManager()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="entities")
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=choices)
    entity = GenericForeignKey()

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')


class UserEntityImage(models.Model):
    user_entity = models.ForeignKey(UserEntity, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/%Y/')


class UserStats(models.Model):
    # Here we'll save each users stats for each kind of entity type

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mean_population = models.IntegerField(default=0, blank=False, null=False)
    mean_elevation = models.IntegerField(default=0, blank=False, null=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=choices)

    class Meta:
        unique_together = ('user', 'content_type')
