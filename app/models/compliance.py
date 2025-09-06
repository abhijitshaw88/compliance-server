"""
Compliance and tax management models
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Numeric, ForeignKey, Enum, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class ComplianceType(str, enum.Enum):
    """Compliance types"""
    GST = "gst"
    TDS = "tds"
    ITR = "itr"
    PF = "pf"
    ESI = "esi"
    ROC = "roc"
    CUSTOM = "custom"


class ComplianceStatus(str, enum.Enum):
    """Compliance status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class TaskPriority(str, enum.Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Project(Base):
    """Project model"""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    status = Column(String(20), default="active")
    budget = Column(Numeric(15, 2), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    client = relationship("Client", back_populates="projects")
    tasks = relationship("Task", back_populates="project")


class Task(Base):
    """Task model"""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM)
    status = Column(String(20), default="pending")
    due_date = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    estimated_hours = Column(Numeric(5, 2), nullable=True)
    actual_hours = Column(Numeric(5, 2), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="tasks")


class Compliance(Base):
    """Compliance model"""
    __tablename__ = "compliances"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(Enum(ComplianceType), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    due_date = Column(Date, nullable=False)
    status = Column(Enum(ComplianceStatus), default=ComplianceStatus.PENDING)
    description = Column(Text, nullable=True)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    completed_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class GSTReturn(Base):
    """GST Return model"""
    __tablename__ = "gst_returns"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    return_type = Column(String(20), nullable=False)  # GSTR-1, GSTR-3B, GSTR-9, etc.
    tax_period = Column(String(20), nullable=False)  # 2023-24
    due_date = Column(Date, nullable=False)
    filing_date = Column(Date, nullable=True)
    status = Column(Enum(ComplianceStatus), default=ComplianceStatus.PENDING)
    total_tax_liability = Column(Numeric(15, 2), default=0)
    total_tax_paid = Column(Numeric(15, 2), default=0)
    penalty_amount = Column(Numeric(15, 2), default=0)
    acknowledgment_number = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class TDSReturn(Base):
    """TDS Return model"""
    __tablename__ = "tds_returns"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    form_type = Column(String(10), nullable=False)  # 24Q, 26Q, 27Q, etc.
    quarter = Column(String(10), nullable=False)  # Q1, Q2, Q3, Q4
    financial_year = Column(String(10), nullable=False)  # 2023-24
    due_date = Column(Date, nullable=False)
    filing_date = Column(Date, nullable=True)
    status = Column(Enum(ComplianceStatus), default=ComplianceStatus.PENDING)
    total_tds_deducted = Column(Numeric(15, 2), default=0)
    total_tds_deposited = Column(Numeric(15, 2), default=0)
    acknowledgment_number = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Document(Base):
    """Document model"""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String(100), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_processed = Column(Boolean, default=False)
    extracted_data = Column(Text, nullable=True)  # JSON string
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    client = relationship("Client")
    project = relationship("Project")
    task = relationship("Task")
    uploader = relationship("User")


class TimeEntry(Base):
    """Time tracking model"""
    __tablename__ = "time_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    duration_hours = Column(Numeric(5, 2), nullable=True)
    description = Column(Text, nullable=True)
    is_billable = Column(Boolean, default=True)
    hourly_rate = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User")
    project = relationship("Project")
    task = relationship("Task")
    client = relationship("Client")
