import requests


class Covid:

    def __init__(self, token):
        self.token = token

    def get_daily_report(self, date):
        url = "https://covid-19-data.p.rapidapi.com/report/totals"

        querystring = {"date": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}

        headers = {
            'x-rapidapi-key': "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
        }

        headers['x-rapidapi-key'] = self.token
        querystring['date'] = date

        response = requests.request("GET", url, headers=headers, params=querystring)

        return response.json()

    def get_latest_totals(self):
        url = "https://covid-19-data.p.rapidapi.com/totals"

        querystring = {"format": "json"}

        headers = {
            'x-rapidapi-key': "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
        }
        headers['x-rapidapi-key'] = self.token

        response = requests.request("GET", url, headers=headers, params=querystring)

        return response.json()

    def get_latest_country_data_by_name(self, country_name):
        url = "https://covid-19-data.p.rapidapi.com/country"

        querystring = {"name": "XXX", "format": "json"}

        headers = {
            'x-rapidapi-key': "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
        }
        headers['x-rapidapi-key'] = self.token
        querystring["name"] = country_name

        response = requests.request("GET", url, headers=headers, params=querystring)

        return response.json()

    def get_daily_report_by_country_name(self, country_name, date):
        url = "https://covid-19-data.p.rapidapi.com/report/country/name"

        querystring = {"name": "XXXXXXXXX", "date": "XXXXXXXXXXXXXX"}

        headers = {
            'x-rapidapi-key': "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
        }
        headers['x-rapidapi-key'] = self.token
        querystring["name"] = country_name
        querystring["date"] = date
        response = requests.request("GET", url, headers=headers, params=querystring)

        return response.json()
