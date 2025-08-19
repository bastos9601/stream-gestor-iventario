# 🚀 Despliegue en Render - Gestor de Cuentas de Streaming

## **📋 Requisitos Previos**

- ✅ Cuenta en [Render.com](https://render.com)
- ✅ Base de datos PostgreSQL 17 creada en Render
- ✅ Nombre de la base de datos: `gestor-cuentas-db`

## **🔧 Configuración en Render**

### **1. Crear Base de Datos PostgreSQL**

1. **Ve a tu dashboard de Render**
2. **Clic en "New +" → "PostgreSQL"**
3. **Configuración:**
   - **Name:** `gestor-cuentas-db`
   - **Database:** `gestor_cuentas_db`
   - **User:** `gestor_cuentas_user`
   - **Plan:** Free (o el que prefieras)
   - **Region:** La más cercana a ti

### **2. Crear Servicio Web**

1. **Clic en "New +" → "Web Service"**
2. **Conecta tu repositorio de GitHub**
3. **Configuración:**
   - **Name:** `gestor-cuentas-stream`
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

### **3. Configurar Variables de Entorno**

En tu servicio web, agrega estas variables:

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `SECRET_KEY` | `tu_clave_super_secreta_aqui` | Clave secreta para Flask |
| `DATABASE_URL` | `${{gestor-cuentas-db.DATABASE_URL}}` | URL de la base de datos |

## **📁 Archivos de Configuración**

### **Archivos Creados/Modificados:**

- ✅ `requirements.txt` - Dependencias de Python
- ✅ `render.yaml` - Configuración automática de Render
- ✅ `Procfile` - Comando de inicio para Render
- ✅ `runtime.txt` - Versión de Python
- ✅ `migrar_postgresql.py` - Script de migración
- ✅ `app.py` - Configuración de PostgreSQL

## **🚀 Pasos para el Despliegue**

### **1. Subir Código a GitHub**

```bash
git add .
git commit -m "Preparado para Render con PostgreSQL"
git push origin main
```

### **2. Conectar en Render**

1. **Conecta tu repositorio de GitHub**
2. **Render detectará automáticamente la configuración**
3. **Se creará el servicio web automáticamente**

### **3. Ejecutar Migración (Opcional)**

Si quieres ejecutar la migración manualmente:

```bash
# En la consola de Render o localmente
python migrar_postgresql.py
```

## **🔍 Verificación del Despliegue**

### **1. Verificar Base de Datos**
- ✅ Conexión establecida
- ✅ Tablas creadas
- ✅ Usuario admin creado

### **2. Verificar Aplicación Web**
- ✅ Página de login accesible
- ✅ Registro de usuarios funcionando
- ✅ Gestión de cuentas funcionando

### **3. Verificar Funcionalidades**
- ✅ Agregar cuentas con plataformas personalizadas
- ✅ Vender cuentas con datos del comprador
- ✅ Botones de WhatsApp funcionando
- ✅ Recordatorios de vencimiento

## **📱 Acceso a la Aplicación**

### **URLs de Acceso:**
- **Aplicación Web:** `https://gestor-cuentas-stream.onrender.com`
- **Login por defecto:**
  - **Usuario:** `admin`
  - **Contraseña:** `admin123`

## **⚠️ Notas Importantes**

### **Plan Gratuito de Render:**
- ⏰ **Sleep después de 15 minutos** de inactividad
- 🔄 **Reinicio automático** al recibir tráfico
- 📊 **Límites de uso** mensual

### **Base de Datos PostgreSQL:**
- 💾 **Persistencia de datos** garantizada
- 🔒 **Backup automático** incluido
- 📈 **Escalabilidad** disponible

## **🆘 Solución de Problemas**

### **Error de Conexión a Base de Datos:**
1. Verificar que `DATABASE_URL` esté configurada
2. Verificar que la base de datos esté activa
3. Ejecutar script de migración

### **Error de Dependencias:**
1. Verificar `requirements.txt`
2. Verificar versión de Python en `runtime.txt`
3. Revisar logs de build en Render

### **Error de Aplicación:**
1. Revisar logs en tiempo real
2. Verificar variables de entorno
3. Verificar configuración de `app.py`

## **🎯 Próximos Pasos**

1. **Desplegar en Render**
2. **Probar todas las funcionalidades**
3. **Configurar dominio personalizado (opcional)**
4. **Configurar backup automático**
5. **Monitorear rendimiento**

---

**¡Tu aplicación está lista para ser desplegada en Render con PostgreSQL! 🎉**
