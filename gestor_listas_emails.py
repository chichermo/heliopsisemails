#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GESTOR AVANZADO DE LISTAS DE EMAILS
===================================

Sistema para:
- Crear y gestionar listas de emails
- Validar emails
- Categorizar contactos
- Importar/exportar listas
- Limpiar emails duplicados
"""

import re
import csv
import json
import sqlite3
from typing import List, Dict, Tuple
from datetime import datetime
import os

class GestorListasEmails:
    """Gestor avanzado de listas de emails"""
    
    def __init__(self, db_path="instance/emails.db"):
        self.db_path = db_path
        self.valid_email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        
    def validar_email(self, email: str) -> bool:
        """Validar formato de email"""
        if not email or not isinstance(email, str):
            return False
        
        email = email.strip().lower()
        
        # Verificar patrón básico
        if not self.valid_email_pattern.match(email):
            return False
        
        # Verificar dominios comunes de spam
        spam_domains = [
            '10minutemail.com', 'tempmail.org', 'guerrillamail.com',
            'mailinator.com', 'yopmail.com', 'trashmail.com'
        ]
        
        domain = email.split('@')[1]
        if domain in spam_domains:
            return False
            
        return True
    
    def categorizar_contacto(self, email: str, name: str = "", company: str = "") -> Dict:
        """Categorizar contacto basado en email y datos"""
        domain = email.split('@')[1].lower()
        
        # Categorías por dominio
        if domain in ['gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com']:
            categoria = 'Personal'
        elif domain in ['tropicana.com', 'empresa.com', 'business.com']:
            categoria = 'Corporativo'
        elif domain in ['edu', 'university.edu', 'college.edu']:
            categoria = 'Educativo'
        elif domain in ['gov', 'gob', 'government']:
            categoria = 'Gubernamental'
        else:
            categoria = 'Otro'
        
        # Prioridad de envío
        if categoria == 'Corporativo':
            prioridad = 'Alta'
        elif categoria == 'Personal':
            prioridad = 'Media'
        else:
            prioridad = 'Baja'
        
        return {
            'categoria': categoria,
            'prioridad': prioridad,
            'dominio': domain,
            'es_valido': self.validar_email(email)
        }
    
    def crear_lista_avanzada(self, nombre: str, descripcion: str = "", 
                            categoria: str = "General") -> int:
        """Crear nueva lista de emails con metadatos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Crear tabla de listas si no existe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS email_lists_advanced (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    category TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_contacts INTEGER DEFAULT 0,
                    valid_contacts INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'active'
                )
            """)
            
            # Insertar nueva lista
            cursor.execute("""
                INSERT INTO email_lists_advanced (name, description, category)
                VALUES (?, ?, ?)
            """, (nombre, descripcion, categoria))
            
            lista_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"✅ Lista '{nombre}' creada con ID: {lista_id}")
            return lista_id
            
        except Exception as e:
            print(f"❌ Error creando lista: {e}")
            return None
    
    def agregar_contactos_a_lista(self, lista_id: int, contactos: List[Dict]) -> Dict:
        """Agregar contactos a una lista con validación"""
        resultados = {
            'total': len(contactos),
            'agregados': 0,
            'duplicados': 0,
            'invalidos': 0,
            'errores': []
        }
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Crear tabla de contactos avanzada si no existe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS email_contacts_advanced (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL,
                    name TEXT,
                    company TEXT,
                    phone TEXT,
                    list_id INTEGER,
                    categoria TEXT,
                    prioridad TEXT,
                    dominio TEXT,
                    es_valido BOOLEAN,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (list_id) REFERENCES email_lists_advanced (id)
                )
            """)
            
            # Crear índice para evitar duplicados
            cursor.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS idx_email_list 
                ON email_contacts_advanced (email, list_id)
            """)
            
            for contacto in contactos:
                try:
                    email = contacto.get('email', '').strip().lower()
                    name = contacto.get('name', '').strip()
                    company = contacto.get('company', '').strip()
                    phone = contacto.get('phone', '').strip()
                    
                    # Validar email
                    if not self.validar_email(email):
                        resultados['invalidos'] += 1
                        continue
                    
                    # Categorizar contacto
                    info_categoria = self.categorizar_contacto(email, name, company)
                    
                    # Intentar insertar contacto
                    try:
                        cursor.execute("""
                            INSERT INTO email_contacts_advanced 
                            (email, name, company, phone, list_id, categoria, prioridad, dominio, es_valido)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            email, name, company, phone, lista_id,
                            info_categoria['categoria'], info_categoria['prioridad'],
                            info_categoria['dominio'], info_categoria['es_valido']
                        ))
                        
                        resultados['agregados'] += 1
                        
                    except sqlite3.IntegrityError:
                        # Email duplicado en esta lista
                        resultados['duplicados'] += 1
                        continue
                        
                except Exception as e:
                    resultados['errores'].append(f"Error con {contacto}: {str(e)}")
                    continue
            
            # Actualizar estadísticas de la lista
            cursor.execute("""
                UPDATE email_lists_advanced 
                SET total_contacts = total_contacts + ?, 
                    valid_contacts = valid_contacts + ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (resultados['agregados'], resultados['agregados'], lista_id))
            
            conn.commit()
            conn.close()
            
            print(f"✅ Contactos agregados: {resultados['agregados']}/{resultados['total']}")
            return resultados
            
        except Exception as e:
            print(f"❌ Error agregando contactos: {e}")
            return resultados
    
    def obtener_contactos_por_categoria(self, lista_id: int, categoria: str = None) -> List[Dict]:
        """Obtener contactos filtrados por categoría"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if categoria:
                cursor.execute("""
                    SELECT * FROM email_contacts_advanced 
                    WHERE list_id = ? AND categoria = ? AND es_valido = 1
                    ORDER BY prioridad DESC, name ASC
                """, (lista_id, categoria))
            else:
                cursor.execute("""
                    SELECT * FROM email_contacts_advanced 
                    WHERE list_id = ? AND es_valido = 1
                    ORDER BY prioridad DESC, name ASC
                """, (lista_id,))
            
            contactos = []
            for row in cursor.fetchall():
                contactos.append({
                    'id': row[0],
                    'email': row[1],
                    'name': row[2],
                    'company': row[3],
                    'phone': row[4],
                    'categoria': row[6],
                    'prioridad': row[7],
                    'dominio': row[8]
                })
            
            conn.close()
            return contactos
            
        except Exception as e:
            print(f"❌ Error obteniendo contactos: {e}")
            return []
    
    def exportar_lista_csv(self, lista_id: int, filename: str = None) -> bool:
        """Exportar lista a archivo CSV"""
        try:
            contactos = self.obtener_contactos_por_categoria(lista_id)
            
            if not filename:
                filename = f"lista_emails_{lista_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['email', 'name', 'company', 'phone', 'categoria', 'prioridad', 'dominio']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for contacto in contactos:
                    # Filtrar solo los campos que queremos exportar
                    contacto_exportar = {
                        'email': contacto.get('email', ''),
                        'name': contacto.get('name', ''),
                        'company': contacto.get('company', ''),
                        'phone': contacto.get('phone', ''),
                        'categoria': contacto.get('categoria', ''),
                        'prioridad': contacto.get('prioridad', ''),
                        'dominio': contacto.get('dominio', '')
                    }
                    writer.writerow(contacto_exportar)
            
            print(f"✅ Lista exportada a: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error exportando lista: {e}")
            return False
    
    def importar_lista_csv(self, lista_id: int, filename: str) -> Dict:
        """Importar contactos desde archivo CSV"""
        try:
            contactos = []
            
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    contactos.append({
                        'email': row.get('email', ''),
                        'name': row.get('name', ''),
                        'company': row.get('company', ''),
                        'phone': row.get('phone', '')
                    })
            
            return self.agregar_contactos_a_lista(lista_id, contactos)
            
        except Exception as e:
            print(f"❌ Error importando lista: {e}")
            return {'total': 0, 'agregados': 0, 'duplicados': 0, 'invalidos': 0, 'errores': [str(e)]}
    
    def limpiar_lista(self, lista_id: int) -> Dict:
        """Limpiar lista eliminando emails inválidos y duplicados"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Eliminar emails inválidos
            cursor.execute("""
                DELETE FROM email_contacts_advanced 
                WHERE list_id = ? AND es_valido = 0
            """, (lista_id,))
            
            invalidos_eliminados = cursor.rowcount
            
            # Eliminar duplicados (mantener el más reciente)
            cursor.execute("""
                DELETE FROM email_contacts_advanced 
                WHERE id NOT IN (
                    SELECT MAX(id) 
                    FROM email_contacts_advanced 
                    WHERE list_id = ? 
                    GROUP BY email
                ) AND list_id = ?
            """, (lista_id, lista_id))
            
            duplicados_eliminados = cursor.rowcount
            
            # Actualizar estadísticas
            cursor.execute("""
                UPDATE email_lists_advanced 
                SET total_contacts = (
                    SELECT COUNT(*) FROM email_contacts_advanced WHERE list_id = ?
                ),
                valid_contacts = (
                    SELECT COUNT(*) FROM email_contacts_advanced 
                    WHERE list_id = ? AND es_valido = 1
                ),
                updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (lista_id, lista_id, lista_id))
            
            conn.commit()
            conn.close()
            
            resultados = {
                'invalidos_eliminados': invalidos_eliminados,
                'duplicados_eliminados': duplicados_eliminados,
                'total_limpiados': invalidos_eliminados + duplicados_eliminados
            }
            
            print(f"✅ Lista limpiada: {resultados['total_limpiados']} contactos eliminados")
            return resultados
            
        except Exception as e:
            print(f"❌ Error limpiando lista: {e}")
            return {}

def main():
    """Función principal para probar el gestor"""
    print("🧪 PRUEBA DEL GESTOR AVANZADO DE LISTAS")
    print("=" * 50)
    
    gestor = GestorListasEmails()
    
    # Crear lista de prueba
    print("1️⃣ Creando lista de prueba...")
    lista_id = gestor.crear_lista_avanzada(
        "Lista de Prueba Avanzada",
        "Lista para probar el sistema optimizado",
        "Marketing"
    )
    
    if lista_id:
        # Agregar contactos de prueba
        print("\n2️⃣ Agregando contactos de prueba...")
        contactos_prueba = [
            {'email': 'el_chicher@hotmail.com', 'name': 'El Chicher', 'company': 'Empresa Test 1', 'phone': '123-456-7890'},
            {'email': 'guillermoromerog@gmail.com', 'name': 'Guillermo Romero', 'company': 'Empresa Test 2', 'phone': '098-765-4321'},
            {'email': 'v.luis.romero@tropicana.com', 'name': 'Luis Romero', 'company': 'Tropicana', 'phone': '555-123-4567'},
            {'email': 'test@invalid-email', 'name': 'Test Inválido', 'company': 'Test', 'phone': '000-000-0000'},
            {'email': 'otro@tropicana.com', 'name': 'Otro Contacto', 'company': 'Tropicana', 'phone': '555-999-8888'}
        ]
        
        resultados = gestor.agregar_contactos_a_lista(lista_id, contactos_prueba)
        
        # Mostrar contactos por categoría
        print("\n3️⃣ Contactos por categoría:")
        categorias = ['Personal', 'Corporativo']
        
        for categoria in categorias:
            contactos = gestor.obtener_contactos_por_categoria(lista_id, categoria)
            print(f"\n📧 {categoria} ({len(contactos)} contactos):")
            for contacto in contactos:
                print(f"   • {contacto['name']} <{contacto['email']}> - {contacto['company']} ({contacto['prioridad']})")
        
        # Exportar lista
        print("\n4️⃣ Exportando lista...")
        gestor.exportar_lista_csv(lista_id)
        
        # Limpiar lista
        print("\n5️⃣ Limpiando lista...")
        gestor.limpiar_lista(lista_id)
        
        print("\n🎉 ¡Gestor de listas funcionando correctamente!")
        
    else:
        print("❌ Error creando lista")

if __name__ == "__main__":
    main()
