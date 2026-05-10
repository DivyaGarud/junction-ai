# # database.py
# # This file connects our Flask app to MongoDB

# from pymongo import MongoClient
# from datetime import datetime
# import os

# # Connection string — MongoDB running locally
# MONGO_URI = "mongodb://localhost:27017/"
# DATABASE_NAME = "junction_ai"

# # Create the connection
# client = MongoClient(MONGO_URI)
# db = client[DATABASE_NAME]

# # Collections (like tables in a regular database)
# junction_collection = db["junction_data"]       # Stores real-time traffic data
# analytics_collection = db["analytics"]          # Stores historical analytics
# emergency_collection = db["emergency_events"]   # Stores emergency vehicle events

# def save_junction_data(data):
#     """Save one snapshot of junction data to MongoDB"""
#     data["timestamp"] = datetime.now()
#     result = junction_collection.insert_one(data)
#     return str(result.inserted_id)

# def get_recent_data(limit=20):
#     """Get the most recent traffic snapshots"""
#     records = list(
#         junction_collection.find({}, {"_id": 0})
#         .sort("timestamp", -1)
#         .limit(limit)
#     )
#     return records

# def save_emergency_event(direction, vehicle_type):
#     """Log an emergency vehicle event"""
#     event = {
#         "direction": direction,
#         "vehicle_type": vehicle_type,
#         "timestamp": datetime.now(),
#         "action": "PRIORITY_GRANTED"
#     }
#     emergency_collection.insert_one(event)

# def get_analytics_summary():
#     """Calculate summary stats from stored data"""
#     pipeline = [
#         {
#             "$group": {
#                 "_id": None,
#                 "avg_vehicles": {"$avg": "$total_vehicles"},
#                 "max_vehicles": {"$max": "$total_vehicles"},
#                 "total_records": {"$sum": 1}
#             }
#         }
#     ]
#     result = list(junction_collection.aggregate(pipeline))
#     if result:
#         return result[0]
#     return {"avg_vehicles": 0, "max_vehicles": 0, "total_records": 0}

# print("✅ Database module loaded successfully")




# database.py
# This file connects our Flask app to MongoDB

from pymongo import MongoClient
from datetime import datetime
import os

# ==============================
# MongoDB Connection (IMPORTANT)
# ==============================
MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb://localhost:27017/"
)

DATABASE_NAME = "junction_ai"

# Create connection
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

# ==============================
# Collections (like tables)
# ==============================
junction_collection = db["junction_data"]
analytics_collection = db["analytics"]
emergency_collection = db["emergency_events"]

# ==============================
# Functions
# ==============================

def save_junction_data(data):
    """Save one snapshot of junction data to MongoDB"""
    data["timestamp"] = datetime.now()
    result = junction_collection.insert_one(data)
    return str(result.inserted_id)

def get_recent_data(limit=20):
    """Get most recent traffic snapshots"""
    records = list(
        junction_collection.find({}, {"_id": 0})
        .sort("timestamp", -1)
        .limit(limit)
    )
    return records

def save_emergency_event(direction, vehicle_type):
    """Log emergency vehicle event"""
    event = {
        "direction": direction,
        "vehicle_type": vehicle_type,
        "timestamp": datetime.now(),
        "action": "PRIORITY_GRANTED"
    }
    emergency_collection.insert_one(event)

def get_analytics_summary():
    """Calculate summary stats"""
    pipeline = [
        {
            "$group": {
                "_id": None,
                "avg_vehicles": {"$avg": "$total_vehicles"},
                "max_vehicles": {"$max": "$total_vehicles"},
                "total_records": {"$sum": 1}
            }
        }
    ]

    result = list(junction_collection.aggregate(pipeline))

    if result:
        return result[0]

    return {
        "avg_vehicles": 0,
        "max_vehicles": 0,
        "total_records": 0
    }

print("✅ Database module loaded successfully")