import streamlit as st
from firebase_admin import auth, firestore
from firebase_admin.exceptions import FirebaseError

def get_user_role(uid):
    """Check Firestore to determine user role based on your existing collections"""
    db = firestore.client()
    
    # Check in helpers collection (using helperID field)
    helpers_ref = db.collection('helpers').where('helperID', '==', uid).limit(1)
    helper_docs = helpers_ref.stream()
    for doc in helper_docs:
        return 'helper', doc.to_dict()
    
    # Check in households collection (using householdID field)
    households_ref = db.collection('households').where('householdID', '==', uid).limit(1)
    household_docs = households_ref.stream()
    for doc in household_docs:
        return 'household', doc.to_dict()
    
    # Check in admins collection if you have one
    admins_ref = db.collection('admins').where('adminID', '==', uid).limit(1)
    admin_docs = admins_ref.stream()
    for doc in admin_docs:
        return 'admin', doc.to_dict()
    
    return None, None

def verify_token_and_set_session(token):
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        
        role, user_data = get_user_role(uid)
        if not role:
            st.error("User not found in any role collection")
            return False
            
        st.session_state["user"] = {
            "uid": uid,
            "role": role,
            "phone": decoded_token.get('phone_number'),
            **user_data  # Merge all user data from Firestore
        }
        return True
        
    except FirebaseError as e:
        st.error(f"Authentication failed: {e}")
        return False
