import requests


class City:

    def __init__(self, token):
        self.token = token

    def get_cities(self, limit, country_id, min_population):
        url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"

        querystring = {"limit": "3", "countryIds": "DE", "minPopulation": "5000000"}
        # 227ee4eea8mshe252fd0ec651c66p1ce50ajsn6b9eecfbd55a
        headers = {
            'x-rapidapi-key': "2xxxxxxxxxxxxxxxpxxxxxxcfbd55a",
            'x-rapidapi-host': "wft-geo-db.p.rapidapi.com"
        }
        headers['x-rapidapi-key'] = self.token
        querystring['limit'] = limit
        querystring['countryIds'] = country_id
        querystring['minPopulation'] = min_population

        response = requests.request("GET", url, headers=headers, params=querystring)

        return response.json()

    def get_city_details(self, city_id):
        url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities/REPLACE"

        url = url.replace("REPLACE", city_id)

        headers = {
            'x-rapidapi-key': "2xxxxxxxxxxxxxxxpxxxxxxcfbd55a",
            'x-rapidapi-host': "wft-geo-db.p.rapidapi.com"
        }

        headers['x-rapidapi-key'] = self.token

        response = requests.request("GET", url, headers=headers)

        return response.json()
