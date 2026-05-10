# detector.py
# YOLOv8-based vehicle detection engine
# This is the "eyes" of our AI system

from ultralytics import YOLO
import cv2
import numpy as np
from datetime import datetime

# Vehicle class IDs in YOLO's COCO dataset
# (YOLO was trained on 80 classes; we only care about vehicles)
VEHICLE_CLASSES = {
    2: "car",
    3: "motorcycle", 
    5: "bus",
    7: "truck"
}

# Emergency vehicle keywords to detect from classification
EMERGENCY_KEYWORDS = ["ambulance", "fire truck", "police"]


class VehicleDetector:
    """
    Detects and counts vehicles in video frames using YOLOv8.
    
    Usage:
        detector = VehicleDetector()
        result = detector.process_frame(frame_image)
        print(result["vehicle_count"])  # Number of vehicles
        print(result["has_emergency"])  # True if ambulance detected
    """
    
    def __init__(self, model_size="yolov8n.pt"):
        """
        model_size options:
        - yolov8n.pt  → Nano  (fastest, less accurate)  ← USE THIS for demo
        - yolov8s.pt  → Small (good balance)
        - yolov8m.pt  → Medium (slower, more accurate)
        """
        print(f"🔄 Loading YOLOv8 model ({model_size})...")
        # Downloads model automatically on first run (~6MB for nano)
        self.model = YOLO(model_size)
        self.confidence_threshold = 0.45  # Only count detections >45% confident
        print("✅ YOLOv8 model loaded!")
    
    def process_frame(self, frame):
        """
        Main function: takes one video frame, returns detection results.
        
        Input: frame — numpy array (OpenCV image)
        Output: dict with counts and annotated frame
        """
        if frame is None:
            return self._empty_result()
        
        # Run YOLOv8 detection
        results = self.model(frame, conf=self.confidence_threshold, verbose=False)
        
        # Process the results
        vehicle_count = 0
        vehicles_found = []
        has_emergency = False
        
        for result in results:
            boxes = result.boxes
            if boxes is None:
                continue
                
            for box in boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                
                # Only process vehicle classes
                if class_id in VEHICLE_CLASSES:
                    vehicle_count += 1
                    vehicle_type = VEHICLE_CLASSES[class_id]
                    
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    
                    vehicles_found.append({
                        "type": vehicle_type,
                        "confidence": round(confidence * 100, 1),
                        "bbox": [int(x1), int(y1), int(x2), int(y2)]
                    })
                    
                    # Simple emergency detection: large vehicles flagged
                    # (In production, use a separate ambulance-trained model)
                    if vehicle_type in ["bus", "truck"] and confidence > 0.8:
                        # Check if it could be an emergency vehicle by size
                        bbox_area = (x2 - x1) * (y2 - y1)
                        frame_area = frame.shape[0] * frame.shape[1]
                        if bbox_area / frame_area > 0.15:  # Very large vehicle
                            has_emergency = True
        
        # Draw boxes on the frame for display
        annotated_frame = self._draw_boxes(frame.copy(), vehicles_found)
        
        return {
            "vehicle_count": vehicle_count,
            "vehicles": vehicles_found,
            "has_emergency": has_emergency,
            "annotated_frame": annotated_frame,
            "queue_length": vehicle_count * 5.5,   # Rough estimate: 5.5m per vehicle
            "avg_wait_time": vehicle_count * 2.3,  # Rough estimate: 2.3s per vehicle
            "timestamp": datetime.now().isoformat()
        }
    
    def _draw_boxes(self, frame, vehicles):
        """Draw colored bounding boxes and labels on the frame"""
        colors = {
            "car": (0, 255, 0),          # Green
            "motorcycle": (255, 165, 0),  # Orange
            "bus": (255, 0, 0),          # Blue
            "truck": (0, 0, 255)         # Red
        }
        
        for vehicle in vehicles:
            x1, y1, x2, y2 = vehicle["bbox"]
            vtype = vehicle["type"]
            color = colors.get(vtype, (128, 128, 128))
            
            # Draw rectangle
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # Draw label background
            label = f"{vtype} {vehicle['confidence']}%"
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
            cv2.rectangle(frame, (x1, y1 - 20), (x1 + label_size[0], y1), color, -1)
            
            # Draw label text
            cv2.putText(frame, label, (x1, y1 - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Add vehicle count overlay
        count_text = f"Vehicles: {len(vehicles)}"
        cv2.putText(frame, count_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
        return frame
    
    def process_video_file(self, video_path, direction="North"):
        """
        Process a video file and return results for each frame.
        Use this when you have a recorded video to demo.
        """
        cap = cv2.VideoCapture(video_path)
        results = []
        
        if not cap.isOpened():
            print(f"❌ Could not open video: {video_path}")
            return results
        
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process every 5th frame to save computation
            if frame_count % 5 == 0:
                result = self.process_frame(frame)
                result["direction"] = direction
                results.append(result)
            
            frame_count += 1
        
        cap.release()
        print(f"✅ Processed {frame_count} frames from {video_path}")
        return results
    
    def frame_to_base64(self, frame):
        """Convert OpenCV frame to base64 string for sending to React"""
        _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
        return __import__("base64").b64encode(buffer).decode("utf-8")
    
    def _empty_result(self):
        return {
            "vehicle_count": 0,
            "vehicles": [],
            "has_emergency": False,
            "annotated_frame": None,
            "queue_length": 0,
            "avg_wait_time": 0,
            "timestamp": datetime.now().isoformat()
        }


# Create one global detector instance
detector = VehicleDetector()

print("✅ Vehicle Detector ready")