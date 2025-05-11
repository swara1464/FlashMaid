import streamlit as st
from utils.firestore_ops import get_dashboard_stats
from utils.auth import check_authenticate

user = check_authenticate()
if user and user['role'] == 'admin':
    st.title("Admin Dashboard")

    stats = get_dashboard_stats()
    st.metric("Total Helpers", stats.get('total_helpers', 0))
    st.metric("Total Households", stats.get('total_households', 0))
    st.metric("Pending Leaves", stats.get('pending_leaves', 0))
    st.metric("Pending Quits", stats.get('pending_quits', 0))
    st.metric("Reported Complaints", stats.get('reported_complaints', 0))
        
else:
    st.error("Access restricted to admins.")
