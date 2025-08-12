#!/usr/bin/env python3
"""
Test de la versión simplificada
"""

import os
import sys

try:
    print("🚀 Probando versión simplificada...")
    
    # Importar la aplicación simplificada
    from vercel_app_simple import app
    
    print("✅ Aplicación simplificada cargada correctamente")
    print("🌐 Iniciando servidor en http://localhost:5000")
    print("🔄 Presiona Ctrl+C para detener")
    
    # Ejecutar la aplicación
    app.run(debug=True, host='0.0.0.0', port=5000)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
