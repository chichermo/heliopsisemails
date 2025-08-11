#!/usr/bin/env python3
"""
API Entry Point para Vercel - Versión Simplificada
Sistema de Emails Masivos Heliopsis
"""

from flask import Flask, jsonify

# Crear aplicación Flask básica
app = Flask(__name__)

@app.route('/')
def home():
    """Página principal"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sistema de Emails Masivos Heliopsis</title>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; }
            .status { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; }
            .features { background: #e2e3e5; padding: 20px; border-radius: 5px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Sistema de Emails Masivos Heliopsis</h1>
            <div class="status">
                <strong>✅ Estado:</strong> Aplicación funcionando correctamente en Vercel
            </div>
            <div class="features">
                <h3>🌟 Funcionalidades Disponibles:</h3>
                <ul>
                    <li>📧 Gestión de listas de emails</li>
                    <li>📝 Sistema de plantillas HTML</li>
                    <li>📊 Campañas masivas</li>
                    <li>📈 Dashboard con estadísticas</li>
                    <li>🔧 Configuración avanzada</li>
                </ul>
            </div>
            <p><strong>URL de la API:</strong> <code>/api</code></p>
            <p><strong>Estado de salud:</strong> <code>/health</code></p>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    """Endpoint de verificación de salud"""
    return jsonify({
        "status": "healthy",
        "message": "Sistema de Emails Masivos Heliopsis funcionando correctamente",
        "version": "2.0.0",
        "platform": "Vercel"
    })

@app.route('/api')
def api_info():
    """Información de la API"""
    return jsonify({
        "name": "Sistema de Emails Masivos Heliopsis",
        "version": "2.0.0",
        "endpoints": [
            "/",
            "/health",
            "/api"
        ],
        "status": "operational"
    })

@app.route('/favicon.ico')
def favicon():
    """Servir favicon"""
    return app.send_static_file('favicon.ico')

# Para Vercel, necesitamos exportar la aplicación Flask
handler = app

# Configuración para producción
app.debug = False
app.config['TESTING'] = False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
