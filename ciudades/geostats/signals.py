from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver

from ciudades.geostats.models import UserEntity, UserStats


@receiver(post_save, sender=UserEntity)
def update_user_stats(sender, **kwargs):

    """On saving an user_entity -> Update stats for the user"""
    instance = kwargs.get('instance')
    user = instance.user
    entity_type = instance.content_type.model
    content_type = ContentType.objects.get(model=entity_type)
    ustats, new = UserStats.objects.get_or_create(user=user, content_type=content_type)
    entities_id = user.entities.get_relevant_query(entity_type, user).values_list("object_id", flat=True)
    values = content_type.model_class().objects.filter(id__in=entities_id).aggregate(population=Avg("population"),
                                                                                     elevation=Avg("elevation"))
    ustats.mean_elevation = values.get("elevation", 0)
    ustats.mean_population = values.get("population", 0)

    ustats.save()
