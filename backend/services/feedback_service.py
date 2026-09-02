"""Service for handling user feedback storage."""
import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


class FeedbackService:
    """Service for saving prediction feedback."""

    FIELDNAMES = [
        "recorded_at",
        "model_name",
        "prediction",
        "confidence",
        "save_for_improvement",
        "passenger_name",
        "airline_name",
        "destination",
        "travel_reason",
        "booking_channel",
        "overall_service_rating",
        "comment",
        "Gender",
        "Customer Type",
        "Age",
        "Type of Travel",
        "Class",
        "Flight Distance",
        "Inflight wifi service",
        "Departure/Arrival time convenient",
        "Ease of Online booking",
        "Gate location",
        "Food and drink",
        "Online boarding",
        "Seat comfort",
        "Inflight entertainment",
        "On-board service",
        "Leg room service",
        "Baggage handling",
        "Checkin service",
        "Inflight service",
        "Cleanliness",
        "Departure Delay in Minutes",
    ]

    def __init__(self, feedback_log_path: Path):
        """Initialize feedback service.
        
        Args:
            feedback_log_path: Path to CSV file for storing feedback
        """
        self.feedback_log_path = feedback_log_path
        self.feedback_log_path.parent.mkdir(exist_ok=True)

    def save_record(self, record: dict) -> None:
        """Save a feedback record to CSV.
        
        Args:
            record: Dictionary with feedback data
        """
        file_exists = self.feedback_log_path.exists()
        
        with self.feedback_log_path.open("a", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.FIELDNAMES)
            
            if not file_exists:
                writer.writeheader()
            
            row = {key: record.get(key, "") for key in self.FIELDNAMES}
            writer.writerow(row)

    def create_feedback_record(
        self,
        model_name: str,
        prediction: str,
        confidence: float,
        payload_dict: dict,
        metadata: Optional[dict] = None,
    ) -> dict:
        """Create a feedback record.
        
        Args:
            model_name: Name of the model used
            prediction: Prediction result
            confidence: Confidence/probability of prediction
            payload_dict: Original input features
            metadata: Optional metadata about the prediction
            
        Returns:
            Dictionary ready to be saved
        """
        metadata = metadata or {}
        
        record = {
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "model_name": model_name,
            "prediction": prediction,
            "confidence": confidence,
            "save_for_improvement": True,
            "passenger_name": metadata.get("passenger_name", ""),
            "airline_name": metadata.get("airline_name", ""),
            "destination": metadata.get("destination", ""),
            "travel_reason": metadata.get("travel_reason", ""),
            "booking_channel": metadata.get("booking_channel", ""),
            "overall_service_rating": metadata.get("overall_service_rating", ""),
            "comment": metadata.get("comment", ""),
        }
        record.update(payload_dict)
        
        return record
