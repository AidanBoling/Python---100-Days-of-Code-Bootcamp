import os
import requests

USERNAME = os.environ.get('SHEETY_USERNAME')
AUTH = os.environ.get('SHEETY_FLIGHTS_AUTH')

project_name = 'flightDeals'
sheet_name = 'prices'

sheety_url = f'https://api.sheety.co/{USERNAME}/{project_name}/{sheet_name}'


class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.api_url = sheety_url
        self.headers = {'Authorization': 'Bearer ' + AUTH, 'Content-Type': 'application/json'}
        self.all_watched_cities = []
        self.cities_missing_code = []
        self.cities_with_codes = []
        # later: set self.all_watched_cities = self.set_all_watched, so runs on instantiation

    def set_all_watched(self):
        data = self.get_spreadsheet_data()
        self.all_watched_cities = data['prices']

    def put(self, api_url, body):
        res = requests.put(url=api_url, json=body, headers=self.headers)
        res.raise_for_status()
        return res.json()


    def get_spreadsheet_data(self):
        res = requests.get(url=self.api_url, headers=self.headers)
        return res.json()
    

    def get_cities_missing_code(self):
        for row in self.all_watched_cities:
            try:
                if not row['iataCode']:
                    self.cities_missing_code.append(row)
                else:
                    self.cities_with_codes.append(row)
            except KeyError:
                    self.cities_missing_code.append(row)

        return self.cities_missing_code


    def update_spreadsheet_data(self, cities_data: list):
        '''Expects cities_data to be list of dicts, one for each row to be updated, formatted per Sheety API docs: 
        [{'<column>': data, {...}}, {...}]'''

        responses = []
        for city_data in cities_data:
            id = city_data.pop('id')
            url = self.api_url + f'/{id}'
            row = {'price': city_data}
            
            res = self.put(api_url=url, body=row)
            
            responses.append(res['price'])

        self.cities_with_codes.extend(responses)
        print('Cities updated with IATA code: ', responses)
        # print(self.cities_with_codes)
        
        return responses