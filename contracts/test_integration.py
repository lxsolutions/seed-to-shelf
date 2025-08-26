

#!/usr/bin/env python3
"""
Integration test for S2S contracts package.
Tests both Python and TypeScript imports work correctly.
"""

import subprocess
import sys

# Add the current directory to Python path so we can import from editable install
sys.path.insert(0, '/workspace/seed-to-shelf/contracts/python')

def test_python_imports():
    """Test that Python models can be imported and used."""
    print("Testing Python imports...")

    try:
        # Import directly from the module file since package may not be installed globally
        import pydantic_models

        print("✓ Successfully imported all Python models")

        # Test creating instances
        ingredient = pydantic_models.Ingredient(
            name="Tomato",
            lot_id="123e4567-e89b-12d3-a456-426614174000",
            quantity=10
        )

        meal = pydantic_models.ReadyMeal(
            product_id="123e4567-e89b-12d3-a456-426614174000",
            name="Spaghetti Bolognese",
            sku="SKU12345",
            ingredients=[ingredient],
            price=9.99
        )

        lot = pydantic_models.LotCreate(
            lot_id="123e4567-e89b-12d3-a456-426614174000",
            product_name="Tomatoes",
            quantity=100,
            batch_id="batch123"
        )

        status_change = pydantic_models.OrderStatusChange(
            order_id="123e4567-e89b-12d3-a456-426614174000",
            status="DELIVERED"
        )

        print("✓ Successfully created model instances")
        return True

    except ImportError as e:
        print(f"✗ Python import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Python model creation failed: {e}")
        return False

def test_typescript_imports():
    """Test that TypeScript models can be imported and used."""
    print("Testing TypeScript imports...")

    try:
        # Test Node.js import
        result = subprocess.run([
            "node", "-e",
            "const { Ingredient, ReadyMeal } = require('./dist/index'); "
            "console.log('TypeScript imports successful')"
        ], cwd="/workspace/seed-to-shelf/contracts", capture_output=True, text=True)

        if result.returncode == 0:
            print("✓ TypeScript imports work correctly")
            return True
        else:
            print(f"✗ TypeScript import failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"✗ TypeScript test execution failed: {e}")
        return False

def main():
    """Run all integration tests."""
    print("Running S2S Contracts Integration Tests")
    print("=" * 50)

    python_success = test_python_imports()
    typescript_success = test_typescript_imports()

    print("\n" + "=" * 50)
    if python_success and typescript_success:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
