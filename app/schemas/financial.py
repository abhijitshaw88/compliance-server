"""
Financial-related Pydantic schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, date
from decimal import Decimal
from app.models.financial import InvoiceStatus, PaymentStatus

# Forward reference for Payment class


class ClientBase(BaseModel):
    """Base client schema"""
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    gstin: Optional[str] = None
    pan: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    assigned_user_id: Optional[int] = None


class ClientCreate(ClientBase):
    """Schema for creating a client"""
    pass


class ClientUpdate(BaseModel):
    """Schema for updating a client"""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    gstin: Optional[str] = None
    pan: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    assigned_user_id: Optional[int] = None
    status: Optional[str] = None


class Client(ClientBase):
    """Schema for client response"""
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChartOfAccountsBase(BaseModel):
    """Base chart of accounts schema"""
    code: str
    name: str
    account_type: str
    parent_id: Optional[int] = None
    is_active: bool = True


class ChartOfAccountsCreate(ChartOfAccountsBase):
    """Schema for creating chart of accounts"""
    pass


class ChartOfAccounts(ChartOfAccountsBase):
    """Schema for chart of accounts response"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class GeneralLedgerBase(BaseModel):
    """Base general ledger schema"""
    account_id: int
    transaction_id: str
    date: datetime
    description: Optional[str] = None
    debit_amount: Decimal = Field(default=0, decimal_places=2)
    credit_amount: Decimal = Field(default=0, decimal_places=2)
    balance: Decimal = Field(default=0, decimal_places=2)
    reference: Optional[str] = None


class GeneralLedgerCreate(GeneralLedgerBase):
    """Schema for creating general ledger entry"""
    pass


class GeneralLedger(GeneralLedgerBase):
    """Schema for general ledger response"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class InvoiceItemBase(BaseModel):
    """Base invoice item schema"""
    description: str
    quantity: Decimal = Field(decimal_places=2)
    unit_price: Decimal = Field(decimal_places=2)
    total_price: Decimal = Field(decimal_places=2)
    tax_rate: Decimal = Field(default=0, decimal_places=2)


class InvoiceItemCreate(InvoiceItemBase):
    """Schema for creating invoice item"""
    pass


class InvoiceItem(InvoiceItemBase):
    """Schema for invoice item response"""
    id: int
    invoice_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class InvoiceBase(BaseModel):
    """Base invoice schema"""
    invoice_number: str
    client_id: int
    issue_date: datetime
    due_date: datetime
    subtotal: Decimal = Field(decimal_places=2)
    tax_amount: Decimal = Field(default=0, decimal_places=2)
    total_amount: Decimal = Field(decimal_places=2)
    notes: Optional[str] = None


class InvoiceCreate(InvoiceBase):
    """Schema for creating an invoice"""
    items: List[InvoiceItemCreate] = []


class InvoiceUpdate(BaseModel):
    """Schema for updating an invoice"""
    invoice_number: Optional[str] = None
    issue_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    subtotal: Optional[Decimal] = None
    tax_amount: Optional[Decimal] = None
    total_amount: Optional[Decimal] = None
    status: Optional[InvoiceStatus] = None
    notes: Optional[str] = None


class PaymentBase(BaseModel):
    """Base payment schema"""
    invoice_id: int
    amount: Decimal = Field(decimal_places=2)
    payment_date: datetime
    payment_method: str
    reference: Optional[str] = None
    notes: Optional[str] = None


class PaymentCreate(PaymentBase):
    """Schema for creating a payment"""
    pass


class PaymentUpdate(BaseModel):
    """Schema for updating a payment"""
    amount: Optional[Decimal] = None
    payment_date: Optional[datetime] = None
    payment_method: Optional[str] = None
    reference: Optional[str] = None
    status: Optional[PaymentStatus] = None
    notes: Optional[str] = None


class Payment(PaymentBase):
    """Schema for payment response"""
    id: int
    status: PaymentStatus
    created_at: datetime

    class Config:
        from_attributes = True


class Invoice(InvoiceBase):
    """Schema for invoice response"""
    id: int
    status: InvoiceStatus
    created_at: datetime
    updated_at: datetime
    items: List[InvoiceItem] = []
    payments: List[Payment] = []

    class Config:
        from_attributes = True


class BankReconciliationBase(BaseModel):
    """Base bank reconciliation schema"""
    bank_account_id: int
    statement_date: datetime
    opening_balance: Decimal = Field(decimal_places=2)
    closing_balance: Decimal = Field(decimal_places=2)


class BankReconciliationCreate(BankReconciliationBase):
    """Schema for creating bank reconciliation"""
    pass


class BankReconciliation(BankReconciliationBase):
    """Schema for bank reconciliation response"""
    id: int
    is_reconciled: bool
    reconciled_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
