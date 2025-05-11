import streamlit as st
from utils.firestore_ops import get_all_helpers, update_helper_data
from utils.auth import check_authenticate

def edit_helper(helper):
    """Render form for editing helper details."""
    with st.expander(f"Edit {helper['name']}"):
        helper['name'] = st.text_input("Name", value=helper['name'])
        helper['contactInfo'] = st.text_input("Contact Info", value=helper['contactInfo'])
        helper['gender'] = st.selectbox("Gender", options=["Male", "Female"], index=["Male", "Female"].index(helper['gender']))
        helper['age'] = st.number_input("Age", min_value=18, value=helper['age'])

        skills_text = st.text_area("Skills", value="\n".join(helper['skills']))
        helper['skills'] = skills_text.split('\n') if skills_text else []

        if st.button(f"Save Changes for {helper['name']}"):
            update_helper_data(helper['helperID'], helper)
            st.success(f"Updated {helper['name']} successfully!")

user = check_authenticate()

if user and user['role'] == 'admin':
    st.title("Manage Helpers")

    helpers = get_all_helpers()
    
    for helper in helpers:
        st.subheader(f"Helper: {helper['name']}")
        st.write(f"Contact: {helper['contactInfo']}")
        st.write(f"Gender: {helper['gender']}, Age: {helper['age']}")
        st.write(f"Skills: {', '.join(helper['skills'])}")

        edit_helper(helper)

else:
    st.error("Access restricted to admins.")