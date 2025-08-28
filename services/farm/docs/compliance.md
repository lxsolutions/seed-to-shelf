





# Seed to Chef Compliance Framework

## Overview

The Seed to Chef platform is designed with food safety and regulatory compliance at its core. This document outlines the technical implementation of our compliance system, which ensures adherence to FSMA 204 traceability requirements and local jurisdiction regulations.

## Key Data Elements (KDE) Tracking

### Core KDEs Recorded for Each Transaction

1. **Lot Code**: Unique identifier following GS1 standards
2. **Quantity**: Amount transferred in each transaction
3. **Location**: Geographic coordinates or address where the transaction occurred
4. **Timestamp**: Precise date and time of the transaction
5. **Transaction References**: Links to related transactions (e.g., farm batch ID, order ID)

### Critical Tracking Events (CTEs) Implemented

| CTE Type | Description | Implementation Location |
|----------|-------------|------------------------|
| RECEIVE  | Transfer from farm to inventory | `/services/api/inventory` |
| TRANSFORM | Conversion of ingredients into dishes | `/services/api/dishes` |
| SHIP     | Delivery from kitchen to consumer | `/services/logistics` |

## Jurisdiction-Specific Rules Engine

### Rule Structure

Each jurisdiction rule is defined in JSON format and stored in `/services/api/compliance/rules/`:

```json
{
  "jurisdiction_code": "CA_SAN_MATEO_MEHKO",
  "name": "San Mateo County MEHKO Permit",
  "description": "Rules for home kitchens operating under MEHKO permit",
  "rules": [
    {
      "type": "kitchen_type_allowance",
      "value": ["HOME"],
      "message": "Only HOME kitchens are allowed"
    },
    {
      "type": "permit_requirement",
      "value": true,
      "message": "MEHKO permit is required for hot food sales"
    },
    {
      "type": "delivery_restriction",
      "boundary_type": "county",
      "boundary_id": "CA_SAN_MATEO",
      "message": "Delivery restricted to San Mateo County boundaries"
    }
  ]
}
```

### Rule Types

| Rule Type | Description |
|-----------|-------------|
| `kitchen_type_allowance` | Specifies which kitchen types (HOME/COMMERCIAL) are permitted |
| `permit_requirement` | Indicates if a specific permit is required |
| `delivery_restriction` | Defines geographic boundaries for sales/delivery |
| `food_type_restriction` | Limits the types of foods that can be sold (e.g., TCS vs non-TCS) |
| `labeling_requirement` | Specifies labeling templates for cottage food items |

## Implementation Details

### Middleware Validation

The compliance middleware validates transactions against jurisdiction rules:

```python
from fastapi import Request, HTTPException
from src.compliance.rules_engine import RulesEngine

async def validate_jurisdiction(request: Request):
    chef = request.state.chef
    consumer_location = await get_consumer_location(request)

    # Get applicable rules based on chef's location
    rules = await RulesEngine.get_rules_for_jurisdiction(chef.location)

    # Validate kitchen type and permits
    if not rules.validate_kitchen_type(chef.kitchen.type):
        raise HTTPException(
            status_code=403,
            detail="This jurisdiction does not allow your kitchen type"
        )

    # Check delivery boundaries
    if not rules.validate_delivery_boundary(consumer_location, chef.location):
        raise HTTPException(
            status_code=403,
            detail="Delivery outside allowed jurisdiction boundary"
        )
```

### Lot Lineage Graph

The traceability service maintains a graph of lot lineage for complete backtracking:

```python
class LotLineageGraph:
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.nodes = []
        self.edges = []

    def add_receive_event(self, event_data: dict):
        """Add farm-to-inventory transfer"""
        node_id = f"receive_{event_data['lot_code']}"
        self.nodes.append({
            "id": node_id,
            "type": "RECEIVE",
            "data": event_data
        })

    def add_transform_event(self, event_data: dict):
        """Add ingredient-to-dish conversion"""
        input_lots = [f"receive_{lot}" for lot in event_data['input_lots']]
        output_node = f"transform_{event_data['dish_id']}"
        self.nodes.append({
            "id": output_node,
            "type": "TRANSFORM",
            "data": event_data
        })
        # Create edges from input lots to this transformation
        for input_lot in input_lots:
            self.edges.append({"source": input_lot, "target": output_node})

    def add_ship_event(self, event_data: dict):
        """Add dish-to-consumer delivery"""
        dish_node = f"transform_{event_data['dish_id']}"
        ship_node = f"ship_{self.order_id}"
        self.nodes.append({
            "id": ship_node,
            "type": "SHIP",
            "data": event_data
        })
        self.edges.append({"source": dish_node, "target": ship_node})

    def get_graph(self):
        return {
            "nodes": self.nodes,
            "links": self.edges
        }
```

## API Endpoints

### Traceability APIs

| Endpoint | Description |
|----------|-------------|
| `GET /trace/backtrace?order_id={id}` | Returns complete lineage graph for an order |
| `GET /trace/lot/{lot_code}` | Returns all transactions involving a specific lot code |

### Compliance APIs

| Endpoint | Description |
|----------|-------------|
| `POST /compliance/rules` | Admin endpoint to add/update jurisdiction rules |
| `GET /compliance/rules/{jurisdiction_code}` | Retrieve rules for a specific jurisdiction |

## Export Capabilities

For regulatory inspections, the platform provides:

1. **CSV/JSON Exports**: Downloadable reports of all KDEs and CTEs
2. **Audit Trails**: Immutable logs of all compliance events
3. **Graphical Visualization**: Interactive lot lineage graphs for inspectors

## Testing Strategy

### Automated Compliance Tests

```python
def test_jurisdiction_validation():
    # Test CA San Mateo MEHKO rules
    rule = load_rule("CA_SAN_MATEO_MEHKO")

    # Should allow HOME kitchen with permit
    assert rule.validate_kitchen_type("HOME") == True

    # Should block COMMERCIAL kitchen (MEHKO is for home kitchens only)
    assert rule.validate_kitchen_type("COMMERCIAL") == False

def test_cottage_food_restrictions():
    # Test CO Boulder cottage food rules
    rule = load_rule("CO_BOULDER_COTTAGE")

    # Should block TCS foods from HOME kitchens
    tcs_dish = {"risk_level": "HIGH", "required_temp_control": True}
    assert rule.validate_food_type(tcs_dish) == False

    # Should allow shelf-stable foods
    non_tcs_dish = {"risk_level": "LOW", "required_temp_control": False}
    assert rule.validate_food_type(non_tcs_dish) == True
```

### Manual Testing Scenarios

1. **Happy Path**: Consumer orders from MEHKO-approved chef in CA San Mateo
2. **Blocked Transaction**: Consumer attempts to order TCS food from cottage kitchen in CO Boulder
3. **Boundary Test**: Order delivery crossing county lines (should be blocked)
4. **Permit Verification**: Kitchen without proper permit cannot accept orders

## Future Enhancements

1. **Dynamic Rule Updates**: Real-time rule synchronization with regulatory databases
2. **AI-Powered Compliance Assistant**: Automated suggestion of correct jurisdiction codes based on location
3. **Blockchain Integration**: Immutable record-keeping for enhanced auditability
4. **International Expansion**: Support for global food safety regulations (e.g., EU FIR)

## Conclusion

The Seed to Chef compliance framework ensures that all transactions adhere to stringent food safety regulations while providing flexibility for different jurisdiction requirements. The system's modular design allows for easy addition of new rules and jurisdictions as the platform expands.

