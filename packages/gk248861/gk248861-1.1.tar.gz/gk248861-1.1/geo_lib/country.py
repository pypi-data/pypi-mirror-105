import requests


class Country:

    def __init__(self, token):
        self.token = token

    def get_country_details(self, country_id):
        url = "https://wft-geo-db.p.rapidapi.com/v1/geo/countries/REPLACE"

        url = url.replace("REPLACE", country_id)

        headers = {
            'x-rapidapi-key': "XXXXXXXXXXXXXXXXXXXXXXXXXX",
            'x-rapidapi-host': "wft-geo-db.p.rapidapi.com"
        }

        headers['x-rapidapi-key'] = self.token

        response = requests.request("GET", url, headers=headers)

        return response.json()

    def get_country_region_details(self, country_id, region_code):
        url = "https://wft-geo-db.p.rapidapi.com/v1/geo/countries/COUNTRY_ID/regions/REGION_CODE"
        url = url.replace("COUNTRY_ID", country_id)
        url = url.replace("REGION_CODE", region_code)

        headers = {
            'x-rapidapi-key': "227ee4eea8mshe252fd0ec651c66p1ce50ajsn6b9eecfbd55a",
            'x-rapidapi-host': "wft-geo-db.p.rapidapi.com"
        }
        headers['x-rapidapi-key'] = self.token

        response = requests.request("GET", url, headers=headers)

        return response.json()
