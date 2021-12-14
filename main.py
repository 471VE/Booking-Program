import streamlit as st
from src.table import Table
from src.bookingpage import booking_page
from src.tablespage import tables_page
from src.statuspage import status_page


if __name__ == "__main__":
    st.set_page_config(layout="wide") # so that all columns in 'Booking' and 'Status' pages would fit

    # Putting in default tables:
    if 'tables' not in st.session_state:
        st.session_state.tables = [Table('Test table 1', 4), Table('Test table 2', 6)]

    # Declaring three pages with different information:
    page = st.sidebar.radio("Page",["Booking","Tables","Status"])

    # Implementing these pages:
    if page == "Booking":    
        booking_page(st.session_state)      
    elif page == "Tables":
        tables_page(st.session_state)
    elif page == "Status":    
        status_page(st.session_state)