"""
Storage module for managing carbon footprint calculation history.
Handles saving, loading, and retrieving user calculation data.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class CarbonFootprintStorage:
    """Manages persistent storage of carbon footprint calculations."""
    
    def __init__(self, storage_file: str = "carbon_history.json"):
        """Initialize storage with file path."""
        self.storage_file = storage_file
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create storage file if it doesn't exist."""
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, 'w') as f:
                json.dump({"calculations": [], "goals": [], "settings": {}}, f)
    
    def save_calculation(self, data: Dict) -> bool:
        """
        Save a new calculation to history.
        
        Args:
            data: Dictionary containing calculation results and inputs
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            history = self.load_history()
            
            # Add timestamp if not present
            if "timestamp" not in data:
                data["timestamp"] = datetime.now().isoformat()
            
            history["calculations"].append(data)
            
            with open(self.storage_file, 'w') as f:
                json.dump(history, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving calculation: {e}")
            return False
    
    def load_history(self) -> Dict:
        """Load complete history from storage."""
        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading history: {e}")
            return {"calculations": [], "goals": [], "settings": {}}
    
    def get_calculations(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Get calculation history.
        
        Args:
            limit: Maximum number of recent calculations to return
            
        Returns:
            List of calculation dictionaries, most recent first
        """
        history = self.load_history()
        calculations = history.get("calculations", [])
        
        # Sort by timestamp, most recent first
        calculations.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        if limit:
            return calculations[:limit]
        return calculations
    
    def get_latest_calculation(self) -> Optional[Dict]:
        """Get the most recent calculation."""
        calculations = self.get_calculations(limit=1)
        return calculations[0] if calculations else None
    
    def clear_history(self) -> bool:
        """Clear all calculation history."""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump({"calculations": [], "goals": [], "settings": {}}, f)
            return True
        except Exception as e:
            print(f"Error clearing history: {e}")
            return False
    
    def save_goal(self, goal_data: Dict) -> bool:
        """Save a carbon reduction goal."""
        try:
            history = self.load_history()
            
            if "timestamp" not in goal_data:
                goal_data["timestamp"] = datetime.now().isoformat()
            
            # Replace existing active goal or add new one
            history["goals"] = [goal_data]
            
            with open(self.storage_file, 'w') as f:
                json.dump(history, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving goal: {e}")
            return False
    
    def get_active_goal(self) -> Optional[Dict]:
        """Get the currently active goal."""
        history = self.load_history()
        goals = history.get("goals", [])
        return goals[0] if goals else None
    
    def update_settings(self, settings: Dict) -> bool:
        """Update user settings."""
        try:
            history = self.load_history()
            history["settings"].update(settings)
            
            with open(self.storage_file, 'w') as f:
                json.dump(history, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error updating settings: {e}")
            return False
    
    def get_settings(self) -> Dict:
        """Get user settings."""
        history = self.load_history()
        return history.get("settings", {})
    
    def get_statistics(self) -> Dict:
        """Calculate statistics from history."""
        calculations = self.get_calculations()
        
        if not calculations:
            return {
                "total_calculations": 0,
                "average_footprint": 0,
                "lowest_footprint": 0,
                "highest_footprint": 0,
                "trend": "neutral"
            }
        
        footprints = [calc.get("total_emissions", 0) for calc in calculations]
        
        # Calculate trend (comparing latest vs average of previous)
        trend = "neutral"
        if len(footprints) > 1:
            latest = footprints[0]
            previous_avg = sum(footprints[1:]) / len(footprints[1:])
            if latest < previous_avg * 0.95:
                trend = "improving"
            elif latest > previous_avg * 1.05:
                trend = "worsening"
        
        return {
            "total_calculations": len(calculations),
            "average_footprint": round(sum(footprints) / len(footprints), 2),
            "lowest_footprint": round(min(footprints), 2),
            "highest_footprint": round(max(footprints), 2),
            "trend": trend,
            "first_calculation_date": calculations[-1].get("timestamp", "Unknown"),
            "latest_calculation_date": calculations[0].get("timestamp", "Unknown")
        }
