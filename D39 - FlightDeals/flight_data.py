from data_manager import DataManager
from flight_search import FlightSearch
from dateutil import parser
from pytz import timezone
import pandas

data_map =[{'table_col': 'From City', 'kiwi_api': ['cityFrom']},
            {'table_col': 'From Airport', 'kiwi_api': ['flyFrom']},
            {'table_col': 'To City', 'kiwi_api': ['cityTo']},
            {'table_col': 'To Airport', 'kiwi_api': ['flyTo']},
            {'table_col': 'Depart Date', 'kiwi_api': ['local_departure']},
            {'table_col': 'Return Date', 'kiwi_api': ['route', -1, 'local_arrival']},
            {'table_col': 'Nights', 'kiwi_api': ['nightsInDest']},
            {'table_col': 'Price', 'kiwi_api': ['price']},
            {'table_col': 'Bag Fee (1)', 'kiwi_api': ['bags_price', '1']},
            {'table_col': 'Seats Available', 'kiwi_api': ['availability', 'seats']},
            {'table_col': 'Booking Link', 'kiwi_api': ['deep_link']},
           ]


class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, FlightSearch: FlightSearch, user_timezone):
        self.spreadsheet = DataManager
        self.flights = FlightSearch
        self.local_tz = timezone(user_timezone)
    

    def format_flights_to_tables(self, all_flights: list):

        def get_nested_data(data, keys):
            for key in keys:
                data = data[key]
            return data
        
        flights_by_city = {}
        for city in all_flights:
            
            dict = {}
            for col in data_map:
                dict[col['table_col']] = []

            for flight in city:
                for col in data_map:
                    column_name = col['table_col']
                    data = get_nested_data(flight, col['kiwi_api'])
                    
                    dict[column_name].append(data)

            city_flights_table = pandas.DataFrame(dict)
            city_name = city[0]['cityTo']
            flights_by_city[city_name] = city_flights_table

        return flights_by_city


    def format_flights_list_for_alert(self, city, city_flights):
        message = f'{"-" * 50}\n\nFLIGHTS TO {city.upper()}\n'
        
        rows = city_flights.last_valid_index()
        for i in range(rows):
            depart = self.format_date_time(city_flights.at[i, 'Depart Date'])
            return_d = self.format_date_time(city_flights.at[i, 'Return Date'])

            message += f'\n\n🛫 Depart: {depart["date"]}, {depart["time"]}'
            message += f'\n🛬 Return: {return_d["date"]}, {return_d["time"]}  (~{city_flights.at[i, "Nights"]} nights)'
            message += f'\n💰 ${city_flights.at[i, "Price"]:.2f}  (w/ 1 bag, +${city_flights.at[i, "Bag Fee (1)"]})'
            message += f'\n\nLink to view & book flight:\n\n{city_flights.at[i, "Booking Link"]}\n'
        
        message += f'\n\n{"-" * 50}\n'
        
        return message


    def format_date_time(self, date):
        date_time = parser.parse(date)
        local_dt = date_time.astimezone(self.local_tz)
        
        f_date = local_dt.astimezone().strftime('%b %d, %Y')
        f_time = local_dt.astimezone().strftime('%I:%M%p')

        return {'date': f_date, 'time': f_time}