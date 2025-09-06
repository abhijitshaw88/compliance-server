"""
Financial management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.financial import (
    Invoice, InvoiceCreate, InvoiceUpdate, InvoiceItem,
    Payment, PaymentCreate, PaymentUpdate,
    ChartOfAccounts, ChartOfAccountsCreate,
    GeneralLedger, GeneralLedgerCreate,
    BankReconciliation, BankReconciliationCreate
)
from app.services.financial_service import FinancialService

router = APIRouter()


# Invoice endpoints
@router.get("/invoices/", response_model=List[Invoice])
async def get_invoices(
    skip: int = 0,
    limit: int = 100,
    client_id: int = None,
    status: str = None,
    db: Session = Depends(get_db)
):
    """Get all invoices"""
    financial_service = FinancialService(db)
    invoices = financial_service.get_invoices(
        skip=skip, limit=limit, client_id=client_id, status=status
    )
    return invoices


@router.get("/invoices/{invoice_id}", response_model=Invoice)
async def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db)
):
    """Get invoice by ID"""
    financial_service = FinancialService(db)
    invoice = financial_service.get_invoice(invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.post("/invoices/", response_model=Invoice)
async def create_invoice(
    invoice_data: InvoiceCreate,
    db: Session = Depends(get_db)
):
    """Create new invoice"""
    financial_service = FinancialService(db)
    invoice = financial_service.create_invoice(invoice_data.dict())
    return invoice


@router.put("/invoices/{invoice_id}", response_model=Invoice)
async def update_invoice(
    invoice_id: int,
    invoice_data: InvoiceUpdate,
    db: Session = Depends(get_db)
):
    """Update invoice"""
    financial_service = FinancialService(db)
    invoice = financial_service.update_invoice(invoice_id, invoice_data.dict(exclude_unset=True))
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.delete("/invoices/{invoice_id}")
async def delete_invoice(
    invoice_id: int,
    db: Session = Depends(get_db)
):
    """Delete invoice"""
    financial_service = FinancialService(db)
    success = financial_service.delete_invoice(invoice_id)
    if not success:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {"message": "Invoice deleted successfully"}


# Payment endpoints
@router.get("/payments/", response_model=List[Payment])
async def get_payments(
    skip: int = 0,
    limit: int = 100,
    invoice_id: int = None,
    db: Session = Depends(get_db)
):
    """Get all payments"""
    financial_service = FinancialService(db)
    payments = financial_service.get_payments(
        skip=skip, limit=limit, invoice_id=invoice_id
    )
    return payments


@router.post("/payments/", response_model=Payment)
async def create_payment(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db)
):
    """Create new payment"""
    financial_service = FinancialService(db)
    payment = financial_service.create_payment(payment_data.dict())
    return payment


# Chart of Accounts endpoints
@router.get("/chart-of-accounts/", response_model=List[ChartOfAccounts])
async def get_chart_of_accounts(
    skip: int = 0,
    limit: int = 100,
    account_type: str = None,
    db: Session = Depends(get_db)
):
    """Get chart of accounts"""
    financial_service = FinancialService(db)
    accounts = financial_service.get_chart_of_accounts(
        skip=skip, limit=limit, account_type=account_type
    )
    return accounts


@router.post("/chart-of-accounts/", response_model=ChartOfAccounts)
async def create_chart_of_account(
    account_data: ChartOfAccountsCreate,
    db: Session = Depends(get_db)
):
    """Create new chart of account"""
    financial_service = FinancialService(db)
    account = financial_service.create_chart_of_account(account_data.dict())
    return account


# General Ledger endpoints
@router.get("/general-ledger/", response_model=List[GeneralLedger])
async def get_general_ledger(
    skip: int = 0,
    limit: int = 100,
    account_id: int = None,
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db)
):
    """Get general ledger entries"""
    financial_service = FinancialService(db)
    entries = financial_service.get_general_ledger(
        skip=skip, limit=limit, account_id=account_id,
        start_date=start_date, end_date=end_date
    )
    return entries


@router.post("/general-ledger/", response_model=GeneralLedger)
async def create_general_ledger_entry(
    entry_data: GeneralLedgerCreate,
    db: Session = Depends(get_db)
):
    """Create new general ledger entry"""
    financial_service = FinancialService(db)
    entry = financial_service.create_general_ledger_entry(entry_data.dict())
    return entry


# Bank Reconciliation endpoints
@router.get("/bank-reconciliations/", response_model=List[BankReconciliation])
async def get_bank_reconciliations(
    skip: int = 0,
    limit: int = 100,
    bank_account_id: int = None,
    db: Session = Depends(get_db)
):
    """Get bank reconciliations"""
    financial_service = FinancialService(db)
    reconciliations = financial_service.get_bank_reconciliations(
        skip=skip, limit=limit, bank_account_id=bank_account_id
    )
    return reconciliations


@router.post("/bank-reconciliations/", response_model=BankReconciliation)
async def create_bank_reconciliation(
    reconciliation_data: BankReconciliationCreate,
    db: Session = Depends(get_db)
):
    """Create new bank reconciliation"""
    financial_service = FinancialService(db)
    reconciliation = financial_service.create_bank_reconciliation(reconciliation_data.dict())
    return reconciliation
