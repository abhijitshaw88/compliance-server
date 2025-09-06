"""
Compliance service for business logic
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import datetime, date

from app.models.compliance import (
    Project, Task, Compliance, GSTReturn, TDSReturn, 
    Document, TimeEntry
)


class ComplianceService:
    """Compliance service class"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # Project methods
    def get_project(self, project_id: int) -> Optional[Project]:
        """Get project by ID"""
        return self.db.query(Project).filter(Project.id == project_id).first()
    
    def get_projects(self, skip: int = 0, limit: int = 100,
                    client_id: int = None, status: str = None) -> List[Project]:
        """Get all projects with filters"""
        query = self.db.query(Project)
        
        if client_id:
            query = query.filter(Project.client_id == client_id)
        if status:
            query = query.filter(Project.status == status)
        
        return query.offset(skip).limit(limit).all()
    
    def create_project(self, project_data: dict) -> Project:
        """Create new project"""
        project = Project(**project_data)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project
    
    # Task methods
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get task by ID"""
        return self.db.query(Task).filter(Task.id == task_id).first()
    
    def get_tasks(self, skip: int = 0, limit: int = 100,
                 project_id: int = None, assigned_to: int = None,
                 status: str = None) -> List[Task]:
        """Get all tasks with filters"""
        query = self.db.query(Task)
        
        if project_id:
            query = query.filter(Task.project_id == project_id)
        if assigned_to:
            query = query.filter(Task.assigned_to == assigned_to)
        if status:
            query = query.filter(Task.status == status)
        
        return query.offset(skip).limit(limit).all()
    
    def create_task(self, task_data: dict) -> Task:
        """Create new task"""
        task = Task(**task_data)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def update_task(self, task_id: int, task_data: dict) -> Optional[Task]:
        """Update task"""
        task = self.get_task(task_id)
        if not task:
            return None
        
        # Update fields
        for field, value in task_data.items():
            if hasattr(task, field):
                setattr(task, field, value)
        
        # Mark as completed if status is completed
        if task_data.get("status") == "completed":
            task.completed_at = datetime.utcnow()
        
        task.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(task)
        return task
    
    # Compliance methods
    def get_compliance(self, compliance_id: int) -> Optional[Compliance]:
        """Get compliance by ID"""
        return self.db.query(Compliance).filter(Compliance.id == compliance_id).first()
    
    def get_compliances(self, skip: int = 0, limit: int = 100,
                       client_id: int = None, compliance_type: str = None,
                       status: str = None) -> List[Compliance]:
        """Get all compliances with filters"""
        query = self.db.query(Compliance)
        
        if client_id:
            query = query.filter(Compliance.client_id == client_id)
        if compliance_type:
            query = query.filter(Compliance.type == compliance_type)
        if status:
            query = query.filter(Compliance.status == status)
        
        return query.offset(skip).limit(limit).all()
    
    def create_compliance(self, compliance_data: dict) -> Compliance:
        """Create new compliance"""
        compliance = Compliance(**compliance_data)
        self.db.add(compliance)
        self.db.commit()
        self.db.refresh(compliance)
        return compliance
    
    # GST Return methods
    def get_gst_returns(self, skip: int = 0, limit: int = 100,
                       client_id: int = None, status: str = None) -> List[GSTReturn]:
        """Get GST returns with filters"""
        query = self.db.query(GSTReturn)
        
        if client_id:
            query = query.filter(GSTReturn.client_id == client_id)
        if status:
            query = query.filter(GSTReturn.status == status)
        
        return query.offset(skip).limit(limit).all()
    
    # TDS Return methods
    def get_tds_returns(self, skip: int = 0, limit: int = 100,
                       client_id: int = None, status: str = None) -> List[TDSReturn]:
        """Get TDS returns with filters"""
        query = self.db.query(TDSReturn)
        
        if client_id:
            query = query.filter(TDSReturn.client_id == client_id)
        if status:
            query = query.filter(TDSReturn.status == status)
        
        return query.offset(skip).limit(limit).all()
    
    # Time Entry methods
    def get_time_entries(self, skip: int = 0, limit: int = 100,
                        user_id: int = None, project_id: int = None,
                        client_id: int = None) -> List[TimeEntry]:
        """Get time entries with filters"""
        query = self.db.query(TimeEntry)
        
        if user_id:
            query = query.filter(TimeEntry.user_id == user_id)
        if project_id:
            query = query.filter(TimeEntry.project_id == project_id)
        if client_id:
            query = query.filter(TimeEntry.client_id == client_id)
        
        return query.offset(skip).limit(limit).all()
    
    def create_time_entry(self, time_entry_data: dict) -> TimeEntry:
        """Create new time entry"""
        time_entry = TimeEntry(**time_entry_data)
        self.db.add(time_entry)
        self.db.commit()
        self.db.refresh(time_entry)
        return time_entry
    
    def stop_time_entry(self, time_entry_id: int) -> Optional[TimeEntry]:
        """Stop a running time entry"""
        time_entry = self.db.query(TimeEntry).filter(
            and_(
                TimeEntry.id == time_entry_id,
                TimeEntry.end_time.is_(None)
            )
        ).first()
        
        if not time_entry:
            return None
        
        time_entry.end_time = datetime.utcnow()
        if time_entry.start_time:
            duration = time_entry.end_time - time_entry.start_time
            time_entry.duration_hours = duration.total_seconds() / 3600
        
        self.db.commit()
        self.db.refresh(time_entry)
        return time_entry
