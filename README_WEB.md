# 🌐 Sistema de Emails Masivos - Versión Web

Una interfaz web moderna y fácil de usar para el envío de emails masivos a través de Outlook, similar a PoMMo pero con una interfaz más moderna y funcional.

## ✨ Características

- 🎨 **Interfaz web moderna** con Bootstrap 5 y Font Awesome
- 👤 **Sistema de usuarios** con registro y login
- 📧 **Gestión de listas** de emails con importación masiva
- 📝 **Templates personalizables** con variables dinámicas
- 🚀 **Campañas de envío** con seguimiento en tiempo real
- ⚙️ **Configuración fácil** de credenciales de Outlook
- 📊 **Dashboard intuitivo** con estadísticas
- 🔒 **Seguridad** con contraseñas de aplicación
- 📱 **Responsive design** para móviles y tablets

## 🚀 Instalación Rápida

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Iniciar la Aplicación

```bash
python iniciar_web.py
```

O directamente:

```bash
python app.py
```

### 3. Acceder a la Aplicación

Abre tu navegador y ve a: **http://localhost:5000**

## 📋 Requisitos

- Python 3.8+
- Cuenta de Outlook con autenticación de aplicaciones habilitada
- Navegador web moderno

## 🎯 Primeros Pasos

### 1. Crear Cuenta

1. Ve a http://localhost:5000
2. Haz clic en "Regístrate aquí"
3. Completa el formulario de registro
4. Inicia sesión con tus credenciales

### 2. Configurar Outlook

1. Ve a "Configuración" en el menú lateral
2. Sigue las instrucciones para generar una contraseña de aplicación
3. Guarda tu email y contraseña de aplicación

### 3. Crear Lista de Emails

1. Ve a "Listas de Emails"
2. Haz clic en "Nueva Lista"
3. Ingresa el nombre de la lista
4. Agrega los emails en formato: `email@ejemplo.com, Nombre, Empresa, Teléfono`

### 4. Crear Template

1. Ve a "Templates"
2. Haz clic en "Nuevo Template"
3. Completa el nombre, asunto y contenido
4. Usa variables como `{{ name }}`, `{{ email }}`, `{{ company }}`, `{{ phone }}`

### 5. Crear y Ejecutar Campaña

1. Ve a "Campañas"
2. Haz clic en "Nueva Campaña"
3. Selecciona el template y la lista
4. Haz clic en "Iniciar" para comenzar el envío

## 🔧 Configuración de Outlook

### Habilitar Autenticación de Aplicaciones

1. Ve a [account.microsoft.com](https://account.microsoft.com)
2. Inicia sesión con tu cuenta de Outlook
3. Ve a "Seguridad" → "Seguridad avanzada"
4. Activa "Verificación en dos pasos" si no está activada

### Generar Contraseña de Aplicación

1. Ve a "Seguridad" → "Contraseñas de aplicación"
2. Selecciona "Crear una nueva contraseña de aplicación"
3. Elige "Correo" como aplicación
4. Copia la contraseña generada (16 caracteres)
5. Pégala en la configuración de la aplicación

## 📊 Funcionalidades

### Dashboard
- Estadísticas de listas, templates y campañas
- Campañas recientes con progreso
- Acciones rápidas

### Gestión de Listas
- Crear listas de emails
- Importar contactos masivamente
- Ver estadísticas de contactos

### Templates
- Crear templates HTML personalizables
- Variables dinámicas para personalización
- Vista previa de templates

### Campañas
- Crear campañas de envío
- Seguimiento en tiempo real
- Estadísticas de envío
- Pausar/reanudar campañas

### Configuración
- Configurar credenciales de Outlook
- Gestión de contraseñas de aplicación
- Ayuda integrada

## 🎨 Variables de Personalización

En los templates puedes usar estas variables:

- `{{ name }}` - Nombre del destinatario
- `{{ email }}` - Email del destinatario
- `{{ company }}` - Empresa del destinatario
- `{{ phone }}` - Teléfono del destinatario

## 🔒 Seguridad

- Contraseñas hasheadas con Werkzeug
- Sesiones seguras
- Contraseñas de aplicación para Outlook
- Validación de datos
- Protección CSRF

## 📱 Diseño Responsive

La aplicación está optimizada para:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Móvil (320px - 767px)

## 🛠️ Desarrollo

### Estructura del Proyecto

```
mails/
├── app.py                 # Aplicación principal Flask
├── config.py             # Configuración
├── email_sender.py       # Lógica de envío de emails
├── templates/            # Plantillas HTML
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── lists.html
│   ├── templates.html
│   ├── campaigns.html
│   └── settings.html
├── static/               # Archivos estáticos
├── logs/                 # Logs de la aplicación
├── emails.db            # Base de datos SQLite
└── requirements.txt     # Dependencias
```

### Ejecutar en Desarrollo

```bash
# Modo desarrollo
export FLASK_ENV=development
python app.py

# O con debug
python -c "from app import app; app.run(debug=True, host='0.0.0.0', port=5000)"
```

## 🐛 Solución de Problemas

### Error de Conexión a Outlook

1. Verifica que tu cuenta tenga autenticación de aplicaciones habilitada
2. Asegúrate de usar una contraseña de aplicación, no tu contraseña normal
3. Verifica que el email esté correctamente escrito

### Error de Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Error de Base de Datos

```bash
# Eliminar base de datos corrupta
rm emails.db
# Reiniciar aplicación
python app.py
```

## 📞 Soporte

Si tienes problemas:

1. Verifica que todas las dependencias estén instaladas
2. Asegúrate de que tu cuenta de Outlook esté configurada correctamente
3. Revisa los logs en la consola
4. Verifica que el puerto 5000 esté disponible

## 🎉 ¡Listo!

¡Tu sistema de emails masivos está listo para usar! 

- 🌐 **Accede a:** http://localhost:5000
- 👤 **Regístrate** y crea tu primera cuenta
- ⚙️ **Configura** tu cuenta de Outlook
- 📧 **Crea** tu primera lista y template
- 🚀 **Lanza** tu primera campaña

¡Disfruta enviando emails masivos de forma profesional y fácil!
