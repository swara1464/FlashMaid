import json
import os
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.exceptions import GoogleCloudError

# Paths to local files
CONFIG_PATH = 'firebase_config.json'
DATA_FILES = {
    'helpers': ('helpers.json', 'helperID'),
    'households': ('households.json', 'householdID'),
    'leaveApplications': ('leaveApplications.json', 'leaveID'),
    'quitApplications': ('quitApplications.json', 'quitID')
}

def initialize_firebase():
    try:
        cred = credentials.Certificate(CONFIG_PATH)
        firebase_admin.initialize_app(cred)
        print("✅ Firebase initialized successfully.")
        return firestore.client()
    except Exception as e:
        print(f"❌ Error initializing Firebase: {e}")
        exit(1)

def load_json_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return []
    except json.JSONDecodeError:
        print(f"❌ JSON decoding error in file: {filepath}")
        return []

def upload_data(db, collection_name, data, id_key):
    print(f"\n🚀 Uploading data to '{collection_name}' collection...")
    success_count = 0
    for record in data:
        try:
            doc_id = record.get(id_key)
            if not doc_id:
                print(f"⚠️ Skipping record with missing ID field '{id_key}': {record}")
                continue
            db.collection(collection_name).document(doc_id).set(record)
            success_count += 1
        except GoogleCloudError as gce:
            print(f"❌ Firestore error uploading document {doc_id}: {gce}")
        except Exception as e:
            print(f"❌ Unexpected error for document {doc_id}: {e}")
    print(f"✅ Uploaded {success_count}/{len(data)} records to '{collection_name}'.")

def main():
    db = initialize_firebase()
    for collection, (file_name, id_key) in DATA_FILES.items():
        data = load_json_data(file_name)
        upload_data(db, collection, data, id_key)

if __name__ == '__main__':
    main()
