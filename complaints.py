import streamlit as st
from utils.firestore_ops import get_all_complaints
from utils.auth import check_authenticate

user = check_authenticate()
if user and user['role'] == 'admin':
    st.title("Manage Complaints")

    complaints = get_all_complaints()
    
    if complaints:
        for complaint in complaints:
            st.write(f"Household ID: {complaint['householdID']}")
            st.write(f"Helper ID: {complaint.get('helperID', 'N/A')}")
            st.write(f"Issue: {complaint['issueDescription']}")
            st.button(f"Resolve Issue {complaint['issueDescription']}", key=complaint['id'])
            
            # Implement resolve functionality here
    else:
        st.success("No Complaints reported.")

else:
    st.error("Access restricted to admins.")