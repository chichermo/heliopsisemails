# 🎯 Guía Completa para Configurar App Password de Microsoft

## 📋 PASOS DETALLADOS

### Paso 1: Acceder a la Configuración de Seguridad
1. **Abre tu navegador** y ve a: https://account.microsoft.com/security
2. **Inicia sesión** con tu cuenta de Outlook/Hotmail (`el_chicher@hotmail.com`)
3. **Verifica** que estés en la página correcta

### Paso 2: Habilitar Autenticación de Dos Factores (2FA)
1. **Busca** la sección "Autenticación de dos factores"
2. **Haz clic** en "Configurar" o "Habilitar"
3. **Sigue** las instrucciones para configurar 2FA
4. **Usa** tu teléfono para recibir códigos de verificación

### Paso 3: Crear App Password
1. **Una vez que 2FA esté habilitado**, busca "Contraseñas de aplicación"
2. **Haz clic** en "Crear una nueva contraseña de aplicación"
3. **Selecciona** "Correo" o "Outlook" como aplicación
4. **Anota** la contraseña generada (16 caracteres)

### Paso 4: Usar App Password en el Sistema
1. **Ejecuta** el script de configuración:
   ```bash
   python configurar_credenciales_reales.py
   ```
2. **Ingresa** tu email: `el_chicher@hotmail.com`
3. **Ingresa** la App Password (NO tu contraseña normal)
4. **Confirma** los cambios

## 🔍 VERIFICACIÓN

### ¿Tienes 2FA habilitado?
- Ve a: https://account.microsoft.com/security
- Busca "Autenticación de dos factores"
- Debe mostrar "Activado" o "Habilitado"

### ¿Puedes crear App Password?
- Solo aparece si tienes 2FA habilitado
- Si no ves la opción, primero habilita 2FA

## 🚨 PROBLEMAS COMUNES

### Error: "No veo la opción de App Password"
- **Solución**: Primero debes habilitar 2FA
- Ve a: Seguridad → Autenticación de dos factores

### Error: "Invalid credentials"
- **Causa**: Usando contraseña normal en lugar de App Password
- **Solución**: Usa la App Password de 16 caracteres

### Error: "2FA no funciona"
- **Solución**: Usa un número de teléfono válido
- O configura Microsoft Authenticator

## 📞 SOPORTE

Si tienes problemas:
1. **Verifica** que 2FA esté habilitado
2. **Asegúrate** de usar App Password (no contraseña normal)
3. **Revisa** que el email sea correcto
4. **Prueba** con Microsoft Authenticator

## 🎯 PRÓXIMOS PASOS

Una vez que tengas el App Password:
1. Ejecuta: `python configurar_credenciales_reales.py`
2. Ingresa las credenciales correctas
3. Prueba: `python test_real_connection.py`
4. ¡Disfruta del envío real de emails!
