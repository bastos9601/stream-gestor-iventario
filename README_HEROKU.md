# 🚀 Despliegue en Heroku

## 🎯 **Ventajas de Heroku:**

✅ **Base de datos PostgreSQL** gratuita y persistente  
✅ **HTTPS automático** y certificados SSL  
✅ **Soporte completo** para Python/Flask  
✅ **Escalabilidad** automática  
✅ **Muy confiable** y profesional  
✅ **Integración con Git** para despliegues automáticos  

## 📋 **PASOS PARA EL DESPLIEGUE**

### **1. Crear Cuenta en Heroku**

1. Ve a [heroku.com](https://heroku.com)
2. Haz clic en **"Sign up"**
3. Completa el registro con tu email
4. Verifica tu cuenta

### **2. Instalar Heroku CLI**

#### **Windows (PowerShell como administrador):**
```bash
winget install --id=Heroku.HerokuCLI
```

#### **macOS:**
```bash
brew tap heroku/brew && brew install heroku
```

#### **Linux:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

### **3. Iniciar Sesión en Heroku CLI**

```bash
heroku login
```

Se abrirá tu navegador para autenticarte.

### **4. Crear Aplicación en Heroku**

```bash
# Navega a tu directorio del proyecto
cd tu-proyecto

# Crear aplicación en Heroku
heroku create tu-gestor-cuentas

# Ver la URL de tu aplicación
heroku info
```

### **5. Agregar Base de Datos PostgreSQL**

```bash
# Agregar base de datos PostgreSQL gratuita
heroku addons:create heroku-postgresql:mini

# Ver información de la base de datos
heroku config:get DATABASE_URL
```

### **6. Configurar Variables de Entorno**

```bash
# Configurar clave secreta
heroku config:set SECRET_KEY="tu_clave_secreta_super_segura_2024"

# Ver todas las variables configuradas
heroku config
```

### **7. Desplegar la Aplicación**

```bash
# Agregar todos los archivos a Git (si no lo has hecho)
git init
git add .
git commit -m "Primer despliegue en Heroku"

# Desplegar en Heroku
git push heroku main

# Si tu rama principal es 'master' en lugar de 'main':
git push heroku master
```

### **8. Ejecutar Migraciones de Base de Datos**

```bash
# Ejecutar migraciones
heroku run python -c "from app_heroku import app, db; app.app_context().push(); db.create_all()"
```

### **9. Abrir la Aplicación**

```bash
# Abrir en el navegador
heroku open
```

## 🔧 **SOLUCIÓN DE PROBLEMAS**

### **Error: "No module named 'gunicorn'"**
```bash
# Instalar gunicorn localmente
pip install gunicorn

# Agregar y hacer commit
git add requirements_heroku.txt
git commit -m "Agregar gunicorn"
git push heroku main
```

### **Error: "Database connection failed"**
```bash
# Verificar que PostgreSQL esté activo
heroku addons:info heroku-postgresql

# Reiniciar la aplicación
heroku restart
```

### **Error: "App not found"**
```bash
# Verificar que estés en la aplicación correcta
heroku apps

# Cambiar a la aplicación correcta
heroku git:remote -a nombre-de-tu-app
```

## 📱 **PROBAR LA APLICACIÓN**

1. **Ve a tu URL de Heroku** (ej: `https://tu-gestor-cuentas.herokuapp.com`)
2. **Credenciales por defecto:**
   - Usuario: `admin`
   - Contraseña: `admin123`

## 🎯 **COMANDOS ÚTILES DE HEROKU**

```bash
# Ver logs en tiempo real
heroku logs --tail

# Ejecutar comando en el servidor
heroku run python

# Reiniciar aplicación
heroku restart

# Ver información de la aplicación
heroku info

# Ver variables de entorno
heroku config

# Abrir aplicación
heroku open
```

## 🔄 **ACTUALIZACIONES FUTURAS**

Para actualizar tu aplicación:

```bash
# Hacer cambios en tu código
# Agregar y hacer commit
git add .
git commit -m "Descripción de los cambios"

# Desplegar cambios
git push heroku main
```

## 📊 **MONITOREO Y MANTENIMIENTO**

```bash
# Ver uso de recursos
heroku ps

# Ver métricas
heroku addons:open heroku-postgresql

# Hacer backup de la base de datos
heroku pg:backups:capture
```

## 🎉 **¡TU APLICACIÓN ESTÁ LISTA!**

Después del despliegue exitoso:

1. **Cambia la contraseña** del usuario admin
2. **Personaliza** la aplicación según tus necesidades
3. **Prueba** todas las funcionalidades
4. **Configura** un dominio personalizado (opcional)

---

**¡Buena suerte con tu despliegue en Heroku! 🚀**
