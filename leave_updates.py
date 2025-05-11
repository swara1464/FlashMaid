import streamlit as st
from utils.firestore_ops import get_leave_applications
from utils.match_helpers import suggest_replacements
from utils.auth import check_authenticate

user = check_authenticate()
household_id = user['uid'] if user and user['role'] == 'household' else None

if household_id:
    st.title("Leave Updates")
    leave_applications = get_leave_applications(household_id)  # Adjust logic to fetch leave applications affecting household

    if leave_applications:
        st.subheader("Currently Affected Leaves")
        
        for leave in leave_applications:
            st.markdown(f"**Helper**: {leave['helperName']}, **Leave Type**: {leave['leaveType']}, **Dates**: {leave['leaveStartDate']} to {leave['leaveEndDate']}")
            tasks = leave.get('tasksAffected', {})
            
            for task_id, details in tasks.items():
                st.text(f"Task: {details['task']} during {details['slot']}")
                if st.button(f"View Replacement Options for Task {details['task']}"):
                    matching_helpers = suggest_replacements(details['task'], details['slot'])
                    
                    st.subheader("Available Helpers During Leave")
                    for helper in matching_helpers:
                        st.write(f"Helper: {helper['name']}, Skills: {', '.join(helper['skills'])}")
                        # No database change for temporary replacement during leave
    
    else:
        st.success("No leave applications currently affecting your household.")
else:
    st.error("Access restricted to households.")