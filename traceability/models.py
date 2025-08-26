










import datetime
from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ComplianceEvent(Base):
    """FSMA 204 Key Data Element tracking"""
    __tablename__ = 'compliance_events'

    id = Column(Integer, primary_key=True)
    entity_ref = Column(String(50), nullable=False)  # e.g., "lot:123", "order:456"
    cte_type = Column(String(20), nullable=False)   # Receive/Transform/Ship
    data = Column(JSON, nullable=False)             # KDE payload
    ts = Column(DateTime, default=datetime.datetime.utcnow)

class LotLineage(Base):
    """Lot lineage graph for traceability"""
    __tablename__ = 'lot_lineage'

    id = Column(Integer, primary_key=True)
    lot_code = Column(String(50), unique=True, nullable=False)  # GS1-like format
    parent_lot_codes = Column(JSON, default=[])   # For Transform CTEs
    child_lot_codes = Column(JSON, default=[])   # For Transform CTEs
    order_ids = Column(JSON, default=[])         # Orders this lot contributed to

class TraceabilityConfig(Base):
    """Configuration for traceability settings"""
    __tablename__ = 'traceability_config'

    id = Column(Integer, primary_key=True)
    key = Column(String(50), unique=True, nullable=False)  # e.g., "retention_period_days"
    value = Column(JSON, nullable=False)

# Pydantic models for API requests/responses
from typing import Optional, Literal, Union, Annotated
from pydantic import BaseModel, Field

class CTEDataBase(BaseModel):
    """Base model for Common Traceability Element (CTE) data."""
    timestamp: str  # ISO format timestamp

class ReceiveCTEData(CTEDataBase):
    """Data model for Receive CTE events."""
    quantity: float
    location: str
    supplier_lot_code: Optional[str] = None

class TransformCTEData(CTEDataBase):
    """Data model for Transform CTE events."""
    input_lots: list[str]
    output_lot: str
    process_description: str

class ShipCTEData(CTEDataBase):
    """Data model for Ship CTE events."""
    quantity_shipped: float
    destination_location: str
    carrier: Optional[str] = None

# Union type for all possible CTE data payloads
CTEPayloadUnion = Annotated[Union[
    ReceiveCTEData,
    TransformCTEData,
    ShipCTEData
], Field(discriminator='cte_type')]

class ComplianceEventCreate(BaseModel):
    """Request model for creating compliance events."""
    entity_ref: str  # e.g., "lot-12345", "order-67890"
    cte_type: Literal["Receive", "Transform", "Ship"]
    data: CTEPayloadUnion

    class Config:
        schema_extra = {
            "example": {
                "entity_ref": "lot-12345",
                "cte_type": "Receive",
                "data": {
                    "timestamp": "2025-08-25T12:00:00Z",
                    "quantity": 10,
                    "location": "Kitchen A"
                }
            }
        }

class LotInfoResponse(BaseModel):
    """Response model for lot information."""
    lot_code: str
    parent_lots: list[str]
    child_lots: list[str]
    order_references: list[str]

    class Config:
        schema_extra = {
            "example": {
                "lot_code": "lot-12345",
                "parent_lots": ["batch-xyz"],
                "child_lots": [],
                "order_references": ["order-67890"]
            }
        }

class BacktraceResponse(BaseModel):
    """Response model for order backtrace."""
    order_id: str
    lot_lineage: list[dict]

    class Config:
        schema_extra = {
            "example": {
                "order_id": "order-12345",
                "lot_lineage": [
                    {"step": "Harvest", "description": "Farm batch XYZ"},
                    {"step": "Receive", "location": "Kitchen 123"},
                    {"step": "Transform", "dish": "Salad with farm-fresh greens"}
                ]
            }
        }








