from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean
from backend.database import Base
import datetime


class ConceptMemory(Base):
    __tablename__ = "concept_memory"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    concept_id = Column(String, index=True)

    memory_strength = Column(Float, default=0.3)
    last_revision_time = Column(DateTime, default=None)

    successful_recalls = Column(Integer, default=0)
    failed_recalls = Column(Integer, default=0)

    avg_response_time = Column(Float, default=5.0)
    hint_usage_rate = Column(Float, default=0.0)

    difficulty_level = Column(Float, default=0.5)
    importance_level = Column(Float, default=0.5)
    cognitive_load = Column(Float, default=0.5)

    decay_rate = Column(Float, default=0.1)
    stability_factor = Column(Float, default=1.0)
    interference_factor = Column(Float, default=1.0)

    fatigue_modifier = Column(Float, default=1.0)
    reinforcement_gain = Column(Float, default=0.2)
    prediction_uncertainty = Column(Float, default=0.15)

    confidence_state = Column(String, default="Weak")

    # Additional fields used by the scheduler
    weakness_severity = Column(Float, default=0.0)
    recommended_review_window = Column(String, default="7 days")
    episodic_replay_needed = Column(Boolean, default=False)
