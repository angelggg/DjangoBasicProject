from typing import Optional, Union
from ciudades.geostats.models import Town, Country, Region
from ciudades.geostats.content.scraper import GeonamesScraper


class GeonamesHandler:
    entities_to_create = {}
    scraper = None

    @staticmethod
    def get_relevant_model(entity_type: int) -> Union[Town, Region, Country, None]:

        return {
            1: Country,
            2: Region,
            3: Town,
            4: Town
        }.get(entity_type)

    def scrape_geonames(self, geonames_id: int) -> bool:
        if not self.scraper:
            self.scraper = GeonamesScraper()
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
            self.create_entities()
            return True
        else:
            return False

    def create_entities(self) -> int:
        created_count = 0
        keys = list(self.entities_to_create.keys())
        keys.sort()
        for key in keys:
            model = self.get_relevant_model(key)
            entity, is_new = model.objects.get_or_create(**self.entities_to_create[key])
            created_count += 1 if is_new else 0
            if key == 4:
                if entity.country.capital != model:
                    Country.objects.filter(pk=entity.country.pk).update(capital=entity)
        return created_count