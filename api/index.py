#!/usr/bin/env python3
"""
API Entry Point para Vercel - Versión Simplificada
Sistema de Emails Masivos Heliopsis
"""

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 Sistema de Emails Masivos Heliopsis - ¡Funcionando en Vercel!"

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "message": "API funcionando"})

@app.route('/api')
def api():
    return jsonify({
        "name": "Sistema de Emails Masivos Heliopsis",
        "version": "2.0.0",
        "status": "operational"
    })

# Exportar para Vercel
handler = app
