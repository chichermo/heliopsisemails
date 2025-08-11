#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PRUEBA DE INTEGRACIÓN SENDGRID CON APLICACIÓN
=============================================

Este script prueba que SendGrid esté correctamente integrado
con la aplicación Flask y pueda enviar emails reales.
"""

import sys
import os

# Agregar el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sendgrid_sender import SendGridSender
from config_sendgrid_app import SendGridConfig

def probar_sendgrid_integrado():
    """Probar que SendGrid esté funcionando correctamente"""
    
    print("🧪 PRUEBA DE INTEGRACIÓN SENDGRID CON APLICACIÓN")
    print("=" * 50)
    
    try:
        # Validar configuración
        print("1️⃣ Validando configuración...")
        SendGridConfig.validate_config()
        print("✅ Configuración válida")
        
        # Probar conexión
        print("\n2️⃣ Probando conexión con SendGrid...")
        sender = SendGridSender()
        if sender.test_connection():
            print("✅ Conexión exitosa con SendGrid")
        else:
            print("❌ Error de conexión con SendGrid")
            return False
        
        # Probar envío de email
        print("\n3️⃣ Probando envío de email...")
        test_emails = [
            {'email': 'el_chicher@hotmail.com', 'name': 'El Chicher'}
        ]
        
        test_template = """
        <html>
        <body>
            <h2>¡Hola {{name}}!</h2>
            <p>Este es un email de prueba de la integración con SendGrid.</p>
            <p>✅ Si recibes este email, significa que tu aplicación web</p>
            <p>   ya puede enviar emails REALES usando SendGrid!</p>
            <br>
            <p>Saludos,<br>Sistema de Emails Integrado</p>
        </body>
        </html>
        """
        
        results = sender.send_bulk_emails(
            test_emails,
            "Prueba de Integración - SendGrid Funcionando",
            test_template,
            "El Chicher",
            "el_chicher@hotmail.com"
        )
        
        print(f"📊 Resultados del envío:")
        print(f"   • Total: {results['total']}")
        print(f"   • Enviados: {results['sent']}")
        print(f"   • Fallidos: {results['failed']}")
        
        if results['sent'] > 0:
            print("\n🎉 ¡INTEGRACIÓN EXITOSA!")
            print("✅ Tu aplicación web ahora puede enviar emails REALES")
            print("✅ No más modo de prueba - emails reales a través de SendGrid")
            print("✅ Límite: 100 emails gratis por día")
            return True
        else:
            print("\n❌ Error en el envío de emails")
            return False
            
    except Exception as e:
        print(f"\n❌ Error durante la prueba: {e}")
        return False

def mostrar_estado_actual():
    """Mostrar el estado actual del sistema"""
    
    print("\n📊 ESTADO ACTUAL DEL SISTEMA:")
    print("=" * 30)
    
    # Verificar archivos
    archivos = [
        'sendgrid_sender.py',
        'config_sendgrid_app.py',
        'app.py'
    ]
    
    for archivo in archivos:
        if os.path.exists(archivo):
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo}")
    
    print(f"\n🔧 CONFIGURACIÓN:")
    print(f"   • API Key: {'✅ Configurada' if SendGridConfig.SENDGRID_API_KEY else '❌ No configurada'}")
    print(f"   • Email remitente: {SendGridConfig.SENDER_EMAIL}")
    print(f"   • Nombre remitente: {SendGridConfig.SENDER_NAME}")

def main():
    """Función principal"""
    
    print("🚀 SISTEMA DE INTEGRACIÓN SENDGRID")
    print("=" * 40)
    
    # Mostrar estado
    mostrar_estado_actual()
    
    # Probar integración
    if probar_sendgrid_integrado():
        print("\n🎯 PRÓXIMOS PASOS:")
        print("1. Ejecuta tu aplicación Flask: python app.py")
        print("2. Ve a la interfaz web")
        print("3. Crea una campaña y envíala")
        print("4. Los emails se enviarán REALMENTE usando SendGrid")
    else:
        print("\n❌ La integración no está funcionando correctamente")
        print("   Revisa la configuración y vuelve a intentar")

if __name__ == "__main__":
    main()
