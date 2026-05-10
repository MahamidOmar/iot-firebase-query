import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter  # <-- We import the new filter method

# 1. Setup credentials
cred = credentials.Certificate("service_account.json")

# 2. Initialize the app
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()


def run_technician_query():
    print("--- Example 3: Firestore Technician Query ---")

    start_time = 1708941600000
    end_time = 1708943000000

    try:
        # Using the newer FieldFilter syntax to avoid the red UserWarnings
        query = db.collection("sensor_readings") \
            .where(filter=FieldFilter("siteId", "==", "S1")) \
            .where(filter=FieldFilter("category", "==", "temperature")) \
            .where(filter=FieldFilter("temp", ">=", 80.0)) \
            .where(filter=FieldFilter("timestamp", ">=", start_time)) \
            .where(filter=FieldFilter("timestamp", "<=", end_time))

        docs = query.stream()

        found = False
        print("Executing Query...\n")
        for doc in docs:
            found = True
            data = doc.to_dict()
            print(f"Sensor: {data.get('sensorId')}")
            print(f"Temp: {data.get('temp')}")
            print(f"Time: {data.get('timestamp')}")
            print("-------------------")

        if not found:
            print("Query succeeded, but no documents matched.")

    except Exception as e:
        print(f"QUERY FAILED!")
        print(f"Error: {e}")


if __name__ == "__main__":
    run_technician_query()