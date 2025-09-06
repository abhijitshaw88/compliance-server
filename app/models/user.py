"""
User and authentication models
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class UserRole(str, enum.Enum):
    """User roles enum"""
    ADMIN = "admin"
    MANAGER = "manager"
    ACCOUNTANT = "accountant"
    AUDITOR = "auditor"
    DATA_ENTRY = "data_entry"
    CLIENT = "client"


class UserStatus(str, enum.Enum):
    """User status enum"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CLIENT)
    status = Column(Enum(UserStatus), default=UserStatus.PENDING)
    phone = Column(String(20), nullable=True)
    department = Column(String(100), nullable=True)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(Integer, nullable=True)
    
    # Relationships
    clients = relationship("Client", back_populates="assigned_user")
    audit_logs = relationship("AuditLog", back_populates="user")


class Permission(Base):
    """Permission model"""
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    resource = Column(String(100), nullable=False)  # e.g., 'client', 'invoice', 'report'
    action = Column(String(50), nullable=False)     # e.g., 'create', 'read', 'update', 'delete'
    created_at = Column(DateTime, default=func.now())


class RolePermission(Base):
    """Role-Permission mapping"""
    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(Enum(UserRole), nullable=False)
    permission_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())


class AuditLog(Base):
    """Audit log for tracking user actions"""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(100), nullable=False)
    resource = Column(String(100), nullable=False)
    resource_id = Column(Integer, nullable=True)
    old_values = Column(Text, nullable=True)  # JSON string
    new_values = Column(Text, nullable=True)  # JSON string
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
