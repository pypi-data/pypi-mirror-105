import requests


class Administration:

    def __init__(self, token):
        self.token = token

    def get_currencies(self, country_id, limit):
        url = "https://wft-geo-db.p.rapidapi.com/v1/locale/currencies"

        querystring = {"countryId": "X", "limit": "X"}

        headers = {
            'x-rapidapi-key': "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            'x-rapidapi-host': "wft-geo-db.p.rapidapi.com"
        }
        querystring["countryId"] = country_id
        querystring["limit"] = limit
        headers['x-rapidapi-key'] = self.token

        response = requests.request("GET", url, headers=headers, params=querystring)

        return response.json()

    def get_languages(self, limit):
        url = "https://wft-geo-db.p.rapidapi.com/v1/locale/languages"

        querystring = {"limit": "x"}

        headers = {
            'x-rapidapi-key': "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            'x-rapidapi-host': "wft-geo-db.p.rapidapi.com"
        }
        headers['x-rapidapi-key'] = self.token
        querystring['limit'] = limit
        response = requests.request("GET", url, headers=headers, params=querystring)

        return response.json()
