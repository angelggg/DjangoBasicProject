from ciudades.geostats.models import Town, Country, Region

import requests
from typing import Optional


class GeonamesScraper:

    entity_types = {
        "country": 1,
        "region": 2,
        "town": 3,
        "capital": 4
    }
    parsed_response = None

    def get_entity_type(self) -> str:
        fcode = self.parsed_response.get("fcodeName")
        fclName = self.parsed_response.get("fclName")

        if fclName == 'city, village,...':
            if fcode == "capital of a political entity":
                # Capital, modify country in case.
                return "capital"
            else:
                # Not a capital
                return "town"

        elif fcode == "first-order administrative division":
            # Region
            return "region"

        elif fcode == "independent political entity":
            # Country
            return "country"

    def scrape_geonames(self, entity_id: int) -> Optional[dict]:
        # Get info from their api
        query_url = f"https://www.geonames.org/getJSON?id={entity_id}&style=gui"
        response = requests.get(query_url)
        if response.status_code == 200:
            self.parsed_response = response.json()
            # Check what kind of entity we are dealing with.
            entity_type = self.get_entity_type()
            process_flag = self.entity_types.get(entity_type)

            if not process_flag:
                print("Could not find the entity type")
                return
            if process_flag in (3, 4):
                return {process_flag: self.get_create_dict_town()}
            if process_flag == 2:
                return {process_flag: self.get_create_dict_region()}
            if process_flag == 1:
                return {process_flag: self.get_create_dict_country()}

        else:
            print(f"Response status code = {response.status_code}")

    def get_general_reqs(self) -> dict:
        # Info needed by any object
        return {
            'id': self.parsed_response.get("geonameId"),
            'name': self.parsed_response.get("name")
        }

    def get_general_opts(self) -> dict:
        # Optional info needed by any object
        return {
            'population': self.parsed_response.get("population"),
            'elevation': self.parsed_response.get("astergdem")
        }

    def get_town_reqs(self) -> dict:
        # Needed by every town object
        region_id = self.parsed_response.get("adminId1")
        country_id = self.parsed_response.get("countryId")

        return {
            'region_id': region_id,
            'parent_id': region_id,
            'country_id': country_id,
        }

    def get_region_reqs(self) -> dict:
        # Needed by every region object
        country_id = self.parsed_response.get("countryId")
        return {
            'country_id': country_id,
            'parent_id': country_id
        }

    def get_country_reqs(self):
        return {
            'country_code': self.parsed_response.get("countryCode")
        }

    def get_create_dict_town(self) -> dict:
        general_reqs = {**self.get_general_reqs(),
                        **self.get_town_reqs()}
        optional_reqs = self.get_general_opts()
        return {**general_reqs, **optional_reqs}

    def get_create_dict_region(self) -> dict:
        # Check if we have enough info...
        general_reqs = {**self.get_general_reqs(),
                        **self.get_region_reqs()}
        optional_reqs = self.get_general_opts()
        return {**general_reqs, **optional_reqs}

    def get_create_dict_country(self) -> dict:
        general_reqs = {**self.get_general_reqs(),
                        **self.get_country_reqs()}
        optional_reqs = self.get_general_opts()
        return {**general_reqs, **optional_reqs}
