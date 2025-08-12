#!/usr/bin/env python3
"""
Ejecutar sistema de emails Heliopsis localmente
"""

import os
import sys

# Agregar el directorio actual al path
sys.path.append('.')

try:
    print("🚀 Iniciando Sistema de Emails Heliopsis...")
    print("📁 Directorio actual:", os.getcwd())
    
    # Importar y ejecutar la aplicación
    from vercel_app import app
    
    print("✅ Aplicación Flask cargada correctamente")
    print("🌐 Iniciando servidor en http://localhost:5000")
    print("🔄 Presiona Ctrl+C para detener")
    
    # Ejecutar la aplicación
    app.run(debug=True, host='0.0.0.0', port=5000)
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("🔍 Verificando archivos...")
    
    if not os.path.exists("vercel_app.py"):
        print("❌ vercel_app.py no existe")
    else:
        print("✅ vercel_app.py existe")
        
    if not os.path.exists("templates/"):
        print("❌ Directorio templates/ no existe")
    else:
        print("✅ Directorio templates/ existe")
        
    print("\n📋 Archivos en templates/:")
    if os.path.exists("templates/"):
        for file in os.listdir("templates/"):
            print(f"   - {file}")
            
except Exception as e:
    print(f"❌ Error general: {e}")
    import traceback
    traceback.print_exc()
