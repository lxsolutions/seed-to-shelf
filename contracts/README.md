









# S2S Contracts

Shared API and event schemas for Seed-to-Shelf (S2S) and ChefGrid (CG) interoperability.

## Overview

This directory contains the shared contracts between:
- **seed-to-shelf**: Agri automation, processing, and distribution
- **chefgrid**: Consumer-facing chef marketplace platform

## Contents

### Events (`/events`)
- `asyncapi.yaml`: Event schema definitions for async communication
- Topics covered: supply chain events, order status changes, menu updates

### Schemas (`/schemas/json`)
- JSON Schema definitions for shared data models:
  - Lot tracking (FSMA 204 compliance)
  - Ready meals and kits
  - Order status changes
  - Menu dishes

### Type Definitions
- **TypeScript**: Zod schemas in `/typescript/index.ts`
- **Python**: Pydantic models in `/python/pydantic_models.py`

## Usage

1. Install the package from npm or PyPI:
   ```bash
   # For JavaScript/TypeScript projects
   npm install @s2s/contracts

   # For Python projects
   pip install s2s-contracts
   ```

2. Import and use the schemas in your project:

```typescript
// TypeScript example
import { z } from 'zod';
import * as contracts from '@s2s/contracts';

const lotSchema = contracts.lot;
```

```python
# Python example
from s2s_contracts import Lot

lot_data = {"id": "123", "product_code": "ORGANIC_TOMATOES"}
lot = Lot(**lot_data)
```

## Development

### Publishing

Packages are published automatically on GitHub tags using semantic versioning.

```bash
# Example: Publish v0.1.0
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

## License

MIT









