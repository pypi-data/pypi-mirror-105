import requests


class Help:

    def __init__(self, token):
        self.token = token

    def get_list_of_countries(self):
        url = "https://covid-19-data.p.rapidapi.com/help/countries"

        querystring = {"format": "json"}

        headers = {
            'x-rapidapi-key': "XXXXXXXXXXXXXXXXX",
            'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
        }
        headers['x-rapidapi-key'] = self.token
        response = requests.request("GET", url, headers=headers, params=querystring)

        return response.json()

    def get_documentation(self):
        url = "https://covid-19-data.p.rapidapi.com/docs.json"
        # 227ee4eea8mshe252fd0ec651c66p1ce50ajsn6b9eecfbd55a
        headers = {
            'x-rapidapi-key': "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
        }
        headers['x-rapidapi-key'] = self.token
        response = requests.request("GET", url, headers=headers)

        return response.json()
