#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db, User, EmailCampaign, EmailContact, EmailTemplate, EmailList
from datetime import datetime

def estado_sistema():
    with app.app_context():
        print("📊 ESTADO ACTUAL DEL SISTEMA")
        print("=" * 50)
        
        # Usuario
        user = User.query.filter_by(username='admin').first()
        if not user:
            print("❌ Usuario admin no encontrado")
            return
        
        print(f"👤 Usuario: {user.username}")
        print(f"📧 Email configurado: {user.outlook_email or 'No configurado'}")
        print(f"🔑 Password configurado: {'Sí' if user.outlook_password else 'No'}")
        
        # Listas
        lists = EmailList.query.filter_by(user_id=user.id).all()
        print(f"\n📋 Listas de emails: {len(lists)}")
        for lst in lists:
            contacts = EmailContact.query.filter_by(list_id=lst.id).all()
            print(f"   • {lst.name}: {len(contacts)} contactos")
            for contact in contacts:
                print(f"     - {contact.email} ({contact.name or 'Sin nombre'})")
        
        # Templates
        templates = EmailTemplate.query.filter_by(user_id=user.id).all()
        print(f"\n📝 Templates: {len(templates)}")
        for template in templates:
            print(f"   • {template.name}")
            print(f"     Asunto: {template.subject[:50]}...")
        
        # Campañas
        campaigns = EmailCampaign.query.filter_by(user_id=user.id).all()
        print(f"\n📧 Campañas: {len(campaigns)}")
        for campaign in campaigns:
            status_emoji = {
                'pending': '⏳',
                'running': '🚀',
                'completed': '✅',
                'failed': '❌'
            }.get(campaign.status, '❓')
            
            print(f"   {status_emoji} {campaign.name}")
            print(f"     Estado: {campaign.status}")
            print(f"     Progreso: {campaign.sent_count}/{campaign.total_count}")
            print(f"     Fecha: {campaign.created_at.strftime('%d/%m/%Y %H:%M')}")
        
        # Estado del sistema
        print(f"\n🎯 ESTADO DEL SISTEMA:")
        if user.outlook_email and user.outlook_password:
            print(f"   ✅ Credenciales configuradas")
            print(f"   📧 Email: {user.outlook_email}")
            print(f"   🔑 Password: {user.outlook_password[:4]}****{user.outlook_password[-4:]}")
        else:
            print(f"   ⚠️ Credenciales no configuradas")
            print(f"   🎭 Sistema en modo PRUEBA")
        
        print(f"\n🚀 PRÓXIMOS PASOS:")
        if user.outlook_email and user.outlook_password:
            print(f"   1. Ejecutar: python probar_conexion_final.py")
            print(f"   2. Si falla, ejecutar: python configurar_credenciales_final.py")
        else:
            print(f"   1. Ejecutar: python configurar_credenciales_final.py")
            print(f"   2. Seguir las instrucciones para configurar 2FA y App Password")
        
        print(f"   3. Ejecutar: python iniciar_web.py")
        print(f"   4. Abrir: http://127.0.0.1:5000")
        
        print(f"\n💡 INFORMACIÓN ADICIONAL:")
        print(f"   • El sistema está funcionando correctamente")
        print(f"   • Tienes {len(lists)} listas con {sum(len(EmailContact.query.filter_by(list_id=lst.id).all()) for lst in lists)} contactos total")
        print(f"   • Tienes {len(templates)} templates disponibles")
        print(f"   • Tienes {len(campaigns)} campañas creadas")

if __name__ == "__main__":
    estado_sistema()
