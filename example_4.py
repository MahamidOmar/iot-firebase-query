import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter

# 1. Setup credentials
cred = credentials.Certificate("service_account.json")

# 2. Initialize the app
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()


def run_admin_rollup_query():
    """
    Example 4: Admin Dashboard Rollups.
    Scenario: Fetching hourly averages for the dashboard chart.
    Why: Bypasses Firestore's lack of a native GROUP BY function.
    """
    print("--- Example 4: Firestore Admin Rollups (The GROUP BY Workaround) ---")

    try:
        # We query the 'hourly_stats' collection using the hourKey
        # hourKey format: YYYYMMDDHH (e.g., 2026022814 is Feb 28, 2026 at 14:00)
        query = db.collection("hourly_stats") \
            .where(filter=FieldFilter("hourKey", ">=", "2026022814")) \
            .where(filter=FieldFilter("hourKey", "<=", "2026022816")) \
            .order_by("hourKey")

        docs = query.stream()

        found = False
        print("Success! Admin Dashboard Chart Data:\n")

        for doc in docs:
            found = True
            data = doc.to_dict()
            print(f"Hour Block: {data.get('hourKey')}")
            print(f"  -> Avg Temp: {data.get('avg')}")
            print(f"  -> Total Readings: {data.get('count')}")
            print("-------------------")

        if not found:
            print("No hourly stats found. Check your 'hourly_stats' collection data.")

    except Exception as e:
        print(f"Query Failed: {e}")


if __name__ == "__main__":
    run_admin_rollup_query()