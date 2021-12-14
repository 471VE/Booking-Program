import streamlit as st
from datetime import datetime, timedelta, time
from .helpers import select_table, print_table_statistics, no_formal_mistakes

def booking_page(state):
    """
    Creates 'Booking' page.
    """
    st.title('Booking')

    # Booking form:
    st.header('Booking Form')    
    name = st.text_input('Name:')
    name_error_slot = st.empty()
    phone = st.text_input('Phone number:')
    phone_error_slot = st.empty()
    date_col, from_col, to_col = st.columns(3)
    date = date_col.date_input('Date')
    from_time = from_col.time_input('From', value=time(10, 0))
    to_time = to_col.time_input('To', value=time(10, 30))
    time_error_slot = st.empty()
    
    # Converting to datetime (for reducing the number of calculations later on):
    from_datetime = datetime.combine(date, from_time)
    to_datetime = datetime.combine(date, to_time) if to_time >= from_time else datetime.combine(date + timedelta(days=1), to_time)
    
    # Selectbox of tables:
    booking_slot = st.empty()
    table_to_book_idx = select_table(booking_slot, state.tables)
    
    if st.button('Submit'):
        # Checks if the booking form has no formal mistakes:
        if no_formal_mistakes(name, name_error_slot,
                              phone, phone_error_slot,
                              from_datetime, to_datetime, time_error_slot):
            # Add booking to the table:
            state.tables[table_to_book_idx].add_booking(name, phone, from_datetime, to_datetime)
            table_to_book_idx = select_table(booking_slot, state.tables, key=1) # to refresh the selectbox of tables
    
    # Booking management section:                  
    st.header('Booking Management')
    print_table_statistics(state.tables, include_delete_button=True)
    
