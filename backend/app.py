# app.py
# Main Flask server — the brain that connects everything
# from detector import detector
# import base64
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import threading
import time
import json
import random
from datetime import datetime
import cv2
import base64
import numpy as np
import os



# Import our custom modules
from database import (save_junction_data, get_recent_data, 
                      save_emergency_event, get_analytics_summary)
from ai_engine import optimizer
from predictor import predictor

# ============================================================
# APP SETUP
# ============================================================

app = Flask(__name__)
app.config["SECRET_KEY"] = "junction-ai-secret-2024"

# Allow React (running on port 5173) to talk to Flask (running on port 5000)
CORS(app, origins=["http://localhost:5173", "http://localhost:3000"])

# Socket.IO for real-time updates (pushes data to React without React asking)
# socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")
# ============================================================
# GLOBAL STATE (in-memory data for demo)
# ============================================================

# This holds the current state of the junction
junction_state = {
    "North": {"vehicle_count": 0, "queue_length": 0, "avg_wait_time": 0, "has_emergency": False},
    "South": {"vehicle_count": 0, "queue_length": 0, "avg_wait_time": 0, "has_emergency": False},
    "East":  {"vehicle_count": 0, "queue_length": 0, "avg_wait_time": 0, "has_emergency": False},
    "West":  {"vehicle_count": 0, "queue_length": 0, "avg_wait_time": 0, "has_emergency": False},
}

current_signal_times = {}
simulation_running = False

# ============================================================
# SIMULATION (generates fake data when no camera is available)
# ============================================================

def run_simulation():
    """
    Continuously generates realistic traffic data.
    Runs in a background thread so it doesn't block Flask.
    """
    global junction_state, current_signal_times, simulation_running
    
    import random
    
    simulation_running = True
    print("🚦 Traffic simulation started")
    
    while simulation_running:
        current_hour = datetime.now().hour
        is_rush = (8 <= current_hour <= 10) or (17 <= current_hour <= 20)
        
        # Update each lane with random (but realistic) values
        for direction in ["North", "South", "East", "West"]:
            base = random.randint(15, 35) if is_rush else random.randint(2, 20)
            junction_state[direction] = {
                "vehicle_count": base + random.randint(-3, 3),
                "queue_length": base * 4.5 + random.uniform(-5, 5),
                "avg_wait_time": base * 2.1 + random.uniform(-5, 5),
                "has_emergency": random.random() < 0.04,  # 4% chance of emergency
                "direction": direction
            }
        
        # Run AI optimizer
        lane_list = [
            {"direction": d, **junction_state[d]} 
            for d in ["North", "South", "East", "West"]
        ]
        current_signal_times = optimizer.calculate_green_times(lane_list)
        
        # Get congestion predictions for each lane
        predictions = {}
        for direction in ["North", "South", "East", "West"]:
            lane = junction_state[direction]
            predictions[direction] = predictor.predict(
                vehicle_count=lane["vehicle_count"],
                queue_length=lane["queue_length"],
                wait_time=lane["avg_wait_time"],
                hour=current_hour
            )
        
        # Check for emergency
        emergency_info = None
        for direction in ["North", "South", "East", "West"]:
            if junction_state[direction]["has_emergency"]:
                emergency_info = {"direction": direction, "type": "Ambulance"}
                save_emergency_event(direction, "Ambulance")
                break
        
        # Build the complete data package to send to React
        payload = {
            "timestamp": datetime.now().isoformat(),
            "lanes": {
                direction: {
                    **junction_state[direction],
                    "green_time": current_signal_times.get(direction, 10),
                    "congestion": predictions[direction]
                }
                for direction in ["North", "South", "East", "West"]
            },
            "emergency": emergency_info,
            "emergency_override": current_signal_times.get("emergency_override", False),
            "total_vehicles": sum(
                junction_state[d]["vehicle_count"] 
                for d in ["North", "South", "East", "West"]
            )
        }
        
        # Save to database
        save_junction_data(payload.copy())
        
        # Push to all connected React clients via WebSocket
        socketio.emit("junction_update", payload)
        
        time.sleep(3)  # Update every 3 seconds

# ============================================================
# API ROUTES
# ============================================================

@app.route("/")
def home():
    return jsonify({"message": "Junction AI API running!", "status": "ok"})

@app.route("/api/status")
def get_status():
    """Check if server is running"""
    return jsonify({
        "status": "running",
        "simulation": simulation_running,
        "timestamp": datetime.now().isoformat()
    })

@app.route("/api/junction/current")
def get_current_data():
    """Get the current junction state (used when React first loads)"""
    if not junction_state["North"]["vehicle_count"]:
        return jsonify({"message": "No data yet. Start simulation first."})
    
    lane_list = [{"direction": d, **junction_state[d]} for d in ["North", "South", "East", "West"]]
    green_times = optimizer.calculate_green_times(lane_list)
    
    return jsonify({
        "lanes": junction_state,
        "signal_times": green_times,
        "timestamp": datetime.now().isoformat()
    })

@app.route("/api/junction/history")
def get_history():
    """Get recent historical data for charts"""
    limit = request.args.get("limit", 20, type=int)
    data = get_recent_data(limit)
    return jsonify({"data": data, "count": len(data)})

@app.route("/api/analytics")
def get_analytics():
    """Get summary analytics for the dashboard"""
    summary = get_analytics_summary()
    summary.pop("_id", None)
    return jsonify(summary)

@app.route("/api/predict", methods=["POST"])
def predict_congestion():
    """Predict congestion for given inputs"""
    data = request.get_json()
    result = predictor.predict(
        vehicle_count=data.get("vehicle_count", 0),
        queue_length=data.get("queue_length", 0),
        wait_time=data.get("wait_time", 0),
        hour=data.get("hour", datetime.now().hour)
    )
    return jsonify(result)

@app.route("/api/simulate/start", methods=["POST"])
def start_simulation():
    """Start the traffic simulation"""
    global simulation_running
    if not simulation_running:
        thread = threading.Thread(target=run_simulation, daemon=True)
        thread.start()
        return jsonify({"message": "Simulation started!", "status": "running"})
    return jsonify({"message": "Simulation already running", "status": "running"})

@app.route("/api/simulate/stop", methods=["POST"])
def stop_simulation():
    """Stop the traffic simulation"""
    global simulation_running
    simulation_running = False
    return jsonify({"message": "Simulation stopped", "status": "stopped"})

@app.route("/api/emergency/trigger", methods=["POST"])
def trigger_emergency():
    """Manually trigger an emergency for testing"""
    data = request.get_json()
    direction = data.get("direction", "North")
    junction_state[direction]["has_emergency"] = True
    return jsonify({"message": f"Emergency triggered on {direction} lane", "direction": direction})

@app.route("/api/emergency/clear", methods=["POST"])
def clear_emergency():
    """Clear emergency state"""
    for direction in ["North", "South", "East", "West"]:
        junction_state[direction]["has_emergency"] = False
    return jsonify({"message": "All emergencies cleared"})

# ============================================================
# WEBSOCKET EVENTS
# ============================================================

@socketio.on("connect")
def handle_connect():
    print(f"✅ React client connected!")
    emit("connected", {"message": "Connected to Junction AI"})

@socketio.on("disconnect")
def handle_disconnect():
    print("❌ React client disconnected")

# ============================================================
# START SERVER
# ============================================================


# Add this import at top of app.py
from detector import detector
import base64

# Add this route in app.py
@app.route("/api/detect/frame", methods=["POST"])
def detect_from_frame():
    """
    Accepts a base64 image from React, runs YOLO detection, returns results.
    React sends camera frame → Flask runs YOLO → returns count + annotated frame
    """
    try:
        data = request.get_json()
        direction = data.get("direction", "North")
        
        # Decode base64 image
        image_data = data.get("frame", "")
        if not image_data:
            return jsonify({"error": "No frame provided"}), 400
        
        # Remove data URL prefix if present
        if "," in image_data:
            image_data = image_data.split(",")[1]
        
        img_bytes = base64.b64decode(image_data)
        img_array = np.frombuffer(img_bytes, dtype=np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        # Run detection
        result = detector.process_frame(frame)
        
        # Update junction state with detected values
        junction_state[direction]["vehicle_count"] = result["vehicle_count"]
        junction_state[direction]["queue_length"] = result["queue_length"]
        junction_state[direction]["avg_wait_time"] = result["avg_wait_time"]
        junction_state[direction]["has_emergency"] = result["has_emergency"]
        
        # Return annotated frame as base64
        if result["annotated_frame"] is not None:
            annotated_b64 = detector.frame_to_base64(result["annotated_frame"])
        else:
            annotated_b64 = image_data
        
        return jsonify({
            "vehicle_count": result["vehicle_count"],
            "has_emergency": result["has_emergency"],
            "vehicles": result["vehicles"],
            "annotated_frame": annotated_b64,
            "direction": direction
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == "__main__":
    print("🚦 Starting Junction AI Flask Server...")
    print("📍 API available at: http://localhost:5000")
    print("📡 WebSocket ready for React connection")
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port, debug=False)