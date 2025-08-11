#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def verificar_2fa():
    print("🔍 VERIFICACIÓN DE 2FA Y APP PASSWORD")
    print("=" * 50)
    
    print("\n📋 PASOS PARA VERIFICAR:")
    print("1. Abre tu navegador")
    print("2. Ve a: https://account.microsoft.com/security")
    print("3. Inicia sesión con: el_chicher@hotmail.com")
    print("4. Busca estas secciones:")
    
    print("\n🔐 SECCIONES A VERIFICAR:")
    print("   • Autenticación de dos factores")
    print("   • Contraseñas de aplicación")
    
    print("\n✅ SI VES 'Autenticación de dos factores':")
    print("   • Debe mostrar 'Activado' o 'Habilitado'")
    print("   • Si no está activado, haz clic en 'Configurar'")
    print("   • Sigue las instrucciones para habilitarlo")
    
    print("\n🔑 SI VES 'Contraseñas de aplicación':")
    print("   • Haz clic en 'Crear una nueva contraseña de aplicación'")
    print("   • Selecciona 'Correo' o 'Outlook'")
    print("   • Anota la contraseña de 16 caracteres")
    
    print("\n❌ SI NO VES 'Contraseñas de aplicación':")
    print("   • Primero debes habilitar 2FA")
    print("   • Solo aparece después de habilitar 2FA")
    
    print("\n" + "=" * 50)
    print("🎯 PRÓXIMOS PASOS:")
    print("1. Verifica si tienes 2FA habilitado")
    print("2. Si no, habilítalo primero")
    print("3. Crea un App Password")
    print("4. Ejecuta: python configurar_credenciales_reales.py")
    
    input("\nPresiona Enter cuando hayas verificado...")
    
    print("\n✅ ¿Tienes 2FA habilitado? (s/n): ", end="")
    tiene_2fa = input().strip().lower()
    
    if tiene_2fa in ['s', 'si', 'sí', 'y', 'yes']:
        print("✅ ¿Puedes crear App Password? (s/n): ", end="")
        puede_app_password = input().strip().lower()
        
        if puede_app_password in ['s', 'si', 'sí', 'y', 'yes']:
            print("\n🎉 ¡Perfecto! Ahora puedes:")
            print("1. Crear un App Password")
            print("2. Ejecutar: python configurar_credenciales_reales.py")
            print("3. Usar el App Password (NO tu contraseña normal)")
        else:
            print("\n⚠️ Necesitas habilitar 2FA primero:")
            print("1. Ve a: https://account.microsoft.com/security")
            print("2. Busca 'Autenticación de dos factores'")
            print("3. Haz clic en 'Configurar'")
            print("4. Sigue las instrucciones")
    else:
        print("\n⚠️ Necesitas habilitar 2FA:")
        print("1. Ve a: https://account.microsoft.com/security")
        print("2. Busca 'Autenticación de dos factores'")
        print("3. Haz clic en 'Configurar'")
        print("4. Usa tu teléfono para recibir códigos")

if __name__ == "__main__":
    verificar_2fa()
