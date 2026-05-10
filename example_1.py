import firebase_admin
from firebase_admin import credentials, db

# 1. Setup credentials using the file you just placed
cred = credentials.Certificate("service_account.json")

# 2. Initialize the app with your specific Database URL
# Note: If your RTDB is not in the US, the URL might end in something like .europe-west1.firebasedatabase.app
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iot-query-default-rtdb.firebaseio.com/'
})


def run_viewer_query():
    print("--- Example 1: RTDB Viewer Lookup ---")

    # The path for a specific sensor, just like in your presentation
    ref = db.reference("bySensor/temp1/logs")

    try:
        # Querying the logs between these two timestamps
        results = ref.order_by_child("timestamp") \
            .start_at(1708941000000) \
            .end_at(1708946000000) \
            .get()

        if not results:
            print("No data found for this time range. Check your database data.")
            return

        print("Success! Here are the logs:")
        for log_id, data in results.items():
            print(f"Log: {log_id} | Val: {data.get('value')} | Time: {data.get('timestamp')}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    run_viewer_query()