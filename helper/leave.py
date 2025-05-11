import streamlit as st
from utils.firestore_ops import get_helper_by_id, update_helper_data
from utils.auth import check_authenticate

# Authenticate user and retrieve helperID
user = check_authenticate()
helper_id = user['uid'] if user and user['role'] == 'helper' else None

if helper_id:
    st.title("Leave Application")

    # Fetch helper data
    helper_data = get_helper_by_id(helper_id)

    if helper_data:
        with st.form(key='leave_form'):
            st.subheader("Leave Details")
            leave_type = st.selectbox("Leave Type", options=["slot", "partial", "full_day", "multiple_day"])
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")

            if leave_type in ["slot", "partial"]:
                start_time = st.time_input("Start Time")
                end_time = st.time_input("End Time")
            else:
                start_time = end_time = None

            tasks_affected = st.text_area("Tasks Affected", value="")
            affected_households = st.text_area("Affected Households", value="")

            submit_button = st.form_submit_button("Submit Leave Application")

            # Handle leave submission
            if submit_button:
                leave_data = {
                    "helperID": helper_id,
                    "helperName": helper_data['name'],
                    "leaveType": leave_type,
                    "leaveStartDate": str(start_date),
                    "leaveEndDate": str(end_date),
                    "leaveStartTime": str(start_time) if start_time else None,
                    "leaveEndTime": str(end_time) if end_time else None,
                    "affectedHouseholds": affected_households.split('\n'),
                    "tasksAffected": tasks_affected
                }
                # Add leaveData to Firestore leaveApplications
                # Implement Firestore adding logic here...
                st.success("Leave application submitted successfully")
    else:
        st.error("Unable to fetch profile. Please try again later.")
else:
    st.error("You must be logged in as a helper to view this page.")
