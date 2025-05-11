import streamlit as st
from utils.firestore_ops import get_helper_by_id
from utils.auth import check_authenticate

# Authenticate user and retrieve helperID
user = check_authenticate()
helper_id = user['uid'] if user and user['role'] == 'helper' else None

if helper_id:
    st.title("Quit Application")

    # Fetch helper data
    helper_data = get_helper_by_id(helper_id)

    if helper_data:
        with st.form(key='quit_form'):
            st.subheader("Quit Details")
            quit_type = st.selectbox("Quit Type", options=["Full", "Partial", "Slot", "Household"])
            quit_date = st.date_input("Quit Date")

            if quit_type in ["Slot", "Partial"]:
                quit_time = st.time_input("Quit Time")
            else:
                quit_time = None

            affected_households = st.text_area("Affected Households", value="")

            submit_button = st.form_submit_button("Submit Quit Application")

            # Handle quit submission
            if submit_button:
                quit_data = {
                    "helperID": helper_id,
                    "helperName": helper_data['name'],
                    "quitType": quit_type,
                    "quitDate": str(quit_date),
                    "quitTime": str(quit_time) if quit_time else None,
                    "affectedHouseholds": affected_households.split('\n')
                }
                # Add quitData to Firestore quitApplications
                # Implement Firestore adding logic here...
                st.success("Quit application submitted successfully")
    else:
        st.error("Unable to fetch profile. Please try again later.")
else:
    st.error("You must be logged in as a helper to view this page.")