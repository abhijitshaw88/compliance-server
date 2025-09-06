"""
Financial service for business logic
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import datetime, date
from decimal import Decimal

from app.models.financial import (
    Invoice, InvoiceItem, Payment, ChartOfAccounts, 
    GeneralLedger, BankReconciliation
)
from app.schemas.financial import (
    InvoiceCreate, InvoiceUpdate, PaymentCreate, PaymentUpdate,
    ChartOfAccountsCreate, GeneralLedgerCreate, BankReconciliationCreate
)


class FinancialService:
    """Financial service class"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # Invoice methods
    def get_invoice(self, invoice_id: int) -> Optional[Invoice]:
        """Get invoice by ID"""
        return self.db.query(Invoice).filter(Invoice.id == invoice_id).first()
    
    def get_invoices(self, skip: int = 0, limit: int = 100, 
                    client_id: int = None, status: str = None) -> List[Invoice]:
        """Get all invoices with filters"""
        query = self.db.query(Invoice)
        
        if client_id:
            query = query.filter(Invoice.client_id == client_id)
        if status:
            query = query.filter(Invoice.status == status)
        
        return query.offset(skip).limit(limit).all()
    
    def create_invoice(self, invoice_data: dict) -> Invoice:
        """Create new invoice"""
        # Generate invoice number if not provided
        if not invoice_data.get("invoice_number"):
            invoice_data["invoice_number"] = self._generate_invoice_number()
        
        # Calculate totals
        items = invoice_data.pop("items", [])
        subtotal = sum(item["total_price"] for item in items)
        tax_amount = sum(item.get("tax_rate", 0) * item["total_price"] / 100 for item in items)
        total_amount = subtotal + tax_amount
        
        invoice_data.update({
            "subtotal": subtotal,
            "tax_amount": tax_amount,
            "total_amount": total_amount
        })
        
        # Create invoice
        invoice = Invoice(**invoice_data)
        self.db.add(invoice)
        self.db.commit()
        self.db.refresh(invoice)
        
        # Create invoice items
        for item_data in items:
            item_data["invoice_id"] = invoice.id
            item = InvoiceItem(**item_data)
            self.db.add(item)
        
        self.db.commit()
        return invoice
    
    def update_invoice(self, invoice_id: int, invoice_data: dict) -> Optional[Invoice]:
        """Update invoice"""
        invoice = self.get_invoice(invoice_id)
        if not invoice:
            return None
        
        # Update fields
        for field, value in invoice_data.items():
            if hasattr(invoice, field):
                setattr(invoice, field, value)
        
        invoice.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(invoice)
        return invoice
    
    def delete_invoice(self, invoice_id: int) -> bool:
        """Delete invoice"""
        invoice = self.get_invoice(invoice_id)
        if not invoice:
            return False
        
        # Delete related items first
        self.db.query(InvoiceItem).filter(InvoiceItem.invoice_id == invoice_id).delete()
        
        self.db.delete(invoice)
        self.db.commit()
        return True
    
    # Payment methods
    def get_payments(self, skip: int = 0, limit: int = 100, 
                    invoice_id: int = None) -> List[Payment]:
        """Get all payments with filters"""
        query = self.db.query(Payment)
        
        if invoice_id:
            query = query.filter(Payment.invoice_id == invoice_id)
        
        return query.offset(skip).limit(limit).all()
    
    def create_payment(self, payment_data: dict) -> Payment:
        """Create new payment"""
        payment = Payment(**payment_data)
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        
        # Update invoice status if fully paid
        self._update_invoice_payment_status(payment.invoice_id)
        
        return payment
    
    # Chart of Accounts methods
    def get_chart_of_accounts(self, skip: int = 0, limit: int = 100, 
                             account_type: str = None) -> List[ChartOfAccounts]:
        """Get chart of accounts with filters"""
        query = self.db.query(ChartOfAccounts)
        
        if account_type:
            query = query.filter(ChartOfAccounts.account_type == account_type)
        
        return query.offset(skip).limit(limit).all()
    
    def create_chart_of_account(self, account_data: dict) -> ChartOfAccounts:
        """Create new chart of account"""
        account = ChartOfAccounts(**account_data)
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account
    
    # General Ledger methods
    def get_general_ledger(self, skip: int = 0, limit: int = 100,
                          account_id: int = None, start_date: str = None,
                          end_date: str = None) -> List[GeneralLedger]:
        """Get general ledger entries with filters"""
        query = self.db.query(GeneralLedger)
        
        if account_id:
            query = query.filter(GeneralLedger.account_id == account_id)
        if start_date:
            query = query.filter(GeneralLedger.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(GeneralLedger.date <= datetime.fromisoformat(end_date))
        
        return query.offset(skip).limit(limit).all()
    
    def create_general_ledger_entry(self, entry_data: dict) -> GeneralLedger:
        """Create new general ledger entry"""
        entry = GeneralLedger(**entry_data)
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry
    
    # Bank Reconciliation methods
    def get_bank_reconciliations(self, skip: int = 0, limit: int = 100,
                                bank_account_id: int = None) -> List[BankReconciliation]:
        """Get bank reconciliations with filters"""
        query = self.db.query(BankReconciliation)
        
        if bank_account_id:
            query = query.filter(BankReconciliation.bank_account_id == bank_account_id)
        
        return query.offset(skip).limit(limit).all()
    
    def create_bank_reconciliation(self, reconciliation_data: dict) -> BankReconciliation:
        """Create new bank reconciliation"""
        reconciliation = BankReconciliation(**reconciliation_data)
        self.db.add(reconciliation)
        self.db.commit()
        self.db.refresh(reconciliation)
        return reconciliation
    
    def _generate_invoice_number(self) -> str:
        """Generate unique invoice number"""
        today = date.today()
        year = today.year
        month = today.month
        
        # Get count of invoices for current month
        count = self.db.query(Invoice).filter(
            and_(
                Invoice.created_at >= datetime(year, month, 1),
                Invoice.created_at < datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
            )
        ).count()
        
        return f"INV-{year}{month:02d}-{count + 1:04d}"
    
    def _update_invoice_payment_status(self, invoice_id: int):
        """Update invoice payment status based on payments"""
        invoice = self.get_invoice(invoice_id)
        if not invoice:
            return
        
        total_paid = sum(payment.amount for payment in invoice.payments 
                        if payment.status == "completed")
        
        if total_paid >= invoice.total_amount:
            invoice.status = "paid"
        elif total_paid > 0:
            invoice.status = "partially_paid"
        else:
            invoice.status = "unpaid"
        
        self.db.commit()
