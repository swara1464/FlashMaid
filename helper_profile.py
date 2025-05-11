import streamlit as st
from utils.firestore_ops import get_helper_by_id, update_helper_data
from utils.auth import check_authenticate

# Authenticate user and retrieve helperID
user = check_authenticate()
helper_id = user['uid'] if user and user['role'] == 'helper' else None

if helper_id:
    st.title("Helper Profile")

    # Fetch helper data
    helper_data = get_helper_by_id(helper_id)

    if helper_data:
        # Title bar with photo, name, and contact info
        st.subheader("Profile Overview")
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Placeholder for profile photo
            st.image("path/to/photo.jpg", width=150, caption="Helper Photo")  # Change to dynamic photo path if available

        with col2:
            st.write(f"**Name**: {helper_data['name']}")
            st.write(f"**Contact Info**: {helper_data['contactInfo']}")
        
        # Detailed profile information
        with st.form(key='profile_form'):
            st.subheader("Detailed Profile Information")
            gender = st.selectbox("Gender", options=["Male", "Female"], index=["Male", "Female"].index(helper_data['gender']))
            age = st.number_input("Age", min_value=18, value=helper_data['age'])

            st.subheader("Skills")
            current_skills = st.text_area("Skills", value="\n".join(helper_data['skills']))

            st.subheader("Allotment Schedule")
            allotment = helper_data.get('allotment', {})
            for time, details in allotment.items():
                st.text(f"Time: {time} - Task: {details['task']} (Household: {details['householdID']})")

            submit_button = st.form_submit_button("Update Profile")

            # Handle update
            if submit_button:
                updated_data = {
                    "gender": gender,
                    "age": age,
                    "skills": current_skills.split('\n')
                }
                update_helper_data(helper_id, updated_data)
                st.success("Profile updated successfully")
    else:
        st.error("Unable to fetch profile. Please try again later.")
else:
    st.error("You must be logged in as a helper to view this page.")