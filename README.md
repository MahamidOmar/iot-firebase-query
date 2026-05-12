# IoT Firebase Database Testing Suite

This project contains a suite of Python scripts designed to test querying capabilities and data structuring paradigms across Firebase Realtime Database (RTDB) and Cloud Firestore. It serves as a proof-of-concept for an IoT backend system.

## Included Files
* **`populate_db.py`**: A setup script that automatically seeds your Firebase project with the necessary mock data and anomalies required for the tests.
* **`example_1.py`**: Demonstrates a targeted range query on a specific RTDB path (Viewer Lookup).
* **`example_2.py`**: Demonstrates RTDB Denormalization to achieve a global timeline query (Admin Timeline).
* **`example_3.py`**: Showcases Firestore compound queries and the necessity of Composite Indexes (Technician Anomalies).
* **`example_4.py`**: Highlights a workaround for Firestore's lack of a native `GROUP BY` function using rollup documents (Admin Dashboard).

## Prerequisites
To run these scripts, you will need Python 3.x and the Firebase Admin SDK installed:
```bash
pip install firebase-admin
