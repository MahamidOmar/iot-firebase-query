import firebase_admin
from firebase_admin import credentials, db, firestore

# 1. Setup credentials (Students will use their own key)
cred = credentials.Certificate("service_account.json")

# Initialize the app
# Instructors/Students MUST replace this URL with their own RTDB URL
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://your-project-id-default-rtdb.firebaseio.com/'
    })

firestore_db = firestore.client()


def populate_rtdb():
    print("Populating RTDB with sample logs and timeline data...")

    # 1. Data for Example 1 (Viewer Lookup - temp1 logs)
    ref_viewer = db.reference("bySensor/temp1/logs")
    ref_viewer.set({
        "log_id_001": {"value": 24.5, "timestamp": 1708941600000},
        "log_id_002": {"value": 25.1, "timestamp": 1708945200000},
        "log_id_003": {"value": 22.0, "timestamp": 1708948000000}  # Outside the query range
    })

    # 2. Data for Example 2 (Admin Timeline - Denormalized)
    ref_timeline = db.reference("byTime/temperature")
    ref_timeline.set({
        "1708941600000": {
            "log1": {"sensorId": "temp1", "value": 24.5},
            "log2": {"sensorId": "temp2", "value": 22.0}
        },
        "1708945200000": {
            "log3": {"sensorId": "temp1", "value": 25.1}
        }
    })
    print("-> RTDB Population Complete.")


def populate_firestore():
    print("Populating Firestore with sensor readings and hourly stats...")

    # 3. Data for Example 3 (Technician - Complex Query & Anomalies)
    readings_ref = firestore_db.collection("sensor_readings")

    # Intentional anomalies to trigger the >= 80 filter
    readings_ref.document("doc1").set({
        "siteId": "S1", "category": "temperature", "temp": 85.0, "timestamp": 1708941900000, "sensorId": "temp2"
    })
    readings_ref.document("doc2").set({
        "siteId": "S1", "category": "temperature", "temp": 88.0, "timestamp": 1708942500000, "sensorId": "temp2"
    })
    # Normal reading (should be ignored by the query)
    readings_ref.document("doc3").set({
        "siteId": "S1", "category": "temperature", "temp": 70.0, "timestamp": 1708942000000, "sensorId": "temp1"
    })

    # 4. Data for Example 4 (Admin Dashboard Rollups)
    stats_ref = firestore_db.collection("hourly_stats")
    stats_ref.document("stat1").set({"hourKey": "2026022814", "avg": 24.5, "count": 120})
    stats_ref.document("stat2").set({"hourKey": "2026022815", "avg": 26.2, "count": 115})
    stats_ref.document("stat3").set({"hourKey": "2026022816", "avg": 25.8, "count": 130})

    print("-> Firestore Population Complete.")


if __name__ == "__main__":
    try:
        populate_rtdb()
        populate_firestore()
        print("\nSuccess! The database has been seeded with test data.")
        print("You can now run examples 1 through 4.")
    except Exception as e:
        print(f"Error populating data: {e}")