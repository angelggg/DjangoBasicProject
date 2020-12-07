import pytest
from ciudades.geostats.models import *
from ciudades.geostats.content.handler import GeonamesHandler


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        if User.objects.filter(pk=110).exists():
            return
        user, new = User.objects.get_or_create(
            email="test@tesmail.com",
            first_name="test",
            id=110,
            password="test0Test",
            username="test45678"
        )
        user.set_password("test0Test")
        user.save()


# Some simple tests
@pytest.mark.django_db
class TestEntities:
    geonames_country_id = 2510769  # Spain
    geonames_region_id = 5332921  # California
    geonames_capital_id = 3169070  # Rome
    geonames_town_id = 2646393  # Huntingdon
    entities_handler = GeonamesHandler()

    def test_create_countryget_or_create(self):
        # Create town/region/country
        user = User.objects.get(pk=110)
        created = self.entities_handler.scrape_geonames(self.geonames_country_id, user)
        if created != 1:
            pytest.fail(f"Should have created 1 entity, created {created} instead")
        country = Country.objects.filter(pk=self.geonames_country_id)
        if not country.exists():
            pytest.fail(f"Could not find the entity on db")
            return
        country = country.first()
        if country.pk not in [userentity.object_id for userentity in user.entities.get_countries()]:
            pytest.fail(f"Entity not related with user {user.entities.count()}")

    def test_create_capital(self):
        user = User.objects.get(pk=110)
        created = self.entities_handler.scrape_geonames(self.geonames_capital_id, user)
        if created != 3:
            pytest.fail(f"Should have created 3 entity, created {created} instead")
        capital = Town.objects.filter(pk=self.geonames_capital_id)
        if not capital.exists():
            pytest.fail(f"Could not find the entity on db")
            return
        capital = capital.first()
        if capital.region is None or capital.country is None:
            pytest.fail(f"Missing related models")
        if capital.country.capital != capital:
            pytest.fail(f"Countrys capital not correct")
        if capital.pk not in [userentity.object_id for userentity in user.entities.get_towns()]:
            pytest.fail(f"Entity not related with user {user.entities.count()}")
