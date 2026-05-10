# ai_engine.py
# The core AI brain — decides how long each traffic signal stays green

class SignalOptimizer:
    """
    AI-based traffic signal optimizer.
    
    How it works:
    - Takes vehicle counts from each direction (N, S, E, W)
    - Assigns green time proportionally — busier lane = more green time
    - Emergency vehicles always get immediate 60-second priority
    - Minimum green: 10 seconds (to avoid too-short cycles)
    - Maximum green: 90 seconds (to avoid others waiting too long)
    """
    
    MIN_GREEN = 10      # Minimum seconds any lane gets
    MAX_GREEN = 90      # Maximum seconds any lane gets
    TOTAL_CYCLE = 160   # Total cycle time in seconds (split among 4 lanes)

    def calculate_green_times(self, lane_data):
        """
        Main function: takes lane data, returns green times.
        
        Input example:
        lane_data = [
            {"direction": "North", "vehicle_count": 15, "has_emergency": False},
            {"direction": "South", "vehicle_count": 30, "has_emergency": False},
            {"direction": "East",  "vehicle_count": 5,  "has_emergency": True},
            {"direction": "West",  "vehicle_count": 20, "has_emergency": False},
        ]
        
        Output example:
        {
            "North": 30,
            "South": 55,
            "East": 90,   ← Emergency gets max time
            "West": 40,
            "emergency_override": True,
            "emergency_direction": "East"
        }
        """
        
        # Step 1: Check for emergency vehicles first
        for lane in lane_data:
            if lane.get("has_emergency", False):
                return self._emergency_override(lane["direction"], lane_data)
        
        # Step 2: Calculate scores for each lane
        scores = self._calculate_scores(lane_data)
        
        # Step 3: Convert scores to green times
        green_times = self._scores_to_green_times(scores, lane_data)
        
        green_times["emergency_override"] = False
        green_times["emergency_direction"] = None
        
        return green_times

    def _calculate_scores(self, lane_data):
        """
        Score each lane based on:
        - Vehicle count (most important: 60% weight)
        - Estimated queue length (30% weight)  
        - How long they've been waiting (10% weight)
        """
        scores = {}
        for lane in lane_data:
            direction = lane["direction"]
            vehicle_count = lane.get("vehicle_count", 0)
            queue_length = lane.get("queue_length", vehicle_count * 5)  # estimate if not provided
            wait_time = lane.get("avg_wait_time", 0)
            
            # Weighted score formula
            score = (
                vehicle_count * 0.6 +
                (queue_length / 10) * 0.3 +
                (wait_time / 10) * 0.1
            )
            scores[direction] = max(score, 0.1)  # Minimum score of 0.1
        
        return scores

    def _scores_to_green_times(self, scores, lane_data):
        """Convert raw scores into actual second values"""
        total_score = sum(scores.values())
        available_time = self.TOTAL_CYCLE - (self.MIN_GREEN * len(scores))
        
        green_times = {}
        for direction, score in scores.items():
            ratio = score / total_score
            extra_time = ratio * available_time
            green_time = int(self.MIN_GREEN + extra_time)
            green_time = min(green_time, self.MAX_GREEN)  # Cap at maximum
            green_times[direction] = green_time
        
        return green_times

    def _emergency_override(self, emergency_direction, lane_data):
        """
        When emergency vehicle detected:
        - Emergency lane gets MAX_GREEN (90 seconds)
        - All other lanes get MIN_GREEN (10 seconds)
        - Returns immediately without running normal optimizer
        """
        green_times = {}
        for lane in lane_data:
            direction = lane["direction"]
            if direction == emergency_direction:
                green_times[direction] = self.MAX_GREEN
            else:
                green_times[direction] = self.MIN_GREEN
        
        green_times["emergency_override"] = True
        green_times["emergency_direction"] = emergency_direction
        
        return green_times

    def get_signal_status(self, green_times):
        """
        Converts green times into signal status for display.
        Returns which signal is currently active and countdown.
        """
        directions = ["North", "South", "East", "West"]
        statuses = {}
        
        for i, direction in enumerate(directions):
            time_val = green_times.get(direction, self.MIN_GREEN)
            statuses[direction] = {
                "green_time": time_val,
                "status": "GREEN" if i == 0 else "RED",  # Simplified for demo
                "countdown": time_val
            }
        
        return statuses


# Create one instance to use throughout the app
optimizer = SignalOptimizer()

print("✅ AI Signal Optimizer loaded")