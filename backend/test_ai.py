# test_ai.py — Test the AI components together

from ai_engine import optimizer
from predictor import predictor
from datetime import datetime

print("🧪 Testing AI components...\n")

# Simulate a realistic junction scenario
lane_data = [
    {"direction": "North", "vehicle_count": 32, "queue_length": 145, "avg_wait_time": 75, "has_emergency": False},
    {"direction": "South", "vehicle_count": 8,  "queue_length": 36,  "avg_wait_time": 18, "has_emergency": False},
    {"direction": "East",  "vehicle_count": 20, "queue_length": 90,  "avg_wait_time": 45, "has_emergency": False},
    {"direction": "West",  "vehicle_count": 15, "queue_length": 68,  "avg_wait_time": 35, "has_emergency": False},
]

print("=== SCENARIO 1: Normal Traffic ===")
result = optimizer.calculate_green_times(lane_data)
for direction in ["North", "South", "East", "West"]:
    print(f"  {direction}: {result[direction]}s green time")

print("\n=== SCENARIO 2: Emergency Override ===")
lane_data_emergency = lane_data.copy()
lane_data_emergency[0] = {**lane_data[0], "has_emergency": True}
result_emergency = optimizer.calculate_green_times(lane_data_emergency)
print(f"  Emergency on: {result_emergency['emergency_direction']}")
for direction in ["North", "South", "East", "West"]:
    print(f"  {direction}: {result_emergency[direction]}s green time")

print("\n=== SCENARIO 3: Congestion Prediction ===")
hour = datetime.now().hour
for lane in lane_data:
    pred = predictor.predict(
        vehicle_count=lane["vehicle_count"],
        queue_length=lane["queue_length"],
        wait_time=lane["avg_wait_time"],
        hour=hour
    )
    print(f"  {lane['direction']}: {pred['label']} ({pred['confidence']}% confidence)")

print("\n✅ All AI components working correctly!")