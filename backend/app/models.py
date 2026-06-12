from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from backend.app.database import Base

class MetricLog(Base):
    __tablename__ = "metric_logs"

    id = Column(Integer, primary_key=True, index=True)
    service = Column(String, index=True)       # ex: 'web', 'database', 'dns', 'smtp'
    metric_name = Column(String, index=True)  # ex: 'latency', 'rps', 'qps', 'availability'
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class SecurityEvent(Base):
    __tablename__ = "security_events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, index=True)   # ex: 'ddos', 'brute_force', 'config_change'
    severity = Column(String)                 # 'AMARELO' ou 'VERMELHO'
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)