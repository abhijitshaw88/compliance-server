"""
AI-powered features endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.ai_service import AIService

router = APIRouter()


@router.post("/document-extraction/")
async def extract_document_data(
    file: UploadFile = File(...),
    extraction_type: str = "invoice",
    db: Session = Depends(get_db)
):
    """Extract data from uploaded document using AI"""
    ai_service = AIService(db)
    try:
        extracted_data = await ai_service.extract_document_data(file, extraction_type)
        return extracted_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Document extraction failed: {str(e)}"
        )


@router.post("/document-batch-processing/")
async def batch_process_documents(
    files: List[UploadFile] = File(...),
    extraction_type: str = "invoice",
    db: Session = Depends(get_db)
):
    """Batch process multiple documents"""
    ai_service = AIService(db)
    try:
        results = await ai_service.batch_process_documents(files, extraction_type)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Batch processing failed: {str(e)}"
        )


@router.post("/gst-reconciliation/")
async def gst_reconciliation(
    client_id: int,
    period: str,
    db: Session = Depends(get_db)
):
    """AI-powered GST reconciliation"""
    ai_service = AIService(db)
    try:
        reconciliation_result = await ai_service.gst_reconciliation(client_id, period)
        return reconciliation_result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"GST reconciliation failed: {str(e)}"
        )


@router.post("/tds-reconciliation/")
async def tds_reconciliation(
    client_id: int,
    quarter: str,
    db: Session = Depends(get_db)
):
    """AI-powered TDS reconciliation"""
    ai_service = AIService(db)
    try:
        reconciliation_result = await ai_service.tds_reconciliation(client_id, quarter)
        return reconciliation_result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"TDS reconciliation failed: {str(e)}"
        )


@router.post("/compliance-monitoring/")
async def compliance_monitoring(
    client_id: int = None,
    compliance_type: str = None,
    db: Session = Depends(get_db)
):
    """AI-powered compliance monitoring and alerts"""
    ai_service = AIService(db)
    try:
        monitoring_result = await ai_service.compliance_monitoring(client_id, compliance_type)
        return monitoring_result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Compliance monitoring failed: {str(e)}"
        )


@router.get("/ai-accuracy/")
async def get_ai_accuracy(
    db: Session = Depends(get_db)
):
    """Get AI model accuracy metrics"""
    ai_service = AIService(db)
    try:
        accuracy_metrics = await ai_service.get_ai_accuracy()
        return accuracy_metrics
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get AI accuracy: {str(e)}"
        )


@router.post("/smart-categorization/")
async def smart_categorization(
    transaction_data: dict,
    db: Session = Depends(get_db)
):
    """AI-powered transaction categorization"""
    ai_service = AIService(db)
    try:
        categorization_result = await ai_service.smart_categorization(transaction_data)
        return categorization_result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Smart categorization failed: {str(e)}"
        )


@router.post("/anomaly-detection/")
async def anomaly_detection(
    client_id: int,
    data_type: str = "financial",
    db: Session = Depends(get_db)
):
    """AI-powered anomaly detection in financial data"""
    ai_service = AIService(db)
    try:
        anomalies = await ai_service.anomaly_detection(client_id, data_type)
        return anomalies
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Anomaly detection failed: {str(e)}"
        )
