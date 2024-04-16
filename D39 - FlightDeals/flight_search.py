import os
import requests
from datetime import date
from dateutil.relativedelta import relativedelta
import threading
from flight_data import FlightData

tequila_base_url = 'https://api.tequila.kiwi.com/'
API_KEY = os.environ.get('KIWI_TEQUILA_API_KEY')


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def __init__(self, user_params: dict):
        self.api_url = tequila_base_url
        self.headers = {'apikey': API_KEY, 'accept': 'application/json'}
        self.user_params = user_params
        self.search_params = self.get_search_params()

    def get_search_params(self):
        today = date.today()
        months_ahead = today + relativedelta(months=+self.user_params['month_range'])

        departure_date_from = today.strftime('%d/%m/%Y')
        departure_date_to = months_ahead.strftime('%d/%m/%Y')

        search_params = {
            'fly_from': 'city:' + self.user_params['fly_from_city_code'],
            'date_from': departure_date_from,
            'date_to': departure_date_to, 
            'nights_in_dst_from': self.user_params['min_stay_length'],
            'nights_in_dst_to': self.user_params['max_stay_length'],
            'curr': self.user_params['currency'],
            'locale': self.user_params['locale'],
            'select_airlines': ','.join(self.user_params['exclude_airlines']),
            'select_airlines_exclude': 'true',
            'limit': 10
            }

        return search_params


    def get(self, api_url, params):
        res = requests.get(url=api_url, params=params, headers=self.headers)
        res.raise_for_status()
        return res.json()


    def get_IATA_codes(self, cities: list):
        '''Expects list of cities in format: [{'city': name, 'country': country, ...}, {...}]. 
        Returns IATA codes as dict: {'cityname': code, ... }'''

        codes = {}
        threads = [threading.Thread(target=self.get_city_IATA_code, args=(city_data['city'], city_data['country'], codes)) for city_data in cities]
        [t.start() for t in threads]
        [t.join() for t in threads]

        return codes
    

    def get_city_IATA_code(self, city: str, country: str, codes):
        "Searches flight Location api for city. Gets code from matching result, and adds to passed-in codes dict." 
        
        url = self.api_url + 'locations/query'
        results = self.get(api_url=url, params={'term': city, 'location_types': 'city'})
        
        for result in results['locations']:
            if result['country']['name'] == country.title():
                codes[city] = result['code']
    
    
    def search_flights_for_all_cities(self, cities: list):
        ''' Searches for all roundtrip flights for each city in cities in the time frame between 
        the current date, up to the number of months specified in user search params (month_range).
        Expects cities to be in format [{'key': value, {...}}, {...}] '''
        # (See note at bottom)
    
        flights = {}
        for city_data in cities:
            try:
                self.search_flights_to_city(city_data['city'], city_data['iataCode'], city_data['highestPrice'], self.search_params, flights)
            except KeyError:
                pass
        
        return flights

    
    def search_flights_to_city(self, city, city_code, max_price, search_params, flights):
        url = self.api_url + 'v2/search'
        params = search_params
        
        destination_params = {
            'fly_to': 'city:' + city_code,
            'price_to': max_price 
            }
        params.update(destination_params)

        search_response = self.get(api_url=url, params=params)

        print(f'Flights under ${max_price} found for {city_code}: ', search_response['_results'])
        
        if search_response['data']:
            flight_data_set = self.create_flight_data(search_response['data'])
            flights[city] = flight_data_set

            # print({'city': search_response['data'][0]['cityTo'], 'price': search_response['data'][0]['price'], 'link': search_response['data'][0]['deep_link']})
    

    def create_flight_data(self, result_data):
        flights = []
        for flight in result_data:
            user_tz = self.user_params['timezone']
            from_city = flight['cityFrom']
            from_airport = flight['flyFrom']
            to_city = flight['cityTo']
            to_airport = flight['flyTo']
            date_depart = flight['local_departure']
            date_return = flight['route'][-1]['local_arrival']
            duration = flight['nightsInDest']
            price = flight['price']
            bag_fee_single = flight['bags_price']['1']
            seats_available = flight['availability']['seats']
            booking_link = flight['deep_link']

            flight = FlightData(user_tz, from_city, from_airport, to_city, to_airport, date_depart, date_return, duration, price, bag_fee_single, seats_available, booking_link)
            flights.append(flight)
        
        return flights


# # NOTE: in search_flights_for_all_cities(), tried using threads, but my implementation below (commented-out) has a bug --> only the last city 
        # in the list is actually searched for, and the search is done multiple times (total number of cities)
    # flights = {}
    # threads = [threading.Thread(target=self.search_flights_to_city, args=(city_data['iataCode'], city_data['highestPrice'], search_params, flights)) for city_data in cities]
    # [t.start() for t in threads]
    # [t.join() for t in threads]