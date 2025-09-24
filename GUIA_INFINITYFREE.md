# 🚀 GUÍA COMPLETA PARA INFINITYFREE

## 📋 PASOS PARA CONFIGURAR TU PROYECTO EN INFINITYFREE

### **PASO 1: Crear cuenta en InfinityFree**
1. Ve a: **https://infinityfree.net/**
2. Haz clic en **"Get Started"**
3. Completa el registro con:
   - Username único
   - Email válido
   - Contraseña segura
4. Verifica tu cuenta por email

### **PASO 2: Crear tu hosting**
1. Inicia sesión en tu cuenta
2. Haz clic en **"New Website"**
3. Elige un subdominio gratuito:
   - `.epizy.com` (recomendado)
   - `.rf.gd`
   - `.42web.io`
4. Escribe el nombre de tu sitio (ej: `micuenta`)
5. Haz clic en **"Create Website"**

### **PASO 3: Configurar la base de datos MySQL**
1. Ve a **"MySQL Databases"**
2. Haz clic en **"Create Database"**
3. Completa los campos:
   - **Database Name**: `gestor_cuentas` (o el nombre que prefieras)
   - **Username**: `usuario_cuentas` (o el nombre que prefieras)
   - **Password**: Contraseña segura
4. **GUARDA ESTA INFORMACIÓN** - la necesitarás después

### **PASO 4: Configurar tu código**
1. **Edita el archivo `config_infinityfree.py`:**
   ```python
   DB_NAME = 'gestor_cuentas'  # El nombre que pusiste en el paso 3
   DB_USER = 'usuario_cuentas'  # El usuario que pusiste en el paso 3
   DB_PASSWORD = 'tu_contraseña'  # La contraseña que pusiste en el paso 3
   ```

2. **Cambia la SECRET_KEY:**
   ```python
   SECRET_KEY = 'cambia-esta-clave-por-una-segura-y-única'
   ```

### **PASO 5: Subir tu proyecto**
1. Ve a **"File Manager"**
2. Navega a la carpeta **`htdocs`** (carpeta raíz de tu sitio)
3. **Sube estos archivos:**
   - `app.py` ✅
   - `config_infinityfree.py` ✅
   - `requirements_infinityfree.txt` ✅
   - `.htaccess` ✅
   - Carpeta `templates/` ✅
   - Carpeta `static/` ✅

### **PASO 6: Instalar dependencias**
1. Ve a **"Terminal"** en tu panel de control
2. Ejecuta estos comandos:
   ```bash
   cd htdocs
   pip install -r requirements_infinityfree.txt
   ```

### **PASO 7: Crear la base de datos**
1. Ve a **"phpMyAdmin"**
2. Selecciona tu base de datos
3. Ejecuta este comando SQL:
   ```sql
   CREATE DATABASE IF NOT EXISTS gestor_cuentas CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

### **PASO 8: Probar tu aplicación**
1. Ve a tu sitio: `https://micuenta.epizy.com`
2. Deberías ver tu aplicación funcionando
3. **Usuario por defecto:**
   - Username: `admin`
   - Password: `admin123`

## ⚠️ **IMPORTANTE - CAMBIAR DESPUÉS:**
- Cambia la contraseña del usuario admin
- Cambia la SECRET_KEY por una más segura
- Configura HTTPS si es posible

## 🔧 **SOLUCIÓN DE PROBLEMAS:**

### **Error de conexión a la base de datos:**
- Verifica que las credenciales en `config_infinityfree.py` sean correctas
- Asegúrate de que la base de datos esté creada

### **Error 500:**
- Revisa los logs de error en el panel de control
- Verifica que todas las dependencias estén instaladas

### **Página en blanco:**
- Verifica que el archivo `.htaccess` esté en la raíz
- Asegúrate de que `app.py` tenga permisos de ejecución

## 📱 **ACCESO A TU APLICACIÓN:**
- **URL**: `https://tu_nombre.epizy.com`
- **Panel de control**: Desde tu cuenta de InfinityFree
- **Base de datos**: phpMyAdmin desde el panel de control

## 🎯 **PRÓXIMOS PASOS:**
1. Configura un dominio personalizado (opcional)
2. Configura SSL/HTTPS
3. Optimiza el rendimiento
4. Configura backups automáticos

## 📞 **SOPORTE:**
- **Foros de InfinityFree**: Para problemas técnicos
- **Documentación**: Revisa la ayuda del panel de control

---

## ✅ **CHECKLIST FINAL:**
- [ ] Cuenta creada en InfinityFree
- [ ] Hosting configurado
- [ ] Base de datos MySQL creada
- [ ] Archivos subidos a htdocs
- [ ] Dependencias instaladas
- [ ] Aplicación funcionando
- [ ] Usuario admin configurado
- [ ] Contraseñas cambiadas

**¡Tu proyecto estará funcionando en InfinityFree! 🎉**
