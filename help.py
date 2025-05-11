import streamlit as st
from utils.auth import check_authenticate

user = check_authenticate()
household_id = user['uid'] if user and user['role'] == 'household' else None

if household_id:
    st.title("Help / Complaint Form")
    with st.form(key='help_form'):
        st.subheader("Complaint Details")
        helper_id = st.text_input("Helper ID (if applicable)")
        issue_description = st.text_area("Describe your issue")
        submit_button = st.form_submit_button("Submit Complaint")
        if submit_button:
            complaint_data = {"householdID": household_id, "helperID": helper_id, "issueDescription": issue_description}
            # Implement Firestore complaint submission logic.
            st.success("Complaint submitted successfully.")
else:
    st.error("Access restricted to households.")