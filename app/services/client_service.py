"""
Client service for business logic
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import datetime

from app.models.financial import Client
from app.schemas.financial import ClientCreate, ClientUpdate


class ClientService:
    """Client service class"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_client(self, client_id: int) -> Optional[Client]:
        """Get client by ID"""
        return self.db.query(Client).filter(Client.id == client_id).first()
    
    def get_clients(self, skip: int = 0, limit: int = 100, search: str = None) -> List[Client]:
        """Get all clients with pagination and search"""
        query = self.db.query(Client)
        
        if search:
            search_filter = or_(
                Client.name.ilike(f"%{search}%"),
                Client.email.ilike(f"%{search}%"),
                Client.phone.ilike(f"%{search}%"),
                Client.gstin.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        return query.offset(skip).limit(limit).all()
    
    def create_client(self, client_data: dict) -> Client:
        """Create new client"""
        # Check if client with same GSTIN already exists
        if client_data.get("gstin"):
            existing_client = self.db.query(Client).filter(
                Client.gstin == client_data["gstin"]
            ).first()
            if existing_client:
                raise ValueError("Client with this GSTIN already exists")
        
        client = Client(**client_data)
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client
    
    def update_client(self, client_id: int, client_data: dict) -> Optional[Client]:
        """Update client"""
        client = self.get_client(client_id)
        if not client:
            return None
        
        # Check GSTIN uniqueness if being updated
        if client_data.get("gstin") and client_data["gstin"] != client.gstin:
            existing_client = self.db.query(Client).filter(
                and_(
                    Client.gstin == client_data["gstin"],
                    Client.id != client_id
                )
            ).first()
            if existing_client:
                raise ValueError("Client with this GSTIN already exists")
        
        # Update fields
        for field, value in client_data.items():
            if hasattr(client, field):
                setattr(client, field, value)
        
        client.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(client)
        return client
    
    def delete_client(self, client_id: int) -> bool:
        """Delete client"""
        client = self.get_client(client_id)
        if not client:
            return False
        
        self.db.delete(client)
        self.db.commit()
        return True
    
    def get_client_projects(self, client_id: int) -> List[dict]:
        """Get client projects"""
        from app.models.compliance import Project
        projects = self.db.query(Project).filter(Project.client_id == client_id).all()
        return [
            {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "start_date": project.start_date,
                "end_date": project.end_date,
                "status": project.status,
                "budget": project.budget
            }
            for project in projects
        ]
    
    def get_client_invoices(self, client_id: int) -> List[dict]:
        """Get client invoices"""
        from app.models.financial import Invoice
        invoices = self.db.query(Invoice).filter(Invoice.client_id == client_id).all()
        return [
            {
                "id": invoice.id,
                "invoice_number": invoice.invoice_number,
                "issue_date": invoice.issue_date,
                "due_date": invoice.due_date,
                "total_amount": invoice.total_amount,
                "status": invoice.status
            }
            for invoice in invoices
        ]
