import pytest
from ciudades.geostats.models import *
from ciudades.geostats.content.handler import GeonamesHandler


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        User.objects.create(
            email="test@tesmail.com",
            first_name="test",
            id=110,
            password="test",
            username="tes1t"
        )


@pytest.mark.django_db
class TestEntities:

    geonames_country_id = 2510769 # Spain
    geonames_region_id = 5332921 # California
    geonames_capital_id = 3169070 # Rome
    geonames_town_id = 2646393 # Huntingdon
    entities_handler = GeonamesHandler()


    def test_create_country(self):
        # Create town/region/country
        user = User.objects.get(pk=110)
        created = self.entities_handler.scrape_geonames(self.geonames_country_id, user)
        if created != 1:
            pytest.fail(f"Should have created 1 entity, created {created} instead")
        if not Country.objects.filter(pk=self.geonames_country_id).exists():
            pytest.fail(f"Could not find the entity on db")

    def test_create_capital(self):
        user = User.objects.get(pk=110)
        created = self.entities_handler.scrape_geonames(self.geonames_capital_id, user)
        if created != 3:
            pytest.fail(f"Should have created 3 entity, created {created} instead")
        capital = Town.objects.get(pk=self.geonames_capital_id)
        if capital.region == None or capital.country == None:
            pytest.fail(f"Missing related models")
        if capital.country.capital != capital:
            pytest.fail(f"COuntry¡s capital not correct")

