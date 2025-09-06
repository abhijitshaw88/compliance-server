"""
Client management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.financial import Client, ClientCreate, ClientUpdate
from app.services.client_service import ClientService

router = APIRouter()


@router.get("/", response_model=List[Client])
async def get_clients(
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    db: Session = Depends(get_db)
):
    """Get all clients"""
    client_service = ClientService(db)
    clients = client_service.get_clients(skip=skip, limit=limit, search=search)
    return clients


@router.get("/{client_id}", response_model=Client)
async def get_client(
    client_id: int,
    db: Session = Depends(get_db)
):
    """Get client by ID"""
    client_service = ClientService(db)
    client = client_service.get_client(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.post("/", response_model=Client)
async def create_client(
    client_data: ClientCreate,
    db: Session = Depends(get_db)
):
    """Create new client"""
    client_service = ClientService(db)
    client = client_service.create_client(client_data.dict())
    return client


@router.put("/{client_id}", response_model=Client)
async def update_client(
    client_id: int,
    client_data: ClientUpdate,
    db: Session = Depends(get_db)
):
    """Update client"""
    client_service = ClientService(db)
    client = client_service.update_client(client_id, client_data.dict(exclude_unset=True))
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.delete("/{client_id}")
async def delete_client(
    client_id: int,
    db: Session = Depends(get_db)
):
    """Delete client"""
    client_service = ClientService(db)
    success = client_service.delete_client(client_id)
    if not success:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"message": "Client deleted successfully"}


@router.get("/{client_id}/projects")
async def get_client_projects(
    client_id: int,
    db: Session = Depends(get_db)
):
    """Get client projects"""
    client_service = ClientService(db)
    projects = client_service.get_client_projects(client_id)
    return projects


@router.get("/{client_id}/invoices")
async def get_client_invoices(
    client_id: int,
    db: Session = Depends(get_db)
):
    """Get client invoices"""
    client_service = ClientService(db)
    invoices = client_service.get_client_invoices(client_id)
    return invoices
