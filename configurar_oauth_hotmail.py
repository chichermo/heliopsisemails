#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CONFIGURACIÓN OAUTH2 PARA HOTMAIL/OUTLOOK
==========================================

Microsoft ha deshabilitado la autenticación básica para Hotmail/Outlook.
Necesitamos usar OAuth2 para que funcione.

PASOS PARA CONFIGURAR:
1. Ir a https://portal.azure.com
2. Crear una nueva aplicación
3. Configurar permisos para Microsoft Graph
4. Obtener Client ID y Client Secret
5. Configurar redirect URI
6. Generar token de acceso

ALTERNATIVA MÁS SIMPLE:
Usar una cuenta de Gmail que sí permite autenticación básica
"""

import os
import json
from datetime import datetime, timedelta

def mostrar_instrucciones_oauth():
    """Mostrar instrucciones detalladas para configurar OAuth2"""
    
    print("🔐 CONFIGURACIÓN OAUTH2 PARA HOTMAIL/OUTLOOK")
    print("=" * 60)
    print()
    print("❌ PROBLEMA IDENTIFICADO:")
    print("   Microsoft ha deshabilitado la autenticación básica")
    print("   para Hotmail/Outlook. El error 'basic authentication is disabled'")
    print("   confirma esto.")
    print()
    print("✅ SOLUCIONES DISPONIBLES:")
    print()
    print("1️⃣ CONFIGURAR OAUTH2 (COMPLEJO):")
    print("   • Crear aplicación en Azure Portal")
    print("   • Configurar permisos Microsoft Graph")
    print("   • Obtener tokens de acceso")
    print("   • Implementar flujo OAuth2")
    print()
    print("2️⃣ USAR CUENTA GMAIL (RECOMENDADO):")
    print("   • Gmail permite autenticación básica")
    print("   • Configuración más simple")
    print("   • Funciona inmediatamente")
    print()
    print("3️⃣ USAR APP PASSWORD (SI ESTÁ DISPONIBLE):")
    print("   • Verificar si la cuenta tiene 2FA habilitado")
    print("   • Generar contraseña de aplicación")
    print("   • Usar esa contraseña en lugar de la normal")
    print()
    
    return mostrar_opciones()

def mostrar_opciones():
    """Mostrar opciones disponibles"""
    
    print("🎯 ¿QUÉ QUIERES HACER?")
    print("=" * 40)
    print("1. Configurar OAuth2 (requiere Azure)")
    print("2. Cambiar a cuenta Gmail")
    print("3. Verificar si hay App Password disponible")
    print("4. Salir")
    print()
    
    while True:
        try:
            opcion = input("Selecciona una opción (1-4): ").strip()
            if opcion in ['1', '2', '3', '4']:
                return opcion
            else:
                print("❌ Opción inválida. Selecciona 1, 2, 3 o 4.")
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            return '4'

def configurar_oauth2():
    """Configurar OAuth2 para Hotmail"""
    
    print("\n🔐 CONFIGURACIÓN OAUTH2")
    print("=" * 30)
    print()
    print("⚠️  ADVERTENCIA: Esta opción es compleja y requiere:")
    print("   • Cuenta de Azure (gratuita)")
    print("   • Conocimientos técnicos avanzados")
    print("   • Configuración de aplicaciones")
    print()
    print("📋 PASOS REQUERIDOS:")
    print("1. Ir a https://portal.azure.com")
    print("2. Crear nueva aplicación")
    print("3. Configurar permisos para Microsoft Graph")
    print("4. Obtener Client ID y Client Secret")
    print("5. Configurar redirect URI")
    print("6. Implementar flujo OAuth2 en el código")
    print()
    print("⏰ TIEMPO ESTIMADO: 2-4 horas")
    print("🔄 ¿Quieres continuar con esta opción?")
    
    respuesta = input("(s/n): ").lower().strip()
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        print("\n📚 Recursos para OAuth2:")
        print("• https://docs.microsoft.com/en-us/graph/auth-v2-user")
        print("• https://github.com/Azure-Samples/ms-identity-python-webapp")
        print("• https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade")
        print()
        print("🔧 Después de configurar Azure, necesitarás:")
        print("• Modificar email_sender.py para usar OAuth2")
        print("• Implementar flujo de autenticación")
        print("• Manejar tokens de acceso")
        print()
        print("💡 RECOMENDACIÓN: Considera usar Gmail por ahora")
        return False
    else:
        print("\n✅ Opción cancelada. Volviendo al menú principal.")
        return False

def cambiar_a_gmail():
    """Cambiar a cuenta Gmail"""
    
    print("\n📧 CAMBIO A CUENTA GMAIL")
    print("=" * 30)
    print()
    print("✅ VENTAJAS DE GMAIL:")
    print("   • Autenticación básica habilitada")
    print("   • Configuración simple")
    print("   • Funciona inmediatamente")
    print("   • Límites generosos de envío")
    print()
    print("🔧 CONFIGURACIÓN REQUERIDA:")
    print("1. Habilitar 'Acceso de aplicaciones menos seguras'")
    print("2. O usar contraseña de aplicación (recomendado)")
    print("3. Configurar credenciales en el sistema")
    print()
    
    respuesta = input("¿Quieres configurar Gmail? (s/n): ").lower().strip()
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        print("\n📋 PASOS PARA GMAIL:")
        print("1. Ir a https://myaccount.google.com/security")
        print("2. Habilitar verificación en dos pasos")
        print("3. Generar contraseña de aplicación")
        print("4. Usar esa contraseña en el sistema")
        print()
        print("📧 SERVIDOR SMTP: smtp.gmail.com:587")
        print("🔑 Usar contraseña de aplicación, NO la contraseña normal")
        print()
        
        # Crear archivo de configuración Gmail
        crear_config_gmail()
        return True
    else:
        print("\n✅ Opción cancelada.")
        return False

def crear_config_gmail():
    """Crear archivo de configuración para Gmail"""
    
    config_content = '''# Configuración Gmail
GMAIL_EMAIL = "tu_email@gmail.com"
GMAIL_PASSWORD = "tu_app_password"
GMAIL_SMTP_SERVER = "smtp.gmail.com"
GMAIL_SMTP_PORT = 587

# Instrucciones:
# 1. Reemplaza tu_email@gmail.com con tu email real
# 2. Reemplaza tu_app_password con la contraseña de aplicación
# 3. Guarda este archivo como .env
# 4. El sistema usará Gmail en lugar de Hotmail
'''
    
    try:
        with open('config_gmail.txt', 'w', encoding='utf-8') as f:
            f.write(config_content)
        print("✅ Archivo config_gmail.txt creado")
        print("📝 Edita este archivo con tus credenciales de Gmail")
    except Exception as e:
        print(f"❌ Error creando archivo: {e}")

def verificar_app_password():
    """Verificar si hay App Password disponible"""
    
    print("\n🔑 VERIFICACIÓN DE APP PASSWORD")
    print("=" * 35)
    print()
    print("ℹ️  INFORMACIÓN:")
    print("   • App Password es una contraseña especial")
    print("   • Se genera cuando tienes 2FA habilitado")
    print("   • Permite acceso a aplicaciones")
    print()
    print("🔍 VERIFICAR SI ESTÁ DISPONIBLE:")
    print("1. Ir a https://account.live.com/proofs/AppPassword")
    print("2. Si tienes 2FA, podrás generar App Password")
    print("3. Si no tienes 2FA, no estará disponible")
    print()
    print("⚠️  LIMITACIÓN:")
    print("   • Solo funciona si tienes 2FA habilitado")
    print("   • Si no lo tienes, no podrás usar esta opción")
    print()
    
    respuesta = input("¿Tienes 2FA habilitado en tu cuenta Hotmail? (s/n): ").lower().strip()
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        print("\n✅ ¡Excelente! Puedes usar App Password:")
        print("1. Ve a https://account.live.com/proofs/AppPassword")
        print("2. Genera una nueva contraseña de aplicación")
        print("3. Usa esa contraseña en lugar de tu contraseña normal")
        print("4. El sistema debería funcionar")
        return True
    else:
        print("\n❌ Sin 2FA no puedes usar App Password")
        print("💡 OPCIONES DISPONIBLES:")
        print("   • Habilitar 2FA en tu cuenta Hotmail")
        print("   • Cambiar a cuenta Gmail")
        print("   • Configurar OAuth2 (complejo)")
        return False

def main():
    """Función principal"""
    
    print("🚀 SISTEMA DE CONFIGURACIÓN DE EMAILS")
    print("=" * 50)
    print()
    
    while True:
        opcion = mostrar_instrucciones_oauth()
        
        if opcion == '1':
            configurar_oauth2()
        elif opcion == '2':
            if cambiar_a_gmail():
                print("\n✅ Gmail configurado. El sistema está listo para usar Gmail.")
                break
        elif opcion == '3':
            verificar_app_password()
        elif opcion == '4':
            print("\n👋 ¡Hasta luego!")
            break
        
        print("\n" + "="*50 + "\n")
    
    print("\n📚 RESUMEN DE SOLUCIONES:")
    print("• OAuth2: Complejo, requiere Azure")
    print("• Gmail: Simple, funciona inmediatamente")
    print("• App Password: Solo si tienes 2FA")
    print()
    print("💡 RECOMENDACIÓN: Usa Gmail por simplicidad")

if __name__ == "__main__":
    main()
