#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db, EmailCampaign, EmailContact, EmailTemplate, User, EmailList
from datetime import datetime, timezone

def create_test_campaign():
    with app.app_context():
        # Obtener usuario admin
        user = User.query.filter_by(username='admin').first()
        if not user:
            print("❌ Usuario admin no encontrado")
            return
        
        print(f"👤 Usuario: {user.username}")
        
        # Obtener lista de prueba
        test_list = EmailList.query.filter_by(name='Lista de Prueba').first()
        if not test_list:
            print("❌ Lista de prueba no encontrada")
            return
        
        print(f"📋 Lista: {test_list.name} (ID: {test_list.id})")
        
        # Obtener template
        template = EmailTemplate.query.filter_by(name='Email de Bienvenida').first()
        if not template:
            print("❌ Template no encontrado")
            return
        
        print(f"📝 Template: {template.name} (ID: {template.id})")
        
        # Crear nueva campaña
        new_campaign = EmailCampaign(
            name='Campaña de Prueba - ' + datetime.now().strftime('%H:%M:%S'),
            template_id=template.id,
            list_id=test_list.id,
            user_id=user.id,
            status='pending'
        )
        
        db.session.add(new_campaign)
        db.session.commit()
        
        print(f"✅ Nueva campaña creada: {new_campaign.name} (ID: {new_campaign.id})")
        
        # Verificar contactos
        contacts = EmailContact.query.filter_by(list_id=test_list.id).all()
        print(f"📧 Contactos en la lista: {len(contacts)}")
        for contact in contacts:
            print(f"   - {contact.email}")
        
        return new_campaign.id

def test_campaign_simulation(campaign_id):
    with app.app_context():
        campaign = EmailCampaign.query.get(campaign_id)
        if not campaign:
            print(f"❌ Campaña {campaign_id} no encontrada")
            return
        
        print(f"\n🚀 Probando campaña: {campaign.name}")
        print(f"   Estado actual: {campaign.status}")
        print(f"   Total: {campaign.total_count}")
        print(f"   Enviados: {campaign.sent_count}")
        
        # Simular inicio de campaña
        contacts = EmailContact.query.filter_by(list_id=campaign.list_id).all()
        total_contacts = len(contacts)
        
        print(f"📋 Total de contactos encontrados: {total_contacts}")
        
        # Actualizar campaña
        campaign.total_count = total_contacts
        campaign.status = 'running'
        campaign.started_at = datetime.now(timezone.utc)
        db.session.commit()
        
        print(f"✅ Campaña actualizada:")
        print(f"   Total: {campaign.total_count}")
        print(f"   Estado: {campaign.status}")
        
        # Simular envío
        sent_count = 0
        for i, contact in enumerate(contacts, 1):
            print(f"📧 [SIMULACIÓN] Enviando email {i}/{total_contacts} a: {contact.email}")
            sent_count += 1
            campaign.sent_count = sent_count
            db.session.commit()
            print(f"✅ [SIMULACIÓN] Email enviado exitosamente a: {contact.email} ({sent_count}/{total_contacts})")
        
        # Marcar como completada
        campaign.status = 'completed'
        campaign.completed_at = datetime.now(timezone.utc)
        db.session.commit()
        
        print(f"\n🎉 ¡Campaña completada exitosamente!")
        print(f"   Total enviados: {sent_count}/{total_contacts}")
        print(f"   Estado final: {campaign.status}")

if __name__ == "__main__":
    print("🧪 Iniciando prueba del sistema de envío de emails...")
    
    # Crear nueva campaña
    campaign_id = create_test_campaign()
    
    if campaign_id:
        # Probar simulación
        test_campaign_simulation(campaign_id)
    
    print("\n✅ Prueba completada!")
