import streamlit as st
from utils.firestore_ops import get_quit_applications_all
from utils.auth import check_authenticate

user = check_authenticate()
if user and user['role'] == 'admin':
    st.title("Quit Applications Center")

    quit_applications = get_quit_applications_all()
    
    if quit_applications:
        for quit_ in quit_applications:
            st.write(f"Helper: {quit_['helperName']} - Type: {quit_['quitType']}")
            st.write(f"Date: {quit_['quitDate']}")
            st.button(f"Resolve Quit {quit_['quitID']}", key=quit_['quitID'])
            
else:
    st.error("Access restricted to admins.")