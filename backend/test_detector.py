# test_detector.py — Run this to verify YOLO is working

from detector import detector
import cv2
# import urllib.request
import numpy as np

print("🧪 Testing YOLOv8 vehicle detection...")

# Download a test image from the web
# url = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/Beijing_traffic_jam.jpg/640px-Beijing_traffic_jam.jpg"
# req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
# response = urllib.request.urlopen(req)
# img_array = np.frombuffer(response.read(), dtype=np.uint8)
# frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
# Load local image
frame = cv2.imread("traffic.png")
if frame is not None:
    result = detector.process_frame(frame)
    print(f"✅ Detection successful!")
    print(f"   Vehicles found: {result['vehicle_count']}")
    print(f"   Vehicle types: {[v['type'] for v in result['vehicles']]}")
    print(f"   Emergency: {result['has_emergency']}")
    
    # Save the annotated image
    cv2.imwrite("test_output.jpg", result["annotated_frame"])
    print("   Annotated image saved as: test_output.jpg")
else:
    print("❌ Could not load test image")
    print("   Check your internet connection")