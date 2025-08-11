# 🚀 Instrucciones de Ejecución - Sistema de Emails Masivos

## 📋 Opciones de Ejecución

### **Opción 1: Script de Inicio Rápido (Recomendado)**

#### Para Windows:
1. **Doble clic en `iniciar_sistema.bat`**
   - Se abrirá una ventana con menú interactivo
   - Creará automáticamente el archivo `.env` si no existe
   - Te guiará paso a paso

#### Para PowerShell:
1. **Ejecutar `iniciar_sistema.ps1`**
   ```powershell
   .\iniciar_sistema.ps1
   ```

### **Opción 2: Ejecutable (Más Avanzado)**

1. **Crear el ejecutable:**
   ```bash
   python build_executable.py
   ```

2. **Usar el ejecutable:**
   - Doble clic en `SistemaEmailsMasivos.bat`
   - O ejecutar directamente `SistemaEmailsMasivos.exe`

### **Opción 3: Línea de Comandos (Para Usuarios Avanzados)**

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar credenciales:**
   - Copiar `env_example.txt` a `.env`
   - Editar `.env` con tus credenciales

3. **Ejecutar el sistema:**
   ```bash
   # Modo de prueba
   python main.py --test
   
   # Envío completo
   python main.py
   
   # Crear archivos de ejemplo
   python main.py --create-sample
   ```

## 🎯 Pasos Detallados

### **Paso 1: Configuración Inicial**

1. **Crear archivo `.env`:**
   ```bash
   # Copiar el archivo de ejemplo
   copy env_example.txt .env
   ```

2. **Editar `.env` con tus credenciales:**
   ```env
   OUTLOOK_EMAIL=tu_email@outlook.com
   OUTLOOK_PASSWORD=tu_password
   ```

### **Paso 2: Preparar Datos**

1. **Editar lista de emails (`emails.csv`):**
   ```csv
   email,name,empresa,telefono
   juan@ejemplo.com,Juan Pérez,Empresa A,123456789
   maria@ejemplo.com,María García,Empresa B,987654321
   ```

2. **Personalizar template (`templates/template_ejemplo.html`):**
   - Editar el contenido HTML
   - Usar variables como `{{name}}`, `{{empresa}}`

### **Paso 3: Ejecutar Sistema**

#### **Modo de Prueba (Recomendado para empezar):**
```bash
python main.py --test
```

#### **Envío Completo:**
```bash
python main.py
```

## 🛠️ Solución de Problemas

### **Error: Python no encontrado**
```bash
# Instalar Python desde https://python.org
# Asegurarse de marcar "Add to PATH" durante la instalación
```

### **Error: Dependencias no instaladas**
```bash
pip install -r requirements.txt
```

### **Error: Archivo .env no encontrado**
```bash
# Crear manualmente el archivo .env
copy env_example.txt .env
# Editar con tus credenciales
```

### **Error: Credenciales incorrectas**
- Verificar que el email y contraseña sean correctos
- Asegurarse de que la autenticación de aplicaciones esté habilitada
- Usar contraseña de aplicación si tienes 2FA activado

## 📁 Estructura de Archivos

```
mails/
├── 📄 iniciar_sistema.bat          # Launcher para Windows
├── 📄 iniciar_sistema.ps1          # Launcher para PowerShell
├── 📄 build_executable.py          # Script para crear ejecutable
├── 📄 main.py                      # Script principal
├── 📄 email_sender.py              # Clase de envío
├── 📄 config.py                    # Configuración
├── 📄 requirements.txt             # Dependencias
├── 📄 .env                         # Credenciales (crear)
├── 📄 emails.csv                   # Lista de emails
├── 📁 templates/                   # Templates HTML
│   └── 📄 template_ejemplo.html
└── 📄 README.md                    # Documentación
```

## 🎨 Características del Sistema

### **✅ Funcionalidades**
- Envío masivo de emails (400+)
- Control de rate automático
- Personalización de contenido
- Logging completo
- Modo de prueba
- Interfaz intuitiva

### **🔒 Seguridad**
- Credenciales en archivo .env
- Control de rate para evitar spam
- Delays variables y aleatorios
- Pausas por batch

### **📊 Capacidad**
- Mínimo: 400+ emails por sesión
- Rate recomendado: 50 emails/hora
- Configuración flexible

## 🚀 Comandos Rápidos

```bash
# Inicio rápido con menú
iniciar_sistema.bat

# Modo de prueba
python main.py --test

# Envío completo
python main.py

# Crear archivos de ejemplo
python main.py --create-sample

# Ver ayuda
python main.py --help
```

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en `email_sender.log`
2. Verifica que Python esté instalado correctamente
3. Asegúrate de que las credenciales sean correctas
4. Consulta la documentación en `README.md`

¡El sistema está listo para usar! 🎯
