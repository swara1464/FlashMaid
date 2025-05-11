import streamlit as st
from utils.firestore_ops import get_all_households, update_household_data
from utils.auth import check_authenticate

def edit_household(household):
    """Render form for editing household details."""
    with st.expander(f"Edit {household['ownerName']}"):
        household['ownerName'] = st.text_input("Owner Name", value=household['ownerName'])
        household['contactInfo'] = st.text_input("Contact Info", value=household['contactInfo'])

        tasks_text = st.text_area("Tasks", value="\n".join(household['tasks']))
        household['tasks'] = tasks_text.split('\n') if tasks_text else []

        current_helpers_text = st.text_area("Current Helpers", value="\n".join(household['currentHelpers']))
        household['currentHelpers'] = current_helpers_text.split('\n') if current_helpers_text else []

        if st.button(f"Save Changes for {household['ownerName']}"):
            update_household_data(household['householdID'], household)
            st.success(f"Updated {household['ownerName']} successfully!")

user = check_authenticate()

if user and user['role'] == 'admin':
    st.title("Manage Households")

    households = get_all_households()
    
    for household in households:
        st.subheader(f"Household: {household['ownerName']}")
        st.write(f"Contact: {household['contactInfo']}")
        st.write(f"Tasks: {', '.join(household['tasks'])}")

        edit_household(household)

else:
    st.error("Access restricted to admins.")