# 🔧 Guía de Configuración - Sistema de Emails Masivos

## 📋 Pasos para Configurar tu Cuenta

### **Paso 1: Preparar tu Cuenta de Outlook**

#### **1.1 Habilitar Autenticación de Aplicaciones**

1. **Ve a tu cuenta de Microsoft:**
   - Abre https://account.microsoft.com
   - Inicia sesión con tu cuenta de Outlook

2. **Activar autenticación de dos factores:**
   - Ve a "Seguridad" → "Seguridad avanzada"
   - Activa "Verificación en dos pasos"

3. **Generar contraseña de aplicación:**
   - Ve a "Seguridad" → "Contraseñas de aplicación"
   - Selecciona "Crear una nueva contraseña de aplicación"
   - Elige "Correo" como aplicación
   - Copia la contraseña generada (16 caracteres)

#### **1.2 Verificar Permisos de Envío**

1. **Verificar que la cuenta no esté restringida:**
   - Ve a https://outlook.live.com
   - Verifica que puedas enviar emails normalmente
   - Asegúrate de que no haya límites de envío activos

2. **Configurar límites de envío (opcional):**
   - Ve a Configuración → Ver toda la configuración de Outlook
   - Busca "Límites de envío" o "Envío de correo"

### **Paso 2: Configurar el Archivo .env**

#### **2.1 Editar el Archivo .env**

1. **Abrir el archivo .env:**
   ```bash
   # En Windows (Notepad)
   notepad .env
   
   # O en cualquier editor de texto
   code .env
   ```

2. **Configurar tus credenciales:**
   ```env
   # Configuración de Outlook
   OUTLOOK_EMAIL=tu_email_real@outlook.com
   OUTLOOK_PASSWORD=tu_contraseña_de_aplicacion
   
   # Configuración de envío
   MAX_EMAILS_PER_HOUR=50
   DELAY_BETWEEN_EMAILS=30
   BATCH_SIZE=10
   
   # Configuración de contenido
   DEFAULT_SUBJECT=Mensaje importante
   DEFAULT_SENDER_NAME=Tu Nombre Real
   
   # Configuración de archivos
   EMAILS_FILE=emails.csv
   TEMPLATES_DIR=templates
   LOG_FILE=email_sender.log
   ```

#### **2.2 Ejemplo de Configuración Completa**

```env
# Configuración de Outlook
OUTLOOK_EMAIL=miempresa@outlook.com
OUTLOOK_PASSWORD=abcd1234efgh5678

# Configuración de envío
MAX_EMAILS_PER_HOUR=50
DELAY_BETWEEN_EMAILS=30
BATCH_SIZE=10

# Configuración de contenido
DEFAULT_SUBJECT=Información importante de Mi Empresa
DEFAULT_SENDER_NAME=Juan Pérez - Mi Empresa

# Configuración de archivos
EMAILS_FILE=emails.csv
TEMPLATES_DIR=templates
LOG_FILE=email_sender.log
```

### **Paso 3: Verificar la Configuración**

#### **3.1 Probar la Conexión**

1. **Ejecutar modo de prueba:**
   ```bash
   python main.py --test
   ```

2. **Verificar logs:**
   - Revisar el archivo `email_sender.log`
   - Buscar mensajes de error o éxito

#### **3.2 Solución de Problemas Comunes**

##### **Error: "Invalid credentials"**
- Verificar que el email sea correcto
- Usar contraseña de aplicación, no la contraseña normal
- Asegurarse de que la autenticación de aplicaciones esté habilitada

##### **Error: "Account locked"**
- Verificar que la cuenta no esté bloqueada
- Esperar 24 horas si se excedieron los límites
- Contactar soporte de Microsoft si es necesario

##### **Error: "Rate limit exceeded"**
- Reducir `MAX_EMAILS_PER_HOUR` en el archivo .env
- Aumentar `DELAY_BETWEEN_EMAILS`
- Usar pausas más largas entre envíos

### **Paso 4: Configuración Avanzada**

#### **4.1 Optimizar para Evitar Spam**

```env
# Configuración conservadora (recomendada)
MAX_EMAILS_PER_HOUR=30
DELAY_BETWEEN_EMAILS=45
BATCH_SIZE=5

# Configuración agresiva (solo si es necesario)
MAX_EMAILS_PER_HOUR=100
DELAY_BETWEEN_EMAILS=20
BATCH_SIZE=15
```

#### **4.2 Personalizar Contenido**

1. **Editar template:**
   - Abrir `templates/template_ejemplo.html`
   - Personalizar con tu información
   - Usar variables como `{{name}}`, `{{empresa}}`

2. **Configurar asunto y remitente:**
   ```env
   DEFAULT_SUBJECT=Información importante de [Tu Empresa]
   DEFAULT_SENDER_NAME=Tu Nombre - [Tu Empresa]
   ```

### **Paso 5: Verificación Final**

#### **5.1 Checklist de Configuración**

- [ ] Cuenta de Outlook configurada
- [ ] Autenticación de aplicaciones habilitada
- [ ] Contraseña de aplicación generada
- [ ] Archivo .env creado y configurado
- [ ] Credenciales correctas en .env
- [ ] Modo de prueba ejecutado exitosamente
- [ ] Logs verificados sin errores
- [ ] Template personalizado
- [ ] Lista de emails preparada

#### **5.2 Comandos de Verificación**

```bash
# Verificar configuración
python main.py --help

# Probar conexión
python main.py --test

# Ver logs
type email_sender.log
```

### **🚨 Notas Importantes**

1. **Seguridad:**
   - Nunca compartas tu archivo .env
   - Usa contraseñas de aplicación, no contraseñas normales
   - Mantén tu cuenta segura

2. **Límites:**
   - Respeta los límites de envío de Outlook
   - No excedas 50 emails por hora por defecto
   - Usa delays apropiados

3. **Contenido:**
   - Evita palabras spam en asuntos y contenido
   - Incluye información de contacto real
   - Usa templates profesionales

### **📞 Soporte**

Si tienes problemas:

1. **Revisar logs:** `email_sender.log`
2. **Verificar credenciales:** Archivo .env
3. **Probar conexión:** `python main.py --test`
4. **Consultar documentación:** `README.md`

¡Tu cuenta está lista para enviar emails masivos! 🎯
