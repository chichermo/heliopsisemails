#!/usr/bin/env python3
"""
Test local server para verificar que la API funciona antes de desplegar en Vercel
"""

import http.server
import socketserver
import webbrowser
import os
import sys

# Importar la función handler de api/index.py
sys.path.append('api')
from index import handler

class TestServer(http.server.HTTPServer):
    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)
        print(f"🚀 Servidor local iniciado en http://{server_address[0]}:{server_address[1]}")
        print("📱 Abriendo navegador automáticamente...")
        webbrowser.open(f"http://{server_address[0]}:{server_address[1]}")

if __name__ == "__main__":
    PORT = 8000
    
    try:
        # Crear servidor con nuestro handler personalizado
        with TestServer(("localhost", PORT), handler) as httpd:
            print("✅ API funcionando correctamente!")
            print("🔄 Presiona Ctrl+C para detener el servidor")
            print("🌐 Abre http://localhost:8000 en tu navegador")
            
            # Mantener servidor corriendo
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error al iniciar servidor: {e}")
        print("🔍 Verificando archivos...")
        
        # Verificar que los archivos existen
        if not os.path.exists("api/index.py"):
            print("❌ api/index.py no existe")
        else:
            print("✅ api/index.py existe")
            
        if not os.path.exists("vercel.json"):
            print("❌ vercel.json no existe")
        else:
            print("✅ vercel.json existe")
