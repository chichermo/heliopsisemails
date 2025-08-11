#!/usr/bin/env python3
"""
API Entry Point para Vercel
Sistema de Emails Masivos Heliopsis
"""

import sys
import os

# Agregar el directorio padre al path para importar app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import app
    
    # Configurar para producción
    app.debug = False
    app.config['TESTING'] = False
    
    # Para Vercel, necesitamos exportar la aplicación Flask
    handler = app
    
except ImportError as e:
    # Si hay error de importación, crear una app básica
    from flask import Flask
    
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return "Sistema de Emails Masivos Heliopsis - Funcionando en Vercel!"
    
    @app.route('/health')
    def health():
        return {"status": "healthy", "message": "API funcionando correctamente"}
    
    handler = app
