from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import json
from .database import Base


class Citizen(Base):
    __tablename__ = "citizens"

    id = Column(String(50), primary_key=True, index=True)  # e.g. "C001"
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    state = Column(String(50), default="Maharashtra")

    applications = relationship("Application", back_populates="citizen")


class Service(Base):
    __tablename__ = "services"

    id = Column(String(50), primary_key=True, index=True)  # e.g. "SRV-AGRI-001"
    title = Column(String(150), nullable=False)
    department = Column(String(100), nullable=False)
    category = Column(String(50), default="Agriculture")
    description = Column(Text, nullable=False)
    benefit_amount = Column(String(50), default="₹15,000 / Season")
    eligibility = Column(Text, nullable=True)
    required_data_source = Column(String(100), default="Revenue Department Land Records")
    is_active = Column(Boolean, default=True)

    applications = relationship("Application", back_populates="service")


class Application(Base):
    __tablename__ = "applications"

    id = Column(String(50), primary_key=True, index=True)  # e.g. "APP-2026-001"
    citizen_id = Column(String(50), ForeignKey("citizens.id"), nullable=False)
    service_id = Column(String(50), ForeignKey("services.id"), nullable=False)
    status = Column(String(50), default="CONSENT_PENDING")  # DRAFT, CONSENT_PENDING, CONSENT_GRANTED, VERIFIED, REJECTED
    department_application_id = Column(String(50), default="A001")  # Mapped ID in Agriculture Dept
    land_id = Column(String(50), nullable=True)
    land_area = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    citizen = relationship("Citizen", back_populates="applications")
    service = relationship("Service", back_populates="applications")
    consent = relationship("ConsentRecord", back_populates="application", uselist=False)
    audit_events = relationship("AuditEvent", back_populates="application", order_by="AuditEvent.timestamp.asc()")


class ConsentRecord(Base):
    __tablename__ = "consents"

    id = Column(String(50), primary_key=True, index=True)
    application_id = Column(String(50), ForeignKey("applications.id"), nullable=False)
    citizen_id = Column(String(50), nullable=False)
    purpose = Column(Text, nullable=False)
    data_source = Column(String(100), default="Revenue Department")
    data_recipient = Column(String(100), default="Department of Agriculture")
    status = Column(String(20), default="PENDING")  # PENDING, GRANTED, DENIED, REVOKED
    granted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    application = relationship("Application", back_populates="consent")


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    application_id = Column(String(50), ForeignKey("applications.id"), nullable=False)
    event_type = Column(String(50), nullable=False)
    source = Column(String(50), nullable=False)  # Citizen, MahaSync, Revenue, Agriculture, RabbitMQ
    description = Column(Text, nullable=False)
    status = Column(String(50), default="SUCCESS")
    metadata_json = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    application = relationship("Application", back_populates="audit_events")
