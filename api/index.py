#!/usr/bin/env python3
"""
API Entry Point para Vercel
Sistema de Emails Masivos Heliopsis
"""

import sys
import os

# Agregar el directorio padre al path para importar app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Para Vercel, necesitamos exportar la aplicación Flask
app.debug = False
app.config['TESTING'] = False

# Exportar la aplicación para Vercel
handler = app
