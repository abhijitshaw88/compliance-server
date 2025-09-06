"""
User-related Pydantic schemas
"""

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models.user import UserRole, UserStatus


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: str
    full_name: str
    phone: Optional[str] = None
    department: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str
    role: UserRole = UserRole.CLIENT


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    status: Optional[UserStatus] = None


class UserInDB(UserBase):
    """Schema for user in database"""
    id: int
    role: UserRole
    status: UserStatus
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None

    class Config:
        from_attributes = True


class User(UserInDB):
    """Schema for user response"""
    pass


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str


class Token(BaseModel):
    """Schema for access token"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for token data"""
    username: Optional[str] = None


class PermissionBase(BaseModel):
    """Base permission schema"""
    name: str
    description: Optional[str] = None
    resource: str
    action: str


class PermissionCreate(PermissionBase):
    """Schema for creating a permission"""
    pass


class Permission(PermissionBase):
    """Schema for permission response"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class RolePermissionCreate(BaseModel):
    """Schema for creating role permission"""
    role: UserRole
    permission_id: int


class RolePermission(RolePermissionCreate):
    """Schema for role permission response"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AuditLogBase(BaseModel):
    """Base audit log schema"""
    action: str
    resource: str
    resource_id: Optional[int] = None
    old_values: Optional[str] = None
    new_values: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class AuditLogCreate(AuditLogBase):
    """Schema for creating audit log"""
    user_id: int


class AuditLog(AuditLogBase):
    """Schema for audit log response"""
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
