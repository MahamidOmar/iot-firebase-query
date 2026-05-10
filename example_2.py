import firebase_admin
from firebase_admin import credentials, db

# 1. Setup credentials
cred = credentials.Certificate("service_account.json")

# 2. Initialize the app (Standalone script)
# We check if an app already exists to prevent errors if you ever run these together
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://iot-query-default-rtdb.firebaseio.com/'
    })


def run_admin_timeline_query():
    """
    Example 2: Admin Timeline (Denormalization).
    Scenario: Admin wants to see all sensors for a category in a time window.
    Path: byTime/temperature
    """
    print("--- Example 2: RTDB Admin Timeline (Denormalization) ---")

    # Target the denormalized path designed specifically for this query
    ref = db.reference("byTime/temperature")

    try:
        # In this structure, the Key itself is the timestamp.
        # Note: In your Kotlin code, these were queried as Strings!
        results = ref.order_by_key() \
            .start_at("1708941000000") \
            .end_at("1708946000000") \
            .get()

        if not results:
            print("No data found for this global timeline.")
            return

        print("Global Timeline Results:\n")

        # Parse the nested dictionary (Timestamp -> Logs -> Sensor Data)
        for time_key, time_node in results.items():
            print(f"Time: {time_key}")
            # Loop through the logs inside that specific timestamp
            for log_key, log_data in time_node.items():
                sensor_id = log_data.get('sensorId')
                val = log_data.get('value')
                print(f"  -> Sensor: {sensor_id} | Val: {val}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    run_admin_timeline_query()