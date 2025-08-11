#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SISTEMA DE TEMPLATES OPTIMIZADOS PARA EMAILS
============================================

Sistema para crear y gestionar templates de emails con:
- Headers personalizables
- Contenido optimizado para evitar spam
- Diseños profesionales
- Personalización avanzada
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime

class TemplateOptimizado:
    """Template de email optimizado para evitar spam"""
    
    def __init__(self, nombre: str, categoria: str = "General"):
        self.nombre = nombre
        self.categoria = categoria
        self.headers_personalizados = {}
        self.contenido_html = ""
        self.contenido_texto = ""
        self.variables_disponibles = []
        self.creado_en = datetime.now()
        
    def configurar_headers(self, headers: Dict):
        """Configurar headers personalizados para evitar spam"""
        headers_por_defecto = {
            'X-Mailer': 'SendGrid-Professional',
            'X-Priority': '3',
            'X-MSMail-Priority': 'Normal',
            'Importance': 'Normal',
            'X-Campaign': 'EmailCampaign',
            'X-Sent-Date': datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
        }
        
        # Combinar headers por defecto con personalizados
        self.headers_personalizados = {**headers_por_defecto, **headers}
        
    def agregar_header_personalizado(self, key: str, value: str):
        """Agregar un header personalizado específico"""
        self.headers_personalizados[key] = value
        
    def configurar_contenido_html(self, contenido: str):
        """Configurar contenido HTML del template"""
        self.contenido_html = contenido
        self._extraer_variables()
        
    def configurar_contenido_texto(self, contenido: str):
        """Configurar contenido de texto plano del template"""
        self.contenido_texto = contenido
        
    def _extraer_variables(self):
        """Extraer variables disponibles del template"""
        import re
        variables = re.findall(r'\{\{(\w+)\}\}', self.contenido_html)
        self.variables_disponibles = list(set(variables))
        
    def personalizar_contenido(self, datos: Dict) -> str:
        """Personalizar contenido del template con datos del contacto"""
        contenido_personalizado = self.contenido_html
        
        for variable in self.variables_disponibles:
            valor = datos.get(variable, '')
            placeholder = f"{{{{{variable}}}}}"
            contenido_personalizado = contenido_personalizado.replace(placeholder, str(valor))
            
        return contenido_personalizado
    
    def obtener_headers_finales(self, datos_adicionales: Dict = None) -> Dict:
        """Obtener headers finales para el envío"""
        headers = self.headers_personalizados.copy()
        
        if datos_adicionales:
            headers.update(datos_adicionales)
            
        return headers
    
    def validar_template(self) -> List[str]:
        """Validar que el template esté correctamente configurado"""
        errores = []
        
        if not self.contenido_html:
            errores.append("El contenido HTML es requerido")
            
        if not self.nombre:
            errores.append("El nombre del template es requerido")
            
        if not self.headers_personalizados:
            errores.append("Los headers personalizados son requeridos")
            
        return errores
    
    def exportar_template(self, filename: str = None) -> str:
        """Exportar template a archivo JSON"""
        if not filename:
            filename = f"template_{self.nombre}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
        datos_template = {
            'nombre': self.nombre,
            'categoria': self.categoria,
            'headers_personalizados': self.headers_personalizados,
            'contenido_html': self.contenido_html,
            'contenido_texto': self.contenido_texto,
            'variables_disponibles': self.variables_disponibles,
            'creado_en': self.creado_en.isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(datos_template, f, indent=2, ensure_ascii=False)
            
        return filename
    
    @classmethod
    def importar_template(cls, filename: str) -> 'TemplateOptimizado':
        """Importar template desde archivo JSON"""
        with open(filename, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            
        template = cls(datos['nombre'], datos['categoria'])
        template.headers_personalizados = datos['headers_personalizados']
        template.contenido_html = datos['contenido_html']
        template.contenido_texto = datos['contenido_texto']
        template.variables_disponibles = datos['variables_disponibles']
        template.creado_en = datetime.fromisoformat(datos['creado_en'])
        
        return template

class GestorTemplates:
    """Gestor de templates optimizados"""
    
    def __init__(self):
        self.templates = {}
        self.categorias_disponibles = [
            'Newsletter', 'Marketing', 'Notificaciones', 'Promociones',
            'Corporativo', 'Personal', 'Eventos', 'General'
        ]
        
    def crear_template(self, nombre: str, categoria: str = "General") -> TemplateOptimizado:
        """Crear nuevo template"""
        if categoria not in self.categorias_disponibles:
            categoria = "General"
            
        template = TemplateOptimizado(nombre, categoria)
        self.templates[nombre] = template
        
        return template
    
    def obtener_template(self, nombre: str) -> Optional[TemplateOptimizado]:
        """Obtener template por nombre"""
        return self.templates.get(nombre)
    
    def listar_templates(self, categoria: str = None) -> List[TemplateOptimizado]:
        """Listar templates disponibles"""
        if categoria:
            return [t for t in self.templates.values() if t.categoria == categoria]
        return list(self.templates.values())
    
    def eliminar_template(self, nombre: str) -> bool:
        """Eliminar template"""
        if nombre in self.templates:
            del self.templates[nombre]
            return True
        return False
    
    def crear_template_newsletter(self, nombre: str) -> TemplateOptimizado:
        """Crear template de newsletter optimizado"""
        template = self.crear_template(nombre, "Newsletter")
        
        # Headers optimizados para newsletter
        headers_newsletter = {
            'X-Campaign-Type': 'Newsletter',
            'X-Frequency': 'Weekly',
            'X-Unsubscribe': 'Unsubscribe',
            'List-Unsubscribe': '<mailto:unsubscribe@tuempresa.com>',
            'Precedence': 'bulk'
        }
        template.configurar_headers(headers_newsletter)
        
        # Contenido HTML optimizado
        contenido_html = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="format-detection" content="telephone=no">
            <meta name="format-detection" content="date=no">
            <meta name="format-detection" content="address=no">
            <meta name="format-detection" content="email=no">
            <title>Newsletter - {{company_name}}</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff;">
                <!-- Header -->
                <div style="background-color: #2c3e50; color: white; padding: 20px; text-align: center;">
                    <h1 style="margin: 0; font-size: 24px;">{{company_name}}</h1>
                    <p style="margin: 10px 0 0 0; opacity: 0.8;">{{slogan}}</p>
                </div>
                
                <!-- Contenido Principal -->
                <div style="padding: 30px 20px;">
                    <h2 style="color: #2c3e50; margin-top: 0;">¡Hola {{name}}!</h2>
                    
                    <p>Esperamos que estés teniendo un excelente día. Aquí tienes las últimas novedades:</p>
                    
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <h3 style="color: #2c3e50; margin-top: 0;">{{titulo_destacado}}</h3>
                        <p>{{descripcion_destacado}}</p>
                        <a href="{{enlace_destacado}}" style="background-color: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">Leer Más</a>
                    </div>
                    
                    <p>Gracias por ser parte de nuestra comunidad.</p>
                    
                    <p>Saludos,<br><strong>El equipo de {{company_name}}</strong></p>
                </div>
                
                <!-- Footer -->
                <div style="background-color: #34495e; color: white; padding: 20px; text-align: center; font-size: 12px;">
                    <p style="margin: 0 0 10px 0;">© 2025 {{company_name}}. Todos los derechos reservados.</p>
                    <p style="margin: 0;">
                        <a href="{{unsubscribe_link}}" style="color: #bdc3c7; text-decoration: none;">Darse de baja</a> |
                        <a href="{{contact_link}}" style="color: #bdc3c7; text-decoration: none;">Contacto</a>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        template.configurar_contenido_html(contenido_html)
        
        return template
    
    def crear_template_corporativo(self, nombre: str) -> TemplateOptimizado:
        """Crear template corporativo optimizado"""
        template = self.crear_template(nombre, "Corporativo")
        
        # Headers para emails corporativos
        headers_corporativo = {
            'X-Campaign-Type': 'Corporate',
            'X-Company': 'Business',
            'X-Importance': 'High',
            'X-Priority': '1'
        }
        template.configurar_headers(headers_corporativo)
        
        # Contenido corporativo
        contenido_html = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Comunicado Corporativo - {{company_name}}</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #2c3e50; background-color: #ecf0f1;">
            <div style="max-width: 700px; margin: 0 auto; background-color: #ffffff; box-shadow: 0 0 20px rgba(0,0,0,0.1);">
                <!-- Header Corporativo -->
                <div style="background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%); color: white; padding: 30px; text-align: center;">
                    <img src="{{logo_url}}" alt="{{company_name}}" style="max-height: 60px; margin-bottom: 15px;">
                    <h1 style="margin: 0; font-size: 28px; font-weight: 300;">{{company_name}}</h1>
                    <p style="margin: 10px 0 0 0; opacity: 0.9; font-size: 16px;">{{department_name}}</p>
                </div>
                
                <!-- Contenido Principal -->
                <div style="padding: 40px 30px;">
                    <h2 style="color: #2c3e50; margin-top: 0; border-bottom: 3px solid #3498db; padding-bottom: 10px;">
                        {{asunto_principal}}
                    </h2>
                    
                    <p style="font-size: 16px; line-height: 1.8;">Estimado/a {{name}},</p>
                    
                    <div style="background-color: #f8f9fa; border-left: 4px solid #3498db; padding: 20px; margin: 25px 0;">
                        <p style="margin: 0; font-size: 16px;">{{mensaje_principal}}</p>
                    </div>
                    
                    <p>{{contenido_detallado}}</p>
                    
                    <!-- Call to Action -->
                    <div style="text-align: center; margin: 35px 0;">
                        <a href="{{action_link}}" style="background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); color: white; padding: 15px 35px; text-decoration: none; border-radius: 8px; display: inline-block; font-size: 16px; font-weight: bold; box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);">
                            {{action_text}}
                        </a>
                    </div>
                    
                    <p>Si tienes alguna pregunta, no dudes en contactarnos.</p>
                    
                    <p style="margin-top: 30px;">
                        Saludos cordiales,<br>
                        <strong>{{sender_name}}</strong><br>
                        <em>{{sender_title}}</em><br>
                        {{company_name}}
                    </p>
                </div>
                
                <!-- Footer Corporativo -->
                <div style="background-color: #34495e; color: white; padding: 25px; text-align: center;">
                    <div style="margin-bottom: 15px;">
                        <a href="{{website}}" style="color: #bdc3c7; text-decoration: none; margin: 0 10px;">Sitio Web</a>
                        <a href="{{contact_email}}" style="color: #bdc3c7; text-decoration: none; margin: 0 10px;">Contacto</a>
                        <a href="{{privacy_policy}}" style="color: #bdc3c7; text-decoration: none; margin: 0 10px;">Política de Privacidad</a>
                    </div>
                    <p style="margin: 0; font-size: 12px; opacity: 0.8;">
                        © 2025 {{company_name}}. Todos los derechos reservados.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        template.configurar_contenido_html(contenido_html)
        
        return template

def main():
    """Función principal para probar el sistema de templates"""
    print("🧪 PRUEBA DEL SISTEMA DE TEMPLATES OPTIMIZADOS")
    print("=" * 55)
    
    gestor = GestorTemplates()
    
    # Crear template de newsletter
    print("1️⃣ Creando template de newsletter...")
    newsletter = gestor.crear_template_newsletter("Newsletter Semanal")
    
    print(f"   ✅ Template creado: {newsletter.nombre}")
    print(f"   📧 Categoría: {newsletter.categoria}")
    print(f"   🔧 Variables disponibles: {newsletter.variables_disponibles}")
    print(f"   📋 Headers configurados: {len(newsletter.headers_personalizados)}")
    
    # Crear template corporativo
    print("\n2️⃣ Creando template corporativo...")
    corporativo = gestor.crear_template_corporativo("Comunicado Corporativo")
    
    print(f"   ✅ Template creado: {corporativo.nombre}")
    print(f"   📧 Categoría: {corporativo.categoria}")
    print(f"   🔧 Variables disponibles: {corporativo.variables_disponibles}")
    
    # Personalizar contenido
    print("\n3️⃣ Personalizando contenido...")
    datos_prueba = {
        'name': 'El Chicher',
        'company_name': 'Empresa Test',
        'slogan': 'Innovación y Calidad',
        'titulo_destacado': 'Nuevo Producto Lanzado',
        'descripcion_destacado': 'Hemos lanzado nuestro nuevo producto revolucionario',
        'enlace_destacado': 'https://ejemplo.com/producto',
        'unsubscribe_link': 'https://ejemplo.com/unsubscribe',
        'contact_link': 'https://ejemplo.com/contacto'
    }
    
    contenido_personalizado = newsletter.personalizar_contenido(datos_prueba)
    print(f"   ✅ Contenido personalizado generado ({len(contenido_personalizado)} caracteres)")
    
    # Exportar templates
    print("\n4️⃣ Exportando templates...")
    archivo_newsletter = newsletter.exportar_template()
    archivo_corporativo = corporativo.exportar_template()
    
    print(f"   📁 Newsletter exportado: {archivo_newsletter}")
    print(f"   📁 Corporativo exportado: {archivo_corporativo}")
    
    # Validar templates
    print("\n5️⃣ Validando templates...")
    errores_newsletter = newsletter.validar_template()
    errores_corporativo = corporativo.validar_template()
    
    if not errores_newsletter:
        print("   ✅ Newsletter válido")
    else:
        print(f"   ❌ Errores en newsletter: {errores_newsletter}")
        
    if not errores_corporativo:
        print("   ✅ Corporativo válido")
    else:
        print(f"   ❌ Errores en corporativo: {errores_corporativo}")
    
    print("\n🎉 ¡Sistema de templates funcionando correctamente!")
    print(f"📊 Total de templates creados: {len(gestor.templates)}")

if __name__ == "__main__":
    main()
