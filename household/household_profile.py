import streamlit as st
from utils.firestore_ops import get_household_by_id, update_household_data
from utils.auth import check_authenticate

user = check_authenticate()
household_id = user['uid'] if user and user['role'] == 'household' else None

if household_id:
    st.title("Household Profile")
    household_data = get_household_by_id(household_id)

    if household_data:
        st.subheader("Household Overview")
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("path/to/photo.jpg", width=150, caption="Household Photo")
        with col2:
            st.write(f"**Owner Name**: {household_data['ownerName']}")
            st.write(f"**Contact Info**: {household_data['contactInfo']}")
        
        with st.form(key='household_form'):
            st.subheader("Tasks")
            current_tasks = st.text_area("Tasks", value="\n".join(household_data['tasks']))
            st.subheader("Current Helpers")
            current_helpers = st.text_area("Helpers", value="\n".join(household_data['currentHelpers']))
            st.subheader("Scheduled Tasks")
            scheduled_tasks = household_data.get('scheduledTasks', {})
            for time, details in scheduled_tasks.items():
                st.text(f"Time: {time} - Task: {details['task']} (Helper: {details['helperID']})")
            submit_button = st.form_submit_button("Update Profile")
            if submit_button:
                updated_data = {"tasks": current_tasks.split('\n'), "currentHelpers": current_helpers.split('\n')}
                update_household_data(household_id, updated_data)
                st.success("Profile updated successfully.")
    else:
        st.error("Unable to fetch profile.")
else:
    st.error("Access restricted to households.")
