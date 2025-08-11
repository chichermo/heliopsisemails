#!/usr/bin/env python3
"""
API Entry Point para Vercel - Versión Simplificada
Sistema de Emails Masivos Heliopsis
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 Sistema de Emails Masivos Heliopsis - ¡Funcionando en Vercel!"

@app.route('/health')
def health():
    return {"status": "healthy", "message": "API funcionando"}

# Exportar para Vercel
handler = app
