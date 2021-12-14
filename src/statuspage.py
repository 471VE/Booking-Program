import streamlit as st
from .helpers import print_table_statistics

def status_page(state):
    """
    Creates 'Status' page.
    """
    st.title('Status')
    print_table_statistics(state.tables, include_delete_button=False)        
    st.write(f'Number of currently free tables - {sum(1 for table in state.tables if table.is_free())}')
    st.write(f'Number of currently free seats - {sum(table.number_of_seats for table in state.tables if table.is_free())}')