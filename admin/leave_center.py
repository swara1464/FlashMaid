import streamlit as st
from utils.firestore_ops import get_leave_applications_all
from utils.auth import check_authenticate

user = check_authenticate()
if user and user['role'] == 'admin':
    st.title("Leave Applications Center")

    leave_applications = get_leave_applications_all()
    
    if leave_applications:
        for leave in leave_applications:
            st.write(f"Helper: {leave['helperName']} - Type: {leave['leaveType']}")
            st.write(f"Dates: {leave['leaveStartDate']} to {leave['leaveEndDate']}")
            st.button(f"Resolve Leave {leave['leaveID']}", key=leave['leaveID'])
            
else:
    st.error("Access restricted to admins.")
