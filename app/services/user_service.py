"""
User service for business logic
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import datetime

from app.models.user import User, Permission, RolePermission, AuditLog
from app.core.security import get_password_hash, verify_password
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """User service class"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.db.query(User).filter(User.username == username).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def create_user(self, user_data: dict) -> User:
        """Create new user"""
        # Check if user already exists
        if self.get_user_by_username(user_data["username"]):
            raise ValueError("Username already exists")
        if self.get_user_by_email(user_data["email"]):
            raise ValueError("Email already exists")
        
        # Hash password
        hashed_password = get_password_hash(user_data["password"])
        
        # Create user
        user = User(
            email=user_data["email"],
            username=user_data["username"],
            full_name=user_data["full_name"],
            hashed_password=hashed_password,
            role=user_data.get("role", "client"),
            phone=user_data.get("phone"),
            department=user_data.get("department"),
            created_by=user_data.get("created_by")
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        # Log user creation
        self._log_audit(
            user_id=user.id,
            action="CREATE_USER",
            resource="user",
            resource_id=user.id,
            new_values=str(user_data)
        )
        
        return user
    
    def update_user(self, user_id: int, user_data: dict) -> Optional[User]:
        """Update user"""
        user = self.get_user(user_id)
        if not user:
            return None
        
        # Store old values for audit
        old_values = {
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role,
            "status": user.status,
            "phone": user.phone,
            "department": user.department
        }
        
        # Update fields
        for field, value in user_data.items():
            if hasattr(user, field):
                setattr(user, field, value)
        
        user.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(user)
        
        # Log user update
        self._log_audit(
            user_id=user_id,
            action="UPDATE_USER",
            resource="user",
            resource_id=user_id,
            old_values=str(old_values),
            new_values=str(user_data)
        )
        
        return user
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user"""
        user = self.get_user(user_id)
        if not user:
            return False
        
        # Log user deletion
        self._log_audit(
            user_id=user_id,
            action="DELETE_USER",
            resource="user",
            resource_id=user_id,
            old_values=str({"username": user.username, "email": user.email})
        )
        
        self.db.delete(user)
        self.db.commit()
        return True
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user"""
        user = self.get_user_by_username(username)
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        # Update last login
        user.last_login = datetime.utcnow()
        self.db.commit()
        
        return user
    
    def get_permissions(self) -> List[Permission]:
        """Get all permissions"""
        return self.db.query(Permission).all()
    
    def create_permission(self, permission_data: dict) -> Permission:
        """Create new permission"""
        permission = Permission(**permission_data)
        self.db.add(permission)
        self.db.commit()
        self.db.refresh(permission)
        return permission
    
    def get_role_permissions(self) -> List[RolePermission]:
        """Get all role permissions"""
        return self.db.query(RolePermission).all()
    
    def create_role_permission(self, role_permission_data: dict) -> RolePermission:
        """Create new role permission"""
        role_permission = RolePermission(**role_permission_data)
        self.db.add(role_permission)
        self.db.commit()
        self.db.refresh(role_permission)
        return role_permission
    
    def _log_audit(self, user_id: int, action: str, resource: str, 
                   resource_id: int = None, old_values: str = None, 
                   new_values: str = None, ip_address: str = None, 
                   user_agent: str = None):
        """Log audit trail"""
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource=resource,
            resource_id=resource_id,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent
        )
        self.db.add(audit_log)
        self.db.commit()
