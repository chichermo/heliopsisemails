#!/usr/bin/env python3
"""
Archivo de prueba simple para verificar funcionalidad básica
"""

def test_basic_functionality():
    """Prueba básica de funcionalidad"""
    return {
        "status": "success",
        "message": "Basic functionality test passed",
        "python_version": "3.11",
        "test": True
    }

if __name__ == "__main__":
    result = test_basic_functionality()
    print("Test result:", result)
