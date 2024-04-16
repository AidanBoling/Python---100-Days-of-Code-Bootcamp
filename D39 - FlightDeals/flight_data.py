from dateutil import parser
from pytz import timezone    

class FlightData:
    def __init__(self, user_timezone, from_city, from_airport, to_city, to_airport, date_depart, date_return, duration, price, bag_fee_single, seats_available, booking_link):
        self.local_tz = timezone(user_timezone)
        self._from_city = from_city
        self._from_airport = from_airport
        self._to_city = to_city
        self._to_airport = to_airport
        self._date_depart = date_depart
        self._date_return = date_return
        self._duration = duration
        self._price = price
        self._bag_fee = bag_fee_single
        self._seats_available = seats_available
        self._booking_link = booking_link

    @property
    def from_city(self):
        return self._from_city
    
    @property
    def from_airport(self):
        return self._from_airport

    @property
    def to_city(self):
        return self._to_city

    @property
    def to_airport(self):
        return self._to_airport

    @property
    def date_depart(self):
        return self.format_date_time_to_local(self._date_depart)

    @property
    def date_return(self):
        return self.format_date_time_to_local(self._date_return)

    @property
    def duration(self):
        return self._duration
    
    @property
    def price(self):
        return self._price

    @property
    def bag_fee(self):
        return self._bag_fee
    
    @property
    def seats_available(self):
        return self._seats_available
    
    @property
    def booking_link(self):
        return self._booking_link


    def format_date_time_to_local(self, datetime: str):
        date_time = parser.parse(datetime)
        local_dt = date_time.astimezone(self.local_tz)
        
        f_date = local_dt.astimezone().strftime('%b %d, %Y')
        f_time = local_dt.astimezone().strftime('%I:%M%p')

        return {'date': f_date, 'time': f_time}