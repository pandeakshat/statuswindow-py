import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import numpy as np
import pandas as pd
def main():
    st.set_page_config(layout="wide")
    st.title("Status Window")

    
    # _LOREM_IPSUM = """
    # Lorem ipsum dolor sit amet, **consectetur adipiscing** elit, sed do eiusmod tempor
    # incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
    # nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    # """


    # def stream_data():
    #     for word in _LOREM_IPSUM.split(" "):
    #         yield word + " "
    #         time.sleep(0.1)

    #     yield pd.DataFrame(
    #         np.random.randn(5, 10),
    #         columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
    #     )

    #     for word in _LOREM_IPSUM.split(" "):
    #         yield word + " "
    #         time.sleep(0.1)


    # if st.button("Stream data"):
    #     st.write_stream(stream_data)

    st.divider()
    strength, agility, intelligence, luck, charisma = st.columns(5)
    with strength:
        st.metric(label="Strength", value="10", delta="1", delta_color="inverse")
    with agility:
        st.metric(label="Agility", value="10", delta="1", delta_color="inverse")
    with intelligence:
        st.metric(label="Intelligence", value="10", delta="1", delta_color="inverse")
    with luck:
        st.metric(label="Luck", value="10", delta="1", delta_color="inverse")
    with charisma:
        st.metric(label="Charisma", value="10", delta="1", delta_color="inverse")
    
    st.divider()


    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict({
        "type": st.secrets["connections"]["gsheets"]["type"],
        "project_id": st.secrets["connections"]["gsheets"]["project_id"],
        "private_key_id": st.secrets["connections"]["gsheets"]["private_key_id"],
        "private_key": st.secrets["connections"]["gsheets"]["private_key"],
        "client_email": st.secrets["connections"]["gsheets"]["client_email"],
        "client_id": st.secrets["connections"]["gsheets"]["client_id"],
        "auth_uri": st.secrets["connections"]["gsheets"]["auth_uri"],
        "token_uri": st.secrets["connections"]["gsheets"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["connections"]["gsheets"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["connections"]["gsheets"]["client_x509_cert_url"]
    }, scope)

    # Authorize the client
    client = gspread.authorize(credentials)

    # Extract the spreadsheet ID from the secrets
    spreadsheet_url = st.secrets["connections"]["gsheets"]["spreadsheet"]
    spreadsheet_id = spreadsheet_url.split("/d/")[1].split("/")[0]

    # Open the spreadsheet by ID
    spreadsheet = client.open_by_key(spreadsheet_id)

    # List of sheet names to display
    sheet_names = ['Main', 'Foundation', 'Attributes', 'Story', 'Inventory', 'Log']  # Replace with your actual sheet names

    st.write("Data")
    # Loop through each sheet name and display its data
    tabs = st.tabs(sheet_names)

    # Loop through each sheet name and display its data in a tab
    for i, sheet_name in enumerate(sheet_names):
        with tabs[i]:
            try:
                # Get the sheet by name
                worksheet = spreadsheet.worksheet(sheet_name)
                
                # Convert the worksheet data to a DataFrame
                data = worksheet.get_all_values()
                df = pd.DataFrame(data[1:], columns=data[0])  # Assuming the first row is the header

                # Display the data in Streamlit
                st.write(f"### {sheet_name}")
                st.dataframe(df)
            except gspread.exceptions.WorksheetNotFound:
                st.write(f"Sheet {sheet_name} not found in the spreadsheet.")



    tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

    with tab1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
    with tab2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
    with tab3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

    @st.dialog("Cast your vote")
    def vote(item):
        st.write(f"Why is {item} your favorite?")
        reason = st.text_input("Because...")
        if st.button("Submit"):
            st.session_state.vote = {"item": item, "reason": reason}
            st.rerun()

    if "vote" not in st.session_state:
        st.write("Vote for your favorite")
        if st.button("A"):
            vote("A")
        if st.button("B"):
            vote("B")
    else:
        f"You voted for {st.session_state.vote['item']} because {st.session_state.vote['reason']}"
    with st.popover("Open popover"):
        st.markdown("Hello World 👋")
        name = st.text_input("What's your name?")

    st.write("Your name:", name)





if __name__ == "__main__":
    main()


    # Set wide format by default
