import streamlit as st
from .table import Table
from .helpers import select_table

def tables_page(state):  
    """
    Creates 'Tables' page.
    """  
    # General layout:
    st.title('Tables')
    slot1 = st.empty()
    slot2 = st.empty()
    slot3 = st.empty()
    table_name = st.text_input('Name of the table')
    number_of_seats = st.number_input('Number of seats', min_value=1, value=4)

    # Adding a table to the database:
    if st.button('Add'):
        if table_name not in [table.name for table in state.tables]:
            state.tables.append(Table(table_name, number_of_seats))
            st.info(f"The table '{table_name}' with {number_of_seats} seats was created in the database.")
        else:
            st.error('A table with this name already exists in the database.')
    
    # Selectbox for tables:
    table_to_edit_idx = select_table(slot1, state.tables)
    
    take_button, release_button, _, delete_button = slot2.columns(4)

    # Implementing 'Take the table' button:
    if take_button.button('Take the table'):
        try:
            if state.tables[table_to_edit_idx].is_free():
                state.tables[table_to_edit_idx].take()
                slot3.success('This table is now taken.')
                table_to_edit_idx = select_table(slot1, state.tables) # refreshing selectbox
            else:
                # Cannot take the same table twice:
                slot3.error('This table is already taken.')
        except:
            slot3.error('There are no tables to take.')

    # Implementing 'Release the table' button:
    if release_button.button('Release the table'):
        try:
            if state.tables[table_to_edit_idx].is_taken():
                state.tables[table_to_edit_idx].release()
                slot3.success('This table is now free.')
                table_to_edit_idx = select_table(slot1, state.tables) # refreshing selectbox
            else:
                # Warning in case they wanted to release another table:
                slot3.warning('This table was already free.')
        except:
            slot3.error('There are no table to release.')

    # Implementing 'Delete the table' button:
    if delete_button.button('Delete the table'):
        
        try:
            name_tmp = state.tables[table_to_edit_idx].name
            del state.tables[table_to_edit_idx]
            slot3.info(f"The table '{name_tmp}' was deleted.")
            table_to_edit_idx = select_table(slot1, state.tables) # refreshing selectbox
        except:
            slot3.error(f'There are no tables to delete.')