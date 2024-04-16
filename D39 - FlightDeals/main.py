from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData

user_params = {
    'fly_from_city_code': 'SJC',
    'timezone': 'America/Los_Angeles',
    'month_range': 6,
    'min_stay_length': 5,
    'max_stay_length': 30,
    'currency': 'USD',
    'currency_symbol': '$',
    'locale': 'en',
    'exclude_airlines': ['NK'], #spirit airlines
    }

# data = {'prices': [{'city': 'Paris', 'country': 'France', 'iataCode': 'PAR', 'highestPrice': 600, 'id': 2}, {'city': 'Tokyo', 'country': 'Japan', 'iataCode': 'TYO', 'highestPrice': 570, 'id': 3}, {'city': 'Sydney', 'country': 'Australia', 'iataCode': 'SYD', 'highestPrice': 700, 'id': 4}, {'city': 'Helsinki', 'country': 'Finland', 'iataCode': 'HEL', 'highestPrice': 700, 'id': 5}, {'city': 'Dublin', 'country': 'Ireland', 'iataCode': 'DUB', 'highestPrice': 670, 'id': 6}, {'city': 'Denpasar', 'country': 'Bali', 'id': 7}, {'city': 'Seoul', 'country': 'South Korea', 'iataCode': 'SEL', 'highestPrice': 800, 'id': 8}, {'city': 'Auckland', 'country': 'New Zealand', 'iataCode': 'AKL', 'highestPrice': 800, 'id': 9}, {'city': 'London', 'country': 'United Kingdom', 'iataCode': 'LON', 'highestPrice': 600, 'id': 10}, {'city': 'San Diego', 'country': 'United States', 'iataCode': 'SAN', 'highestPrice': 120, 'id': 11}, {'city': 'Marrakech', 'country': 'Morocco', 'iataCode': 'RAK', 'highestPrice': 700, 'id': 12}, {'city': 'Venice', 'country': 'Italy', 'iataCode': 'VCE', 'highestPrice': 700, 'id': 13}]}


def main():
    data_manager = DataManager()
    flight_search = FlightSearch(user_params)

    # First, get all data from the spreadsheet:
    data_manager.set_all_watched()

    # data_manager.all_watched_cities = data['prices']
    # print(data)

    # Then, check and update any cities that are missing IATA code:
    cities_missing_data = data_manager.get_cities_missing_code()
    if cities_missing_data:
        codes = flight_search.get_IATA_codes(cities_missing_data)
        cities_to_update = update_cities_data(cities_missing_data, codes)
        cities_updated = data_manager.update_spreadsheet_data(cities_to_update)

    # Then, search each city for all round trip flights in given timeframe, for less than given price limit:
    flights_found = flight_search.search_flights_for_all_cities(data_manager.cities_with_codes)
    
    # Finally, prepare and send cheap flight alert via email:
    if flights_found:
        message_content = get_message(flights_found) 
        message_subject = f'Flight Deals Alert: {", ".join(flights_found.keys())}'
        
        send_email(message_subject, message_content)


def update_cities_data(cities_missing_data: list, codes: dict):
    cities_to_update = []
    for city_data in cities_missing_data: 
        city_name = city_data['city']

        try:
            city_data['iataCode'] = codes[city_name]
        except KeyError:
            city_data['iataCode'] = ''
            print(f'Code not found for: {city_name} ({city_data["country"]})') 
        else:
            cities_to_update.append(city_data)
    
    return cities_to_update


def get_message(flights: dict):
    message = f'\nFlight deals found for: {", ".join(flights.keys())}\n\n'
    
    for city in flights:
        city_flight_section = format_flights_list_for_alert(city, flights[city])
        message += city_flight_section

    return message


def format_flights_list_for_alert(city, city_flights):
        symbol = user_params['currency_symbol']

        message = f'{"-" * 50}\n\nFLIGHTS TO {city.upper()}\n'
        f: FlightData
        for f in city_flights:
            message += f'\n\n🛫 Depart: {f.date_depart["date"]}, {f.date_depart["time"]}'
            message += f'\n🛬 Return: {f.date_return["date"]}, {f.date_return["time"]}  (~{f.duration} nights)'
            message += f'\n💰 {symbol}{f.price:.2f}  (w/ 1 bag, +{symbol}{f.bag_fee})'
            message += f'\n\nLink to view & book flight:\n\n{f.booking_link}\n'
        
        message += f'\n\n{"-" * 50}\n'
        
        return message


#TODO:
def send_email(subject: str, content: str):
    print(content)

 
main()