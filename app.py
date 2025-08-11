#!/usr/bin/env python3
"""
Sistema de Emails Masivos - Versión Web
Interfaz web moderna y fácil de usar
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
import pandas as pd
from datetime import datetime, timezone
import threading
import time
from email_sender import EmailSender
from sendgrid_definitivo import SendGridDefinitive as SendGridSender
from config import Config

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelos de base de datos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    outlook_email = db.Column(db.String(120))
    outlook_password = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

class EmailList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    # Relación con contactos
    contacts = db.relationship('EmailContact', backref='email_list', lazy=True, cascade='all, delete-orphan')

class EmailContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(100))
    company = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    list_id = db.Column(db.Integer, db.ForeignKey('email_list.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

class EmailTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

class EmailCampaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('email_template.id'), nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('email_list.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, running, completed, failed
    sent_count = db.Column(db.Integer, default=0)
    total_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)

# Crear tablas
with app.app_context():
    db.create_all()
    
    # Crear usuario por defecto si no existe
    default_user = User.query.filter_by(username='admin').first()
    if not default_user:
        default_user = User(
            username='admin',
            email='admin@localhost',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(default_user)
        db.session.commit()
    
    # Crear templates de ejemplo si no existen
    if EmailTemplate.query.filter_by(user_id=default_user.id).count() == 0:
        # Template 1: Email de bienvenida
        template1 = EmailTemplate(
            name='Email de Bienvenida',
            subject='¡Bienvenido a nuestro sistema!',
            content='''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Bienvenida</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #2c3e50; text-align: center;">¡Bienvenido {{name}}!</h1>
        
        <p>Hola {{name}},</p>
        
        <p>Nos complace darte la bienvenida a nuestro sistema de emails masivos.</p>
        
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
            <h3 style="color: #2c3e50; margin-top: 0;">Información de contacto:</h3>
            <p><strong>Email:</strong> {{email}}</p>
            <p><strong>Empresa:</strong> {{company}}</p>
            <p><strong>Teléfono:</strong> {{phone}}</p>
        </div>
        
        <p>Este es un email de prueba del sistema de envío masivo.</p>
        
        <p>Saludos cordiales,<br>
        <strong>Equipo de Desarrollo</strong></p>
        
        <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
        <p style="text-align: center; color: #666; font-size: 12px;">
            Este email fue enviado desde el Sistema de Emails Masivos
        </p>
    </div>
</body>
</html>
            ''',
            user_id=default_user.id
        )
        db.session.add(template1)
        
        # Template 2: Email promocional
        template2 = EmailTemplate(
            name='Email Promocional',
            subject='¡Oferta especial para {{name}}!',
            content='''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Oferta Especial</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; text-align: center;">
            <h1 style="margin: 0; font-size: 28px;">¡OFERTA ESPECIAL!</h1>
            <p style="font-size: 18px; margin: 10px 0;">Exclusiva para {{name}}</p>
        </div>
        
        <div style="padding: 20px;">
            <h2 style="color: #2c3e50;">Hola {{name}},</h2>
            
            <p>Tenemos una oferta especial preparada especialmente para ti y tu empresa <strong>{{company}}</strong>.</p>
            
            <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3 style="color: #856404; margin-top: 0;">🎉 ¡Descuento del 50%!</h3>
                <p style="margin: 0;">Válido hasta el final del mes</p>
            </div>
            
            <p>No dejes pasar esta oportunidad única. Contacta con nosotros al teléfono: <strong>{{phone}}</strong></p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="#" style="background-color: #28a745; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">¡Aprovechar Oferta!</a>
            </div>
            
            <p>Saludos,<br>
            <strong>Equipo Comercial</strong></p>
        </div>
        
        <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
        <p style="text-align: center; color: #666; font-size: 12px;">
            Email enviado a: {{email}} | Sistema de Emails Masivos
        </p>
    </div>
</body>
</html>
            ''',
            user_id=default_user.id
        )
        db.session.add(template2)
        
        # Template 3: Email informativo
        template3 = EmailTemplate(
            name='Email Informativo',
            subject='Información importante para {{name}}',
            content='''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Información Importante</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="border-left: 4px solid #007bff; padding-left: 20px; margin: 20px 0;">
            <h1 style="color: #007bff; margin: 0;">Información Importante</h1>
        </div>
        
        <p>Estimado/a {{name}},</p>
        
        <p>Esperamos que este mensaje te encuentre bien. Te escribimos para compartir información relevante sobre nuestros servicios.</p>
        
        <div style="background-color: #e3f2fd; padding: 20px; border-radius: 5px; margin: 20px 0;">
            <h3 style="color: #1976d2; margin-top: 0;">📋 Resumen de información:</h3>
            <ul>
                <li><strong>Contacto:</strong> {{email}}</li>
                <li><strong>Empresa:</strong> {{company}}</li>
                <li><strong>Teléfono:</strong> {{phone}}</li>
            </ul>
        </div>
        
        <p>Si tienes alguna pregunta o necesitas más información, no dudes en contactarnos.</p>
        
        <p>Atentamente,<br>
        <strong>Equipo de Atención al Cliente</strong></p>
        
        <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
        <p style="text-align: center; color: #666; font-size: 12px;">
            Sistema de Emails Masivos - {{email}}
        </p>
    </div>
</body>
</html>
            ''',
            user_id=default_user.id
        )
        db.session.add(template3)
        
        db.session.commit()
        print("✅ Templates de ejemplo creados")
    
    # Crear lista de emails de prueba si no existe
    if EmailList.query.filter_by(user_id=default_user.id).count() == 0:
        print("🔍 Creando lista de emails de prueba...")
        # Crear lista de prueba
        test_list = EmailList(
            name='Lista de Prueba',
            user_id=default_user.id
        )
        db.session.add(test_list)
        db.session.commit()
        print(f"✅ Lista creada con ID: {test_list.id}")
        
        # Agregar emails de prueba
        test_emails = [
            ('el_chicher@hotmail.com', 'El Chicher', 'Empresa Test 1', '123-456-7890'),
            ('guillermoromerog@gmail.com', 'Guillermo Romero', 'Empresa Test 2', '098-765-4321'),
            ('v.luis.romero@tropicana.com', 'Luis Romero', 'Tropicana', '555-123-4567')
        ]
        
        for email, name, company, phone in test_emails:
            contact = EmailContact(
                email=email,
                name=name,
                company=company,
                phone=phone,
                list_id=test_list.id
            )
            db.session.add(contact)
        
        db.session.commit()
        print("✅ Lista de emails de prueba creada")
    else:
        print("ℹ️ Lista de prueba ya existe")

# Variables globales para el estado de envío
sending_status = {}
current_campaigns = {}

@app.route('/favicon.ico')
def favicon():
    """Servir favicon para evitar error 404"""
    return app.send_static_file('favicon.ico')

@app.route('/')
def index():
    # Acceso directo sin autenticación - usar usuario por defecto
    default_user = User.query.filter_by(username='admin').first()
    if default_user:
        session['user_id'] = default_user.id
        session['username'] = default_user.username
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirigir directamente al dashboard
    default_user = User.query.filter_by(username='admin').first()
    if default_user:
        session['user_id'] = default_user.id
        session['username'] = default_user.username
        flash('¡Bienvenido al Sistema de Emails Masivos!', 'success')
        return redirect(url_for('dashboard'))
    
    return redirect(url_for('dashboard'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Redirigir directamente al dashboard
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    # Usar usuario por defecto automáticamente
    default_user = User.query.filter_by(username='admin').first()
    if not default_user:
        # Crear usuario por defecto si no existe
        default_user = User(
            username='admin',
            email='admin@localhost',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(default_user)
        db.session.commit()
    
    session['user_id'] = default_user.id
    session['username'] = default_user.username
    
    campaigns = EmailCampaign.query.filter_by(user_id=default_user.id).order_by(EmailCampaign.created_at.desc()).limit(5)
    lists = EmailList.query.filter_by(user_id=default_user.id).count()
    templates = EmailTemplate.query.filter_by(user_id=default_user.id).count()
    
    return render_template('dashboard.html', 
                         user=default_user, 
                         campaigns=campaigns, 
                         lists_count=lists, 
                         templates_count=templates)

@app.route('/lists')
def lists():
    # Usar usuario por defecto automáticamente
    default_user = User.query.filter_by(username='admin').first()
    if default_user:
        session['user_id'] = default_user.id
        user_lists = EmailList.query.filter_by(user_id=default_user.id).all()
        return render_template('lists.html', lists=user_lists)
    return redirect(url_for('dashboard'))

@app.route('/lists/<int:list_id>')
def view_list(list_id):
    # Usar usuario por defecto automáticamente
    default_user = User.query.filter_by(username='admin').first()
    if not default_user:
        return redirect(url_for('dashboard'))
    
    session['user_id'] = default_user.id
    
    email_list = EmailList.query.get_or_404(list_id)
    if email_list.user_id != default_user.id:
        flash('Acceso denegado', 'error')
        return redirect(url_for('lists'))
    
    contacts = EmailContact.query.filter_by(list_id=list_id).all()
    return render_template('view_list.html', email_list=email_list, contacts=contacts)

@app.route('/lists/<int:list_id>/edit', methods=['GET', 'POST'])
def edit_list(list_id):
    # Usar usuario por defecto automáticamente
    default_user = User.query.filter_by(username='admin').first()
    if not default_user:
        return redirect(url_for('dashboard'))
    
    session['user_id'] = default_user.id
    
    email_list = EmailList.query.get_or_404(list_id)
    if email_list.user_id != default_user.id:
        flash('Acceso denegado', 'error')
        return redirect(url_for('lists'))
    
    if request.method == 'POST':
        email_list.name = request.form['name']
        emails_data = request.form['emails_data']
        
        # Eliminar contactos existentes
        EmailContact.query.filter_by(list_id=list_id).delete()
        
        # Procesar nuevos emails
        lines = emails_data.strip().split('\n')
        for line in lines:
            if line.strip():
                parts = line.split(',')
                email = parts[0].strip()
                name = parts[1].strip() if len(parts) > 1 else ''
                company = parts[2].strip() if len(parts) > 2 else ''
                phone = parts[3].strip() if len(parts) > 3 else ''
                
                contact = EmailContact(
                    email=email,
                    name=name,
                    company=company,
                    phone=phone,
                    list_id=email_list.id
                )
                db.session.add(contact)
        
        db.session.commit()
        flash('Lista actualizada exitosamente', 'success')
        return redirect(url_for('lists'))
    
    # Obtener contactos actuales para mostrar en el formulario
    contacts = EmailContact.query.filter_by(list_id=list_id).all()
    emails_data = '\n'.join([f"{c.email}, {c.name}, {c.company}, {c.phone}" for c in contacts])
    
    return render_template('edit_list.html', email_list=email_list, emails_data=emails_data)

@app.route('/lists/create', methods=['GET', 'POST'])
def create_list():
    # Usar usuario por defecto automáticamente
    default_user = User.query.filter_by(username='admin').first()
    if not default_user:
        return redirect(url_for('dashboard'))
    
    session['user_id'] = default_user.id
    
    if request.method == 'POST':
        name = request.form['name']
        emails_data = request.form['emails_data']
        
        # Crear lista
        email_list = EmailList(name=name, user_id=default_user.id)
        db.session.add(email_list)
        db.session.commit()
        
        # Procesar emails
        lines = emails_data.strip().split('\n')
        for line in lines:
            if line.strip():
                parts = line.split(',')
                email = parts[0].strip()
                name = parts[1].strip() if len(parts) > 1 else ''
                company = parts[2].strip() if len(parts) > 2 else ''
                phone = parts[3].strip() if len(parts) > 3 else ''
                
                contact = EmailContact(
                    email=email,
                    name=name,
                    company=company,
                    phone=phone,
                    list_id=email_list.id
                )
                db.session.add(contact)
        
        db.session.commit()
        flash('Lista creada exitosamente', 'success')
        return redirect(url_for('lists'))
    
    return render_template('create_list.html')

@app.route('/templates')
def templates():
    # Usar usuario por defecto automáticamente
    default_user = User.query.filter_by(username='admin').first()
    if default_user:
        session['user_id'] = default_user.id
        user_templates = EmailTemplate.query.filter_by(user_id=default_user.id).all()
        return render_template('templates.html', templates=user_templates)
    return redirect(url_for('dashboard'))

@app.route('/templates/create', methods=['GET', 'POST'])
def create_template():
    # Usar usuario por defecto automáticamente
    default_user = User.query.filter_by(username='admin').first()
    if not default_user:
        return redirect(url_for('dashboard'))
    
    session['user_id'] = default_user.id
    
    if request.method == 'POST':
        name = request.form['name']
        subject = request.form['subject']
        content = request.form['content']
        
        template = EmailTemplate(
            name=name,
            subject=subject,
            content=content,
            user_id=default_user.id
        )
        db.session.add(template)
        db.session.commit()
        
        flash('Template creado exitosamente', 'success')
        return redirect(url_for('templates'))
    
    return render_template('create_template.html')

@app.route('/campaigns')
def campaigns():
    # Usar usuario por defecto automáticamente
    default_user = User.query.filter_by(username='admin').first()
    if default_user:
        session['user_id'] = default_user.id
        user_campaigns = EmailCampaign.query.filter_by(user_id=default_user.id).all()
        return render_template('campaigns.html', campaigns=user_campaigns)
    return redirect(url_for('dashboard'))

@app.route('/campaigns/create', methods=['GET', 'POST'])
def create_campaign():
    # Usar usuario por defecto automáticamente
    default_user = User.query.filter_by(username='admin').first()
    if not default_user:
        return redirect(url_for('dashboard'))
    
    session['user_id'] = default_user.id
    
    if request.method == 'POST':
        name = request.form['name']
        template_id = request.form['template_id']
        list_id = request.form['list_id']
        
        campaign = EmailCampaign(
            name=name,
            template_id=template_id,
            list_id=list_id,
            user_id=default_user.id
        )
        db.session.add(campaign)
        db.session.commit()
        
        flash('Campaña creada exitosamente', 'success')
        return redirect(url_for('campaigns'))
    
    templates = EmailTemplate.query.filter_by(user_id=default_user.id).all()
    lists = EmailList.query.filter_by(user_id=default_user.id).all()
    return render_template('create_campaign.html', templates=templates, lists=lists)

@app.route('/campaigns/<int:campaign_id>')
def view_campaign(campaign_id):
    # Usar usuario por defecto automáticamente
    default_user = User.query.filter_by(username='admin').first()
    if not default_user:
        return redirect(url_for('dashboard'))
    
    session['user_id'] = default_user.id
    
    campaign = EmailCampaign.query.get_or_404(campaign_id)
    if campaign.user_id != default_user.id:
        flash('Acceso denegado', 'error')
        return redirect(url_for('campaigns'))
    
    # Obtener contactos de la lista
    contacts = EmailContact.query.filter_by(list_id=campaign.list_id).all()
    
    # Obtener template
    template = EmailTemplate.query.get(campaign.template_id)
    
    return render_template('view_campaign.html', campaign=campaign, contacts=contacts, template=template)

@app.route('/campaigns/<int:campaign_id>/start')
def start_campaign(campaign_id):
    # Usar usuario por defecto automáticamente
    default_user = User.query.filter_by(username='admin').first()
    if not default_user:
        return redirect(url_for('dashboard'))
    
    session['user_id'] = default_user.id
    
    campaign = EmailCampaign.query.get_or_404(campaign_id)
    if campaign.user_id != default_user.id:
        flash('Acceso denegado', 'error')
        return redirect(url_for('campaigns'))
    
    # Actualizar el total_count antes de iniciar
    contacts = EmailContact.query.filter_by(list_id=campaign.list_id).all()
    campaign.total_count = len(contacts)
    campaign.status = 'running'
    campaign.started_at = datetime.now(timezone.utc)
    db.session.commit()
    
    # Iniciar envío en background
    thread = threading.Thread(target=send_campaign_emails, args=(campaign_id,))
    thread.daemon = True
    thread.start()
    
    flash('Campaña iniciada', 'success')
    return redirect(url_for('campaigns'))

def send_campaign_emails(campaign_id):
    """Función para enviar emails en background usando SendGrid"""
    campaign = None
    try:
        # Crear contexto de aplicación para el hilo
        with app.app_context():
            campaign = db.session.get(EmailCampaign, campaign_id)
            if not campaign:
                print(f"❌ Campaña {campaign_id} no encontrada")
                return
            
            print(f"🚀 Iniciando envío de campaña: {campaign.name} (ID: {campaign_id})")
            
            # Obtener contactos PRIMERO
            contacts = EmailContact.query.filter_by(list_id=campaign.list_id).all()
            total_contacts = len(contacts)
            print(f"📋 Total de contactos encontrados: {total_contacts}")
            
            # Actualizar el total_count de la campaña
            campaign.total_count = total_contacts
            db.session.commit()
            
            if total_contacts == 0:
                print(f"❌ No hay contactos en la lista {campaign.list_id}")
                campaign.status = 'failed'
                db.session.commit()
                return
            
            # Obtener template
            template = db.session.get(EmailTemplate, campaign.template_id)
            if not template:
                print(f"❌ Template {campaign.template_id} no encontrado")
                campaign.status = 'failed'
                db.session.commit()
                return
            
            # USAR SENDGRID PARA ENVÍO REAL
            print(f"📧 Usando SendGrid para envío REAL de emails")
            
            # Crear sender de SendGrid
            sender = SendGridSender()
            
            # Probar conexión con SendGrid
            if not sender.test_connection():
                print(f"❌ Error conectando a SendGrid")
                campaign.status = 'failed'
                db.session.commit()
                return
            
            print(f"✅ Conexión SendGrid exitosa - Iniciando envío real")
            
            # Preparar datos para envío en lote
            emails_data = []
            for contact in contacts:
                emails_data.append({
                    'email': contact.email,
                    'name': contact.name or 'Usuario'
                })
            
            # Enviar emails usando SendGrid
            results = sender.send_bulk_emails(
                emails_data,
                template.subject,
                template.content,
                "El Chicher",
                "el_chicher@hotmail.com"
            )
            
            # Actualizar estadísticas de la campaña
            campaign.sent_count = results['sent']
            campaign.status = 'completed'
            campaign.completed_at = datetime.now(timezone.utc)
            db.session.commit()
            
            print(f"✅ Campaña completada con SendGrid: {results['sent']}/{total_contacts} emails enviados")
            if results['failed'] > 0:
                print(f"⚠️ {results['failed']} emails fallaron")
            
            return
            
    except Exception as e:
        print(f"❌ Error general en send_campaign_emails: {e}")
        if campaign:
            try:
                with app.app_context():
                    campaign.status = 'failed'
                    db.session.commit()
                    print(f"❌ Campaña marcada como fallida debido a error: {e}")
            except Exception as commit_error:
                print(f"❌ Error al marcar campaña como fallida: {commit_error}")

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    # Usar usuario por defecto automáticamente
    default_user = User.query.filter_by(username='admin').first()
    if not default_user:
        return redirect(url_for('dashboard'))
    
    session['user_id'] = default_user.id
    
    if request.method == 'POST':
        default_user.outlook_email = request.form['outlook_email']
        default_user.outlook_password = request.form['outlook_password']
        db.session.commit()
        flash('Configuración actualizada', 'success')
        return redirect(url_for('settings'))
    
    return render_template('settings.html', user=default_user)

@app.route('/api/campaign-status/<int:campaign_id>')
def campaign_status(campaign_id):
    # Usar usuario por defecto automáticamente
    default_user = User.query.filter_by(username='admin').first()
    if not default_user:
        return jsonify({'error': 'No autorizado'}), 401
    
    session['user_id'] = default_user.id
    
    campaign = EmailCampaign.query.get_or_404(campaign_id)
    if campaign.user_id != default_user.id:
        return jsonify({'error': 'Acceso denegado'}), 403
    
    return jsonify({
        'id': campaign.id,
        'status': campaign.status,
        'sent_count': campaign.sent_count,
        'total_count': campaign.total_count,
        'progress': (campaign.sent_count / campaign.total_count * 100) if campaign.total_count > 0 else 0
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
