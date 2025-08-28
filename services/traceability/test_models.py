








"""
Test SQLAlchemy models for traceability service.
"""

import datetime
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Import our models
import models

def test_models():
    """Test that models can be instantiated and serialized."""
    print("Testing SQLAlchemy models...")

    # Test ComplianceEvent model
    event = models.ComplianceEvent(
        entity_ref="lot-12345",
        cte_type="Receive",
        data={
            "quantity": 10,
            "location": "Kitchen A",
            "timestamp": datetime.datetime.utcnow().isoformat()
        },
        ts=datetime.datetime.utcnow()
    )

    print(f"ComplianceEvent created: {event.entity_ref} ({event.cte_type})")
    print(f"Data: {event.data}")
    print(f"Timestamp: {event.ts}")

    # Test LotLineage model
    lineage = models.LotLineage(
        lot_code="lot-12345",
        parent_lot_codes=["batch-xyz"],
        child_lot_codes=[],
        order_ids=["order-67890"]
    )

    print(f"\nLotLineage created: {lineage.lot_code}")
    print(f"Parent lots: {lineage.parent_lot_codes}")
    print(f"Child lots: {lineage.child_lot_codes}")
    print(f"Order references: {lineage.order_ids}")

    # Test TraceabilityConfig model
    config = models.TraceabilityConfig(
        key="retention_period_days",
        value={"days": 365}
    )

    print(f"\nTraceabilityConfig created: {config.key} = {config.value}")

    print("\nAll models tested successfully!")

if __name__ == "__main__":
    test_models()





