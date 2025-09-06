"""
Compliance management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.compliance_service import ComplianceService

router = APIRouter()


@router.get("/projects/")
async def get_projects(
    skip: int = 0,
    limit: int = 100,
    client_id: int = None,
    status: str = None,
    db: Session = Depends(get_db)
):
    """Get all projects"""
    compliance_service = ComplianceService(db)
    projects = compliance_service.get_projects(
        skip=skip, limit=limit, client_id=client_id, status=status
    )
    return projects


@router.get("/projects/{project_id}")
async def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Get project by ID"""
    compliance_service = ComplianceService(db)
    project = compliance_service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/projects/")
async def create_project(
    project_data: dict,
    db: Session = Depends(get_db)
):
    """Create new project"""
    compliance_service = ComplianceService(db)
    project = compliance_service.create_project(project_data)
    return project


@router.get("/tasks/")
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    project_id: int = None,
    assigned_to: int = None,
    status: str = None,
    db: Session = Depends(get_db)
):
    """Get all tasks"""
    compliance_service = ComplianceService(db)
    tasks = compliance_service.get_tasks(
        skip=skip, limit=limit, project_id=project_id,
        assigned_to=assigned_to, status=status
    )
    return tasks


@router.get("/tasks/{task_id}")
async def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """Get task by ID"""
    compliance_service = ComplianceService(db)
    task = compliance_service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/tasks/")
async def create_task(
    task_data: dict,
    db: Session = Depends(get_db)
):
    """Create new task"""
    compliance_service = ComplianceService(db)
    task = compliance_service.create_task(task_data)
    return task


@router.put("/tasks/{task_id}")
async def update_task(
    task_id: int,
    task_data: dict,
    db: Session = Depends(get_db)
):
    """Update task"""
    compliance_service = ComplianceService(db)
    task = compliance_service.update_task(task_id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/compliances/")
async def get_compliances(
    skip: int = 0,
    limit: int = 100,
    client_id: int = None,
    compliance_type: str = None,
    status: str = None,
    db: Session = Depends(get_db)
):
    """Get all compliances"""
    compliance_service = ComplianceService(db)
    compliances = compliance_service.get_compliances(
        skip=skip, limit=limit, client_id=client_id,
        compliance_type=compliance_type, status=status
    )
    return compliances


@router.get("/compliances/{compliance_id}")
async def get_compliance(
    compliance_id: int,
    db: Session = Depends(get_db)
):
    """Get compliance by ID"""
    compliance_service = ComplianceService(db)
    compliance = compliance_service.get_compliance(compliance_id)
    if not compliance:
        raise HTTPException(status_code=404, detail="Compliance not found")
    return compliance


@router.post("/compliances/")
async def create_compliance(
    compliance_data: dict,
    db: Session = Depends(get_db)
):
    """Create new compliance"""
    compliance_service = ComplianceService(db)
    compliance = compliance_service.create_compliance(compliance_data)
    return compliance


@router.get("/gst-returns/")
async def get_gst_returns(
    skip: int = 0,
    limit: int = 100,
    client_id: int = None,
    status: str = None,
    db: Session = Depends(get_db)
):
    """Get GST returns"""
    compliance_service = ComplianceService(db)
    gst_returns = compliance_service.get_gst_returns(
        skip=skip, limit=limit, client_id=client_id, status=status
    )
    return gst_returns


@router.get("/tds-returns/")
async def get_tds_returns(
    skip: int = 0,
    limit: int = 100,
    client_id: int = None,
    status: str = None,
    db: Session = Depends(get_db)
):
    """Get TDS returns"""
    compliance_service = ComplianceService(db)
    tds_returns = compliance_service.get_tds_returns(
        skip=skip, limit=limit, client_id=client_id, status=status
    )
    return tds_returns


@router.get("/time-entries/")
async def get_time_entries(
    skip: int = 0,
    limit: int = 100,
    user_id: int = None,
    project_id: int = None,
    client_id: int = None,
    db: Session = Depends(get_db)
):
    """Get time entries"""
    compliance_service = ComplianceService(db)
    time_entries = compliance_service.get_time_entries(
        skip=skip, limit=limit, user_id=user_id,
        project_id=project_id, client_id=client_id
    )
    return time_entries


@router.post("/time-entries/")
async def create_time_entry(
    time_entry_data: dict,
    db: Session = Depends(get_db)
):
    """Create new time entry"""
    compliance_service = ComplianceService(db)
    time_entry = compliance_service.create_time_entry(time_entry_data)
    return time_entry
