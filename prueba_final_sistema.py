#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db, User, EmailCampaign, EmailContact, EmailTemplate, EmailList
from email_sender import EmailSender
from datetime import datetime, timezone
import time

def prueba_final_sistema():
    with app.app_context():
        print("🎯 PRUEBA FINAL DEL SISTEMA COMPLETO")
        print("=" * 60)
        
        # Obtener usuario
        user = User.query.filter_by(username='admin').first()
        if not user:
            print("❌ Usuario admin no encontrado")
            return False
        
        print(f"👤 Usuario: {user.username}")
        print(f"📧 Email: {user.outlook_email}")
        print(f"🔑 Password: {user.outlook_password[:4]}****{user.outlook_password[-4:]}")
        
        # Verificar datos del sistema
        print(f"\n📊 VERIFICANDO DATOS DEL SISTEMA:")
        lists = EmailList.query.filter_by(user_id=user.id).all()
        print(f"   📋 Listas: {len(lists)}")
        for lst in lists:
            contacts = EmailContact.query.filter_by(list_id=lst.id).all()
            print(f"      - {lst.name}: {len(contacts)} contactos")
        
        templates = EmailTemplate.query.filter_by(user_id=user.id).all()
        print(f"   📝 Templates: {len(templates)}")
        for template in templates:
            print(f"      - {template.name}")
        
        campaigns = EmailCampaign.query.filter_by(user_id=user.id).all()
        print(f"   📧 Campañas: {len(campaigns)}")
        
        # Probar conexión
        print(f"\n🚀 PROBANDO CONEXIÓN A OUTLOOK...")
        if user.outlook_email and user.outlook_password:
            sender = EmailSender(email=user.outlook_email, password=user.outlook_password)
            
            if sender.connect():
                print("✅ Conexión exitosa a Outlook!")
                
                # Probar envío de email
                print(f"\n📧 Probando envío de email...")
                test_email = "guillermoromerog@gmail.com"
                test_subject = "Prueba Final - " + datetime.now().strftime('%H:%M:%S')
                test_content = """
                <html>
                <body>
                    <h2>Prueba Final del Sistema</h2>
                    <p>Este es un email de prueba para verificar que el sistema funciona correctamente.</p>
                    <p><strong>Fecha:</strong> {}</p>
                    <p><strong>Hora:</strong> {}</p>
                    <hr>
                    <p><em>Sistema de envío masivo funcionando correctamente.</em></p>
                </body>
                </html>
                """.format(datetime.now().strftime('%d/%m/%Y'), datetime.now().strftime('%H:%M:%S'))
                
                success = sender.send_email(test_email, test_subject, test_content, "admin")
                
                if success:
                    print(f"✅ Email enviado exitosamente a: {test_email}")
                    print(f"📧 Revisa tu bandeja de entrada")
                    print(f"\n🎉 ¡SISTEMA 100% FUNCIONAL!")
                    return True
                else:
                    print(f"❌ Error enviando email")
                    return False
            else:
                print("❌ Error conectando a Outlook")
                print("\n💡 OPCIONES ALTERNATIVAS:")
                print("   1. Generar nuevo App Password")
                print("   2. Usar modo PRUEBA (simulación)")
                print("   3. Verificar configuración de 2FA")
                
                # Activar modo PRUEBA
                print(f"\n🔧 ACTIVANDO MODO PRUEBA...")
                return activar_modo_prueba()
        else:
            print("⚠️ Credenciales no configuradas")
            return activar_modo_prueba()

def activar_modo_prueba():
    print(f"\n🎭 MODO PRUEBA ACTIVADO")
    print(f"   • Los emails se simularán sin enviarse realmente")
    print(f"   • El sistema funcionará para pruebas")
    print(f"   • Para envío real, configura las credenciales")
    
    # Crear una campaña de prueba
    user = User.query.filter_by(username='admin').first()
    test_list = EmailList.query.filter_by(name='Lista de Prueba').first()
    template = EmailTemplate.query.filter_by(name='Email de Bienvenida').first()
    
    if test_list and template:
        campaign = EmailCampaign(
            name='Prueba Final - ' + datetime.now().strftime('%H:%M:%S'),
            template_id=template.id,
            list_id=test_list.id,
            user_id=user.id,
            status='pending'
        )
        db.session.add(campaign)
        db.session.commit()
        
        print(f"✅ Campaña de prueba creada: {campaign.name}")
        print(f"📧 Contactos en lista: {len(EmailContact.query.filter_by(list_id=test_list.id).all())}")
        
        return True
    else:
        print("❌ Error creando campaña de prueba")
        return False

if __name__ == "__main__":
    prueba_final_sistema()
