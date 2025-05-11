import streamlit as st
from utils.firestore_ops import get_quit_applications, update_helper_assignment
from utils.match_helpers import suggest_replacements
from utils.auth import check_authenticate

user = check_authenticate()
household_id = user['uid'] if user and user['role'] == 'household' else None

if household_id:
    st.title("Quit Updates")
    quit_applications = get_quit_applications(household_id)  # Adjust logic to fetch quit applications affecting household

    if quit_applications:
        st.subheader("Currently Affected Quits")
        
        for quit_ in quit_applications:
            st.markdown(f"**Helper**: {quit_['helperName']}, **Quit Type**: {quit_['quitType']}, **Date**: {quit_['quitDate']}")
            tasks = quit_.get('tasksAffected', {})
            
            for time, details in tasks.items():
                st.text(f"Task at {time}: {details['task']}")
                if st.button(f"View Replacement Options for Task {details['task']}"):
                    matching_helpers = suggest_replacements(details['task'], time)
                    
                    st.subheader("Available Helpers to Hire Permanently")
                    for helper in matching_helpers:
                        st.write(f"Helper: {helper['name']}, Skills: {', '.join(helper['skills'])}")
                        if st.button(f"Hire {helper['name']} Permanently for Task {details['task']}"):
                            # Trigger database update here
                            update_helper_assignment(household_id, details['task'], helper['helperID'])
                            st.success(f"Hired {helper['name']} successfully for {details['task']}!")
    
    else:
        st.success("No quit applications currently affecting your household.")
else:
    st.error("Access restricted to households.")
