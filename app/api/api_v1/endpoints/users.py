"""
User management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.user import User, UserCreate, UserUpdate, Permission, RolePermission
from app.services.user_service import UserService

router = APIRouter()


@router.get("/", response_model=List[User])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all users"""
    user_service = UserService(db)
    users = user_service.get_users(skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get user by ID"""
    user_service = UserService(db)
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=User)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Create new user"""
    user_service = UserService(db)
    user = user_service.create_user(user_data.dict())
    return user


@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    """Update user"""
    user_service = UserService(db)
    user = user_service.update_user(user_id, user_data.dict(exclude_unset=True))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Delete user"""
    user_service = UserService(db)
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


@router.get("/permissions/", response_model=List[Permission])
async def get_permissions(
    db: Session = Depends(get_db)
):
    """Get all permissions"""
    user_service = UserService(db)
    permissions = user_service.get_permissions()
    return permissions


@router.post("/permissions/", response_model=Permission)
async def create_permission(
    permission_data: dict,
    db: Session = Depends(get_db)
):
    """Create new permission"""
    user_service = UserService(db)
    permission = user_service.create_permission(permission_data)
    return permission


@router.get("/role-permissions/", response_model=List[RolePermission])
async def get_role_permissions(
    db: Session = Depends(get_db)
):
    """Get all role permissions"""
    user_service = UserService(db)
    role_permissions = user_service.get_role_permissions()
    return role_permissions


@router.post("/role-permissions/", response_model=RolePermission)
async def create_role_permission(
    role_permission_data: dict,
    db: Session = Depends(get_db)
):
    """Create new role permission"""
    user_service = UserService(db)
    role_permission = user_service.create_role_permission(role_permission_data)
    return role_permission
