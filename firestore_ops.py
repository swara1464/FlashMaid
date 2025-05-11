import firebase_admin
from firebase_admin import firestore

# Initialize Firestore
db = firestore.client()

def get_helper_by_id(helper_id):
    """ Retrieve helper document by helper_id. """
    try:
        doc_ref = db.collection('helpers').document(helper_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            print(f"Helper with ID {helper_id} not found.")
            return None
    except Exception as e:
        print(f"Error fetching helper: {str(e)}")
        return None

def get_household_by_id(household_id):
    """ Retrieve household document by household_id. """
    try:
        doc_ref = db.collection('households').document(household_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            print(f"Household with ID {household_id} not found.")
            return None
    except Exception as e:
        print(f"Error fetching household: {str(e)}")
        return None

def get_leave_applications(helper_id):
    """ Fetch leave applications for a specific helper. """
    try:
        docs = db.collection('leaveApplications').where('helperID', '==', helper_id).get()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        print(f"Error fetching leave applications: {str(e)}")
        return []

def get_quit_applications(helper_id):
    """ Fetch quit applications for a specific helper. """
    try:
        docs = db.collection('quitApplications').where('helperID', '==', helper_id).get()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        print(f"Error fetching quit applications: {str(e)}")
        return []

def update_helper_data(helper_id, updates):
    """ Update helper's data with a dictionary of updates. """
    try:
        doc_ref = db.collection('helpers').document(helper_id)
        doc_ref.update(updates)
        print(f"Helper {helper_id} updated successfully.")
    except Exception as e:
        print(f"Error updating helper: {str(e)}")

def update_household_data(household_id, updates):
    """ Update household's data with a dictionary of updates. """
    try:
        doc_ref = db.collection('households').document(household_id)
        doc_ref.update(updates)
        print(f"Household {household_id} updated successfully.")
    except Exception as e:
        print(f"Error updating household: {str(e)}")