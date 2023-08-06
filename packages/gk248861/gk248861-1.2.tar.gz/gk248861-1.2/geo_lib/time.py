import requests


class Time:

    def __init__(self, token):
        self.token = token

    def get_time_zones(self, limit):
        url = "https://wft-geo-db.p.rapidapi.com/v1/locale/timezones"

        querystring = {"limit": "x"}

        headers = {
            'x-rapidapi-key': "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            'x-rapidapi-host': "wft-geo-db.p.rapidapi.com"
        }

        querystring["limit"] = limit
        headers["x-rapidapi-key"] = self.token

        response = requests.request("GET", url, headers=headers, params=querystring)

        return response.json()
