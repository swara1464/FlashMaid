import firebase_admin
from firebase_admin import firestore

# Ensure Firebase admin SDK is initialized properly elsewhere
db = firestore.client()

def suggest_replacements(current_task, task_time):
    """Suggests available helpers for a given task and time."""
    all_helpers = get_available_helpers()
    matching_helpers = [
        helper for helper in all_helpers
        if current_task in helper['skills'] and task_time not in helper.get('allotment', {}).keys()
    ]
    return matching_helpers

def get_available_helpers():
    """Retrieve all helpers available for matching, excluding those on leave or quit."""
    try:
        # Fetch all helpers
        all_helpers_ref = db.collection('helpers')
        all_helpers_docs = all_helpers_ref.get()

        # Fetch leave and quit applications to determine excluded helpers
        leave_docs = db.collection('leaveApplications').get()
        quit_docs = db.collection('quitApplications').get()

        leave_helper_ids = {doc.get('helperID') for doc in leave_docs}
        quit_helper_ids = {doc.get('helperID') for doc in quit_docs}

        # Determine active helpers by excluding those who are on leave or quit
        active_helpers = []
        for helper_doc in all_helpers_docs:
            helper_data = helper_doc.to_dict()
            helper_id = helper_data.get('helperID')

            # Include helper if not in leave or quit lists
            if helper_id not in leave_helper_ids and helper_id not in quit_helper_ids:
                active_helpers.append(helper_data)

        return active_helpers

    except Exception as e:
        print(f"Error fetching helpers: {str(e)}")
        return []