import streamlit as st
from datetime import datetime, timedelta
from functools import wraps
from warnings import warn

class DotDict(dict):
    """Dot notation (signature: dict.key) access to dictionary attributes."""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class Table:
    """
    Class that represents tables in a restaraunt.
    """
    def __init__(self, name: str, number_of_seats: int):
        """
        Initializer of the class.
        """
        self.__name = name
        self.__number_of_seats = number_of_seats
        self.__status = 'Free'
        self.__bookings = list()
    
    def __update_status(self):
        """
        Method that updates status according to current time.
        """
        tmp = 'Free'
        for j in range(len(self.__bookings)):
            if self.__bookings[j].from_datetime <= datetime.now() <= self.__bookings[j].to_datetime:
                tmp = 'Taken (with booking)'
        if self.__status == 'Taken (without booking)' and tmp == 'Free':
            pass
        else:
            self.__status = tmp            
    
    def __updating(func):
        """
        A decorator that updates Table's status each time before displaying, modifying or using status information.
        """
        @wraps(func)
        def wrapper(inst, *args, **kwargs):
            inst.__update_status()
            return func(inst, *args, **kwargs)
        return wrapper
        
    @property
    def name(self):
        """
        Returns the name of the Table in the database.
        """
        return self.__name
    
    @property
    def number_of_seats(self):
        """
        Returns a number of seats of the Table.
        """
        return self.__number_of_seats
    
    @property
    @__updating
    def status(self):
        """
        Returns the current status of a Table.
        """
        return self.__status
    
    @property
    def bookings(self):
        """
        Returns bookings list of a Table.
        """
        return self.__bookings
    
    @__updating
    def take(self):
        """
        Takes the table or notifies that it's already taken.
        """
        if self.__status == 'Free':
            self.__status = 'Taken (without booking)'
        else:
            warn(f"Cannot take an already taken table. Table name: '{self.__name}'.")
    
    @__updating
    def release(self):
        """Releases the table. If it was taken with a booking, shifts the mentioned booking ending time to current moment.
        """
        if self.__status == 'Taken (with booking)':
            for i in range(len(self.__bookings)):
                if self.__bookings[i].from_datetime <= datetime.now() <= self.__bookings[i].to_datetime:
                    self.__bookings[i].to_datetime = datetime.now() - timedelta(minutes=1)
                    break
        self.__status = 'Free'
        
    @__updating
    def __str__(self):
        """
        String representation of a Table.
        """
        return f'{self.__name} ({self.__number_of_seats} seats) - {self.__status}'
    
    @__updating
    def add_booking(self, name: str, phone: str, from_datetime: datetime, to_datetime: datetime):
        """Adds a booking to the Table or notifies that it is already booked at that time.

        Args:
            name (str): customer's name
            phone (str): customer's phone number
            from_datetime (datetime): starting datetime of booking
            to_datetime (datetime): ending datetime of booking
        """
        overlap = None
        # Checks if there exists time overlap between current booking and already existing ones.
        for booking in self.__bookings:
            latest_start = max(from_datetime, booking.from_datetime)
            earliest_end = min(to_datetime, booking.to_datetime)
            delta = earliest_end - latest_start
            overlap = max(timedelta(), delta)
            if overlap:
                break
            
        if overlap:
            st.error('This table is already booked at this time.')
        else:
            # Saving booking information:
            self.__bookings.append(DotDict({'name': name,
                                            'phone': phone,
                                            'from_datetime': from_datetime,
                                            'to_datetime': to_datetime}))
            st.success('The table is booked successfully!')
            
    @__updating
    def is_free(self):
        """
        Checks if the Table is currently free.
        """
        return self.__status == 'Free'
    
    @__updating
    def is_taken(self):
        """
        Checks if the table is currently taken.
        """
        return self.__status != 'Free'
    
    def delete_booking(self, booking_to_delete_idx):
        """
        Deletes booking by index.
        """
        del self.__bookings[booking_to_delete_idx]