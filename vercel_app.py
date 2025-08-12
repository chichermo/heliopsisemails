#!/usr/bin/env python3
"""
Sistema de Emails Masivos - Versión Vercel
Mantiene toda la funcionalidad original pero es compatible con Vercel
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
from sendgrid_definitivo import SendGridDefinitive as SendGridSender

# Configuración para Vercel
app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui_2024'

# Usar SQLite en memoria para Vercel (no persistente)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelos de base de datos (simplificados para Vercel)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

class EmailList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

class EmailContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(100))
    list_id = db.Column(db.Integer, db.ForeignKey('email_list.id'), nullable=False)

class EmailTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Crear tablas
with app.app_context():
    db.create_all()
    
    # Crear usuario por defecto
    default_user = User.query.filter_by(username='admin').first()
    if not default_user:
        default_user = User(
            username='admin',
            email='admin@localhost',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(default_user)
        db.session.commit()
    
    # Crear template de ejemplo
    if EmailTemplate.query.filter_by(user_id=default_user.id).count() == 0:
        template1 = EmailTemplate(
            name='Email de Bienvenida',
            subject='¡Bienvenido a Heliopsis Email System!',
            content='''
            <h2>¡Bienvenido!</h2>
            <p>Este es un email de prueba del sistema Heliopsis.</p>
            <p>El sistema está funcionando correctamente en Vercel.</p>
            ''',
            user_id=default_user.id
        )
        db.session.add(template1)
        db.session.commit()

@app.route('/')
def index():
    """Página principal - Dashboard simplificado"""
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    """Dashboard principal"""
    user = User.query.filter_by(username='admin').first()
    lists = EmailList.query.filter_by(user_id=user.id).all()
    templates = EmailTemplate.query.filter_by(user_id=user.id).all()
    
    return render_template('dashboard.html', 
                         user=user, 
                         lists=lists, 
                         templates=templates)

@app.route('/lists')
def lists():
    """Lista de listas de emails"""
    user = User.query.filter_by(username='admin').first()
    lists = EmailList.query.filter_by(user_id=user.id).all()
    return render_template('lists.html', lists=lists)

@app.route('/templates')
def templates():
    """Lista de templates"""
    user = User.query.filter_by(username='admin').first()
    templates = EmailTemplate.query.filter_by(user_id=user.id).all()
    return render_template('templates.html', templates=templates)

# Rutas de autenticación que faltaban
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('¡Login exitoso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('El usuario ya existe', 'error')
        else:
            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password)
            )
            db.session.add(user)
            db.session.commit()
            flash('¡Usuario creado exitosamente!', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('login'))

@app.route('/campaigns')
def campaigns():
    """Lista de campañas"""
    user = User.query.filter_by(username='admin').first()
    return render_template('campaigns.html', user=user)

@app.route('/profile')
def profile():
    """Perfil del usuario"""
    user = User.query.filter_by(username='admin').first()
    return render_template('profile.html', user=user)

@app.route('/api/health')
def health():
    """Endpoint de salud para Vercel"""
    return jsonify({
        "status": "healthy",
        "message": "Heliopsis Email System funcionando en Vercel",
        "version": "2.0.0"
    })

@app.route('/api/send-test')
def send_test():
    """Enviar email de prueba"""
    try:
        # Configurar SendGrid (usar variables de entorno)
        sender = SendGridSender()
        
        # Email de prueba simple
        result = sender.send_email(
            to_email="test@example.com",
            subject="Prueba desde Vercel",
            content="<h1>¡Funciona!</h1><p>El sistema está funcionando en Vercel</p>"
        )
        
        return jsonify({
            "status": "success",
            "message": "Email de prueba enviado correctamente",
            "result": result
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Exportar para Vercel
handler = app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
