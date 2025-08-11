#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db, EmailCampaign, EmailContact, EmailTemplate, User

def test_campaign():
    with app.app_context():
        # Obtener usuario admin
        user = User.query.filter_by(username='admin').first()
        if not user:
            print("❌ Usuario admin no encontrado")
            return
        
        print(f"👤 Usuario: {user.username}")
        
        # Obtener campañas
        campaigns = EmailCampaign.query.filter_by(user_id=user.id).all()
        print(f"📊 Campañas encontradas: {len(campaigns)}")
        
        for campaign in campaigns:
            print(f"\n📧 Campaña: {campaign.name} (ID: {campaign.id})")
            print(f"   Estado: {campaign.status}")
            print(f"   Total: {campaign.total_count}")
            print(f"   Enviados: {campaign.sent_count}")
            
            # Obtener contactos
            contacts = EmailContact.query.filter_by(list_id=campaign.list_id).all()
            print(f"   Contactos en lista: {len(contacts)}")
            for contact in contacts:
                print(f"     - {contact.email}")
        
        # Verificar templates
        templates = EmailTemplate.query.filter_by(user_id=user.id).all()
        print(f"\n📝 Templates encontrados: {len(templates)}")
        for template in templates:
            print(f"   - {template.name} (ID: {template.id})")

if __name__ == "__main__":
    test_campaign()
