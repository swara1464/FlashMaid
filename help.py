import streamlit as st
from utils.auth import check_authenticate

# Authenticate user and retrieve helperID
user = check_authenticate()
helper_id = user['uid'] if user and user['role'] == 'helper' else None

if helper_id:
    st.title("Help / Complaint Form")

    with st.form(key='help_form'):
        st.subheader("Complaint Details")
        household_id = st.text_input("Household ID (if applicable)")
        issue_description = st.text_area("Describe your issue")

        submit_button = st.form_submit_button("Submit Complaint")

        # Handle complaint submission
        if submit_button:
            complaint_data = {
                "helperID": helper_id,
                "householdID": household_id,
                "issueDescription": issue_description
            }
            # Add complaintData to Firestore complaints collection
            # Implement Firestore adding logic here...
            st.success("Complaint submitted successfully")
else:
    st.error("You must be logged in as a helper to view this page.")