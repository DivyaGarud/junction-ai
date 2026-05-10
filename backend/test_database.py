# test_database.py
from database import save_junction_data, get_recent_data

print("🧪 Testing MongoDB connection...")

# Try saving a record
test_data = {
    "total_vehicles": 25,
    "lanes": {
        "North": {"vehicle_count": 10},
        "South": {"vehicle_count": 15}
    }
}

record_id = save_junction_data(test_data)
print(f"✅ Saved record with ID: {record_id}")

# Try reading it back
recent = get_recent_data(limit=5)
print(f"✅ Read {len(recent)} records from database")
print("   Database is working correctly!")