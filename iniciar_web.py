#!/usr/bin/env python3
"""
Script para iniciar la aplicación web del Sistema de Emails Masivos
"""

import os
import sys
import subprocess
import webbrowser
import time

def check_dependencies():
    """Verificar que las dependencias estén instaladas"""
    required_packages = [
        'flask',
        'flask-sqlalchemy', 
        'werkzeug',
        'exchangelib',
        'pandas',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Faltan dependencias:")
        for package in missing_packages:
            print(f"   - {package}")
        
        print("\n🔧 Instalando dependencias faltantes...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ Dependencias instaladas correctamente")
        except subprocess.CalledProcessError:
            print("❌ Error al instalar dependencias")
            print("Ejecuta manualmente: pip install -r requirements.txt")
            return False
    
    return True

def create_directories():
    """Crear directorios necesarios"""
    directories = ['templates', 'static', 'logs']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Directorio creado: {directory}")

def main():
    """Función principal"""
    print("🚀 Sistema de Emails Masivos - Versión Web")
    print("=" * 50)
    
    # Verificar dependencias
    if not check_dependencies():
        return
    
    # Crear directorios
    create_directories()
    
    # Verificar que app.py existe
    if not os.path.exists('app.py'):
        print("❌ Error: No se encontró app.py")
        print("Asegúrate de estar en el directorio correcto")
        return
    
    print("\n🌐 Iniciando aplicación web...")
    print("📝 La aplicación estará disponible en: http://localhost:5000")
    print("🔄 Presiona Ctrl+C para detener la aplicación")
    print("\n" + "=" * 50)
    
    # Abrir navegador después de un delay
    def open_browser():
        time.sleep(3)
        try:
            webbrowser.open('http://localhost:5000')
        except:
            pass
    
    # Iniciar navegador en background
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Iniciar aplicación Flask
    try:
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n\n🛑 Aplicación detenida por el usuario")
    except Exception as e:
        print(f"\n❌ Error al iniciar la aplicación: {e}")

if __name__ == '__main__':
    main()
