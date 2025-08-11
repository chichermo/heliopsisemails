#!/usr/bin/env python3
"""
API Entry Point para Vercel - Versión Simplificada
Sistema de Emails Masivos Heliopsis
"""

from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Heliopsis Email System</title>
            <meta charset="UTF-8">
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
                .container { max-width: 800px; margin: 0 auto; background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; backdrop-filter: blur(10px); }
                h1 { text-align: center; color: #fff; margin-bottom: 30px; }
                .feature { background: rgba(255,255,255,0.2); padding: 20px; margin: 15px 0; border-radius: 10px; }
                .status { background: #4CAF50; color: white; padding: 10px; border-radius: 5px; text-align: center; margin: 20px 0; }
                .button { background: #2196F3; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px; }
                .button:hover { background: #1976D2; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Heliopsis Email System</h1>
                
                <div class="status">
                    ✅ Sistema funcionando correctamente en Vercel
                </div>
                
                <div class="feature">
                    <h3>📧 Envío de Emails Profesionales</h3>
                    <p>Sistema completo de envío de emails usando Twilio SendGrid con templates personalizables y manejo de listas grandes.</p>
                </div>
                
                <div class="feature">
                    <h3>🎨 Templates Simplificados</h3>
                    <p>Creación de templates sin necesidad de conocimientos HTML. Sistema intuitivo para usuarios no técnicos.</p>
                </div>
                
                <div class="feature">
                    <h3>📊 Gestión Avanzada de Contactos</h3>
                    <p>Manejo de listas de 100+ emails con categorización, validación y procesamiento por lotes.</p>
                </div>
                
                <div class="feature">
                    <h3>🔒 Headers Profesionales</h3>
                    <p>Configuración optimizada para evitar spam y mejorar la entregabilidad en emails corporativos.</p>
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="https://github.com/chichermo/heliopsisemails" class="button">📁 Ver en GitHub</a>
                    <a href="mailto:heliopsis@outlook.be" class="button">📧 Contactar</a>
                </div>
                
                <div style="text-align: center; margin-top: 20px; font-size: 12px; opacity: 0.8;">
                    Sistema desarrollado por Heliopsis - Desplegado en Vercel
                </div>
            </div>
        </body>
        </html>
        """
        
        self.wfile.write(html_content.encode())
    
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "status": "success",
            "message": "Heliopsis Email System API funcionando correctamente",
            "version": "2.0.0",
            "features": [
                "SendGrid Integration",
                "Template Management",
                "Contact Lists",
                "Professional Headers"
            ]
        }
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
