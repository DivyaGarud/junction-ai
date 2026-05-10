# predictor.py
# Machine learning model to predict traffic congestion level

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pickle
import os

class CongestionPredictor:
    """
    Predicts whether traffic will be LOW, MEDIUM, or HIGH congestion.
    
    Uses a Random Forest — an AI model that learns patterns from data.
    Since we don't have real historical data, we train on synthetic data
    that follows realistic traffic patterns.
    """
    
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,    # 100 decision trees (more = more accurate)
            random_state=42      # Fixed seed for reproducibility
        )
        self.is_trained = False
        self.model_path = "utils/congestion_model.pkl"
        
        # Load existing model or train a new one
        if os.path.exists(self.model_path):
            self.load_model()
        else:
            self.train()
    
    def _generate_training_data(self):
        """
        Generate realistic synthetic training data.
        
        Features (inputs):
        - vehicle_count: How many vehicles in the lane (0-50)
        - queue_length: How long the queue is in meters (0-300)
        - avg_wait_time: How long cars have been waiting (0-120 sec)
        - hour_of_day: What hour is it (0-23)
        - day_of_week: Day (0=Monday, 6=Sunday)
        
        Labels (outputs):
        - 0 = LOW congestion
        - 1 = MEDIUM congestion
        - 2 = HIGH congestion
        """
        np.random.seed(42)
        n_samples = 2000
        
        X = []  # Features
        y = []  # Labels
        
        for _ in range(n_samples):
            hour = np.random.randint(0, 24)
            day = np.random.randint(0, 7)
            
            # Rush hours (8-10 AM and 5-8 PM on weekdays) = more vehicles
            is_rush_hour = (8 <= hour <= 10 or 17 <= hour <= 20) and day < 5
            is_night = 23 <= hour or hour <= 5
            
            if is_rush_hour:
                vehicle_count = np.random.randint(20, 50)
                queue_length = np.random.uniform(80, 300)
                wait_time = np.random.uniform(60, 120)
            elif is_night:
                vehicle_count = np.random.randint(0, 8)
                queue_length = np.random.uniform(0, 30)
                wait_time = np.random.uniform(0, 20)
            else:
                vehicle_count = np.random.randint(5, 30)
                queue_length = np.random.uniform(10, 150)
                wait_time = np.random.uniform(10, 70)
            
            X.append([vehicle_count, queue_length, wait_time, hour, day])
            
            # Assign label based on vehicle count (simple rule)
            if vehicle_count >= 30:
                y.append(2)  # HIGH
            elif vehicle_count >= 15:
                y.append(1)  # MEDIUM
            else:
                y.append(0)  # LOW
        
        return np.array(X), np.array(y)
    
    def train(self):
        """Train the model on synthetic data"""
        print("🧠 Training congestion prediction model...")
        X, y = self._generate_training_data()
        self.model.fit(X, y)
        self.is_trained = True
        self.save_model()
        print("✅ Congestion model trained and saved!")
    
    def predict(self, vehicle_count, queue_length, wait_time, hour, day_of_week=1):
        """
        Predict congestion level for given inputs.
        Returns: dict with level, label, and probability
        """
        if not self.is_trained:
            self.train()
        
        features = np.array([[vehicle_count, queue_length, wait_time, hour, day_of_week]])
        
        prediction = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        
        levels = {0: "LOW", 1: "MEDIUM", 2: "HIGH"}
        colors = {0: "#22c55e", 1: "#f59e0b", 2: "#ef4444"}
        
        return {
            "level": int(prediction),
            "label": levels[prediction],
            "color": colors[prediction],
            "confidence": round(float(max(probabilities)) * 100, 1),
            "probabilities": {
                "LOW": round(float(probabilities[0]) * 100, 1),
                "MEDIUM": round(float(probabilities[1]) * 100, 1),
                "HIGH": round(float(probabilities[2]) * 100, 1)
            }
        }
    
    def save_model(self):
        """Save trained model to disk"""
        os.makedirs("utils", exist_ok=True)
        with open(self.model_path, "wb") as f:
            pickle.dump(self.model, f)
    
    def load_model(self):
        """Load previously trained model"""
        with open(self.model_path, "rb") as f:
            self.model = pickle.load(f)
        self.is_trained = True
        print("✅ Congestion model loaded from disk")


# Create one global instance
predictor = CongestionPredictor()

print("✅ Congestion Predictor ready")