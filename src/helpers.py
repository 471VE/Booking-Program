import streamlit as st

def select_table(slot, tables, key=0):
    """
    Creates selectbox for choosing a Table to modify.
    """
    return slot.selectbox('Select table:', options=list(range(len(tables))), format_func=lambda x: f'{str(tables[x])}', key=key)

def print_table_statistics(tables: list, include_delete_button: bool):
    """Prints table statistics for 'Booking' and 'Status' page.

    Args:
        tables (list): list of Tables to process.
        include_delete_button (bool): An option on whether to have a 'Delete Booking' to modify bookings.
    """
    st.markdown('---')    
    
    # Determining the number of columns (depends on whether the buttons would be included or not):
    number_of_columns = 8 + int(include_delete_button)    
    columns = st.columns(number_of_columns)
    
    # Printing column names:
    column_names = ['Table Name','Seats Number','Current Status','Name', 'Phone','Booking Date','Starting Time','Ending Time']
    for column, column_name in zip(columns[:8], column_names):
        column.markdown(f'##### {column_name}')
    
    st.markdown('---')
    for i in range(len(tables)):
        # To make sure that there is at least one line in the statistics for every existing table:
        columns = st.columns(number_of_columns)    
        
        (table_column, seats_column, status_column,
        customer_name, customer_phone, booking_date,
        from_column, to_column) = columns[:8]  
              
        if include_delete_button:
            button_column = columns[8]
        
        # General table information:
        table_column.write(tables[i].name)
        seats_column.write(f'{tables[i].number_of_seats}')
        status_column.markdown(f'###### {tables[i].status}')

        booking_to_delete_idx = 'None'
        for j in range(len(tables[i].bookings)):
            if j > 0:
                # Creating a new line for every booking:
                columns = st.columns(number_of_columns)    
        
                (_, _, _,
                customer_name, customer_phone, booking_date,
                from_column, to_column) = columns[:8]  
                    
                if include_delete_button:
                    button_column = columns[8]

            # Shows information about every booking:
            customer_name.markdown(tables[i].bookings[j].name)
            customer_phone.text(tables[i].bookings[j].phone)
            booking_date.write(tables[i].bookings[j].from_datetime.strftime("%Y/%m/%d"))
            from_column.write(tables[i].bookings[j].from_datetime.strftime("%H:%M"))
            to_column.write(tables[i].bookings[j].to_datetime.strftime("%H:%M"))

            # Saving which booking to delete:
            if include_delete_button:
                if button_column.button('Delete booking', key=f'{i}th table, {j}th booking'):
                    booking_to_delete_idx = j 
        
        # Deleteing booking:     
        if include_delete_button:
            if booking_to_delete_idx != 'None':
                tables[i].delete_booking(booking_to_delete_idx)
                st.experimental_rerun() # to refresh the page
            
        st.markdown('---')
        
        
def no_formal_mistakes(name, name_error_slot,
                        phone, phone_error_slot,
                        from_datetime, to_datetime, time_error_slot):
    """
    Checks if there are no formal mistakes and displays error messages if they are present.

    Returns:
        bool: 'True' if there are no mistakes and 'False' otherwise.
    """
    result = True
    if not name:
        name_error_slot.error('Cannot book a table without name.')
        result = False
    if not phone:
        phone_error_slot.error('Cannot book a table without phone number.')
        result = False
    if from_datetime > to_datetime:
        time_error_slot.error('Starting time is later than the ending time. Check the booking form.')
        result = False
    elif from_datetime == to_datetime:
        time_error_slot.error('The booking time must be bigger than zero minutes. Please specify correct starting and ending times.')
        result = False
    return result