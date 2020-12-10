from typing import Union

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from ciudades.geostats.content.scraper import GeonamesScraper
from ciudades.geostats.models import Town, Country, Region, UserEntity


class GeonamesHandler:
    entities_to_create = {}
    scraper = None
    user = None

    @staticmethod
    def get_relevant_model(entity_type: int) -> Union[Town, Region, Country, None]:

        return {
            1: Country,
            2: Region,
            3: Town,
            4: Town
        }.get(entity_type)

    def scrape_geonames(self, geonames_id: int, user: User) -> int:
        if not self.scraper:
            self.scraper = GeonamesScraper()
        self.user = user
        entity_info = self.scraper.scrape_geonames(geonames_id)
        entity_type = list(entity_info.keys())[0]
        self.entities_to_create.update(entity_info)

        if entity_type in (3, 4):
            # Create / check region
            parent_id = self.entities_to_create[entity_type].pop('parent_id')
            entity_info = self.scraper.scrape_geonames(parent_id)
            entity_type = list(entity_info.keys())[0]
            self.entities_to_create.update(entity_info)

        if entity_type == 2:
            parent_id = self.entities_to_create[entity_type].pop('parent_id')
            entity_info = self.scraper.scrape_geonames(parent_id)
            self.entities_to_create.update(entity_info)
        if self.entities_to_create:
            return self.create_entities()
        else:
            return 0

    def create_entities(self) -> int:
        created_count = 0
        keys = list(self.entities_to_create.keys())
        keys.sort()
        for key in keys:
            model = self.get_relevant_model(key)
            entity, is_new = model.objects.get_or_create(**self.entities_to_create[key],
                                                         defaults={'creator_id': self.user.pk})
            created_count += 1 if is_new else 0
            if self.user and entity.pk:
                self.create_userentity(entity)
            if key == 4:
                if entity.country.capital != model:
                    Country.objects.filter(pk=entity.country.pk).update(capital=entity)
        return created_count

    def create_userentity(self, entity) -> tuple:
        return UserEntity.objects.get_or_create(user=self.user,
                                                object_id=entity.pk,
                                                content_type=ContentType.objects.get_for_model(
                                                    entity, for_concrete_model=False))
