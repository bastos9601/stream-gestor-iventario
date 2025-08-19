# 🚀 Despliegue en InfinityFree

## ⚠️ IMPORTANTE: Limitaciones de InfinityFree

**InfinityFree tiene limitaciones importantes que debes conocer:**

1. **Base de datos**: Solo soporta bases de datos en memoria (se reinicia cada vez)
2. **Archivos**: Máximo 10MB por archivo
3. **Python**: Soporte limitado, solo versiones básicas
4. **HTTPS**: No siempre está disponible
5. **Persistencia**: Los datos se pierden al reiniciar la aplicación

## 📋 Pasos para el Despliegue

### 1. Preparar los Archivos

Asegúrate de tener estos archivos en tu proyecto:

```
📁 Tu_Proyecto/
├── 📄 app_infinityfree.py      # Aplicación principal adaptada
├── 📄 requirements_infinityfree.txt  # Dependencias optimizadas
├── 📄 .htaccess                # Configuración del servidor
├── 📄 config_infinityfree.py   # Configuración específica
├── 📁 templates/               # Plantillas HTML
├── 📁 static/                  # Archivos estáticos (CSS, JS, imágenes)
└── 📄 README_INFINITYFREE.md   # Este archivo
```

### 2. Crear Cuenta en InfinityFree

1. Ve a [infinityfree.net](https://infinityfree.net)
2. Crea una cuenta gratuita
3. Verifica tu email
4. Inicia sesión en el panel de control

### 3. Crear un Sitio Web

1. En el panel de control, haz clic en **"Crear Sitio Web"**
2. Elige un subdominio (ej: `tusitio.infinityfreeapp.com`)
3. Selecciona **"Python"** como tipo de sitio
4. Completa la información del sitio

### 4. Subir Archivos

#### Opción A: Subida Manual (Recomendada)

1. **Comprime tu proyecto** en un archivo ZIP
2. **Sube el ZIP** al panel de control de InfinityFree
3. **Extrae el ZIP** en el servidor
4. **Elimina el archivo ZIP** para ahorrar espacio

#### Opción B: Subida por FTP

1. Obtén las credenciales FTP del panel de control
2. Usa un cliente FTP (FileZilla, WinSCP)
3. Sube todos los archivos a la carpeta `htdocs`

### 5. Configurar la Aplicación

1. **Renombra** `app_infinityfree.py` a `index.py` (opcional)
2. **Verifica** que el archivo `.htaccess` esté en la raíz
3. **Asegúrate** de que `requirements_infinityfree.txt` esté presente

### 6. Instalar Dependencias

1. En el panel de control, ve a **"Python"**
2. Haz clic en **"Instalar Paquetes"**
3. Copia y pega el contenido de `requirements_infinityfree.txt`
4. Haz clic en **"Instalar"**

### 7. Configurar Variables de Entorno (Opcional)

Si InfinityFree lo permite:

1. Ve a **"Variables de Entorno"**
2. Agrega:
   - `SECRET_KEY`: Tu clave secreta personalizada
   - `FLASK_ENV`: `production`

### 8. Probar la Aplicación

1. Ve a tu sitio web
2. **Credenciales por defecto:**
   - Usuario: `admin`
   - Contraseña: `admin123`

## 🔧 Solución de Problemas

### Error: "Module not found"
- Verifica que las dependencias estén instaladas
- Usa versiones compatibles de Python

### Error: "Permission denied"
- Verifica que el archivo `.htaccess` esté presente
- Asegúrate de que los permisos sean correctos

### Error: "Database error"
- La base de datos en memoria se reinicia automáticamente
- Es normal en InfinityFree

### La aplicación no carga
- Verifica que `app_infinityfree.py` esté en la raíz
- Revisa los logs de error en el panel de control

## 📱 Características de la Aplicación

✅ **Funcionalidades disponibles:**
- Login/Logout de usuarios
- Gestión de cuentas de streaming
- Panel de administración
- API REST para cuentas
- Interfaz responsive

❌ **Limitaciones en InfinityFree:**
- Los datos se pierden al reiniciar
- No hay persistencia de archivos
- Rendimiento limitado
- Sin HTTPS garantizado

## 🚀 Alternativas Recomendadas

Si necesitas **persistencia de datos** y **mejor rendimiento**, considera:

1. **Render** (gratuito, con base de datos PostgreSQL)
2. **Railway** (gratuito, fácil de usar)
3. **Heroku** (gratuito limitado, muy confiable)
4. **Vercel** (gratuito, excelente para aplicaciones web)

## 📞 Soporte

Si tienes problemas:

1. Revisa los logs en el panel de control de InfinityFree
2. Verifica que todos los archivos estén subidos correctamente
3. Asegúrate de que las dependencias estén instaladas
4. Contacta al soporte de InfinityFree si es necesario

## 🎯 Próximos Pasos

Después del despliegue exitoso:

1. **Cambia la contraseña** del usuario admin
2. **Personaliza** la aplicación según tus necesidades
3. **Prueba** todas las funcionalidades
4. **Considera** migrar a una plataforma más robusta si necesitas persistencia

---

**¡Buena suerte con tu despliegue! 🎉**
