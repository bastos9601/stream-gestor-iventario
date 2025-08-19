# 🔐 Sistema de Login - Gestor de Cuentas de Streaming

## 📋 Descripción

Este sistema implementa un **sistema de autenticación completo** para proteger el acceso a tu aplicación de gestión de cuentas de streaming. Ahora todos los usuarios deben iniciar sesión antes de acceder a cualquier funcionalidad.

## ✨ Características del Sistema de Login

### 🔒 **Seguridad**
- **Autenticación obligatoria** para todas las rutas
- **Contraseñas encriptadas** con hash seguro
- **Sesiones persistentes** con opción "Recordarme"
- **Protección CSRF** integrada
- **Redirección automática** a la página solicitada después del login

### 👤 **Gestión de Usuarios**
- **Modelo de usuario** con roles (admin/usuario normal)
- **Campos de usuario**: username, email, contraseña, fecha de registro
- **Sistema de permisos** basado en roles
- **Creación automática** de usuario administrador por defecto

### 🎨 **Interfaz de Usuario**
- **Diseño moderno y responsive** con Bootstrap 5
- **Formulario de login elegante** con gradientes y efectos visuales
- **Mensajes de error/success** con auto-ocultado
- **Navegación mejorada** con menú de usuario
- **Iconos Font Awesome** para mejor UX

## 🚀 Instalación y Configuración

### 1. **Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### 2. **Ejecutar la Aplicación**
```bash
python app.py
```

### 3. **Acceder al Sistema**
- **URL de login**: `http://localhost:5000/login`
- **Usuario por defecto**: `admin`
- **Contraseña por defecto**: `admin123`

## 🔑 Credenciales por Defecto

Al ejecutar la aplicación por primera vez, se crea automáticamente un usuario administrador:

```
👤 Usuario: admin
🔑 Contraseña: admin123
📧 Email: admin@gestor.com
🔐 Rol: Administrador
```

## 👥 Gestión de Usuarios

### **Crear Usuarios Adicionales**

Usa el script incluido para crear más usuarios:

```bash
python crear_usuario.py
```

**Opciones disponibles:**
1. **Crear usuario** - Agregar nuevos usuarios al sistema
2. **Listar usuarios** - Ver todos los usuarios existentes
3. **Salir** - Terminar el script

### **Ejemplo de Creación de Usuario**

```bash
📝 Crear nuevo usuario:
Usuario: juan
Email: juan@empresa.com
Contraseña: miContraseña123
¿Es administrador? (s/n): n

✅ Usuario 'juan' creado exitosamente
   Email: juan@empresa.com
   Admin: No
```

## 🛡️ Seguridad Implementada

### **Protección de Rutas**
Todas las rutas están protegidas con `@login_required`:

- ✅ `/` - Dashboard principal
- ✅ `/cuentas` - Lista de cuentas
- ✅ `/cuentas/nueva` - Agregar cuenta
- ✅ `/cuentas/<id>` - Ver cuenta
- ✅ `/cuentas/<id>/editar` - Editar cuenta
- ✅ `/cuentas/<id>/vender` - Vender cuenta
- ✅ `/cuentas/<id>/eliminar` - Eliminar cuenta
- ✅ `/api/estadisticas` - API estadísticas
- ✅ `/api/cuentas` - API cuentas

### **Rutas Públicas**
- 🔓 `/login` - Formulario de login
- 🔓 `/logout` - Cerrar sesión

## 🎯 Flujo de Autenticación

### **1. Acceso Inicial**
```
Usuario accede a cualquier URL → Redirigido a /login
```

### **2. Proceso de Login**
```
Usuario ingresa credenciales → Validación → Creación de sesión
```

### **3. Acceso Autorizado**
```
Usuario autenticado → Acceso a la página solicitada
```

### **4. Cerrar Sesión**
```
Usuario hace logout → Sesión destruida → Redirigido a /login
```

## 📱 Responsive Design

El sistema de login está optimizado para todos los dispositivos:

- **🖥️ Desktop/Laptop**: Vista completa con efectos visuales
- **📱 Tablet**: Adaptación automática al tamaño de pantalla
- **📱 Móvil**: Diseño optimizado para pantallas táctiles

## 🔧 Personalización

### **Cambiar Contraseña del Admin**
```python
# En app.py, función crear_usuario_admin()
admin.set_password('nueva_contraseña_segura')
```

### **Modificar Estilos del Login**
Edita `templates/login.html` para personalizar:
- Colores y gradientes
- Tipografías
- Efectos visuales
- Layout y espaciado

## 🚨 Solución de Problemas

### **Error: "Usuario no encontrado"**
- Verifica que el usuario existe en la base de datos
- Usa `python crear_usuario.py` para crear usuarios

### **Error: "Contraseña incorrecta"**
- Verifica la contraseña ingresada
- Las contraseñas son case-sensitive

### **Error: "Base de datos no encontrada"**
- Ejecuta `python app.py` para crear la base de datos
- Verifica permisos de escritura en el directorio

### **Problemas de Sesión**
- Limpia cookies del navegador
- Verifica que `SECRET_KEY` esté configurada
- Reinicia la aplicación

## 📊 Monitoreo y Logs

### **Logs de Autenticación**
La aplicación registra automáticamente:
- Intentos de login exitosos
- Intentos de login fallidos
- Cierres de sesión
- Creación de usuarios

### **Verificar Estado del Sistema**
```bash
# Ver usuarios existentes
python crear_usuario.py
# Opción 2: Listar usuarios
```

## 🔮 Próximas Mejoras

- [ ] **Recuperación de contraseña** por email
- [ ] **Verificación en dos pasos** (2FA)
- [ ] **Historial de sesiones** del usuario
- [ ] **Bloqueo de cuentas** después de intentos fallidos
- [ ] **Auditoría de acciones** del usuario
- [ ] **Roles y permisos** más granulares

## 📞 Soporte

Si encuentras algún problema:

1. **Verifica los logs** de la aplicación
2. **Revisa la base de datos** con `python crear_usuario.py`
3. **Reinicia la aplicación** completamente
4. **Verifica las dependencias** con `pip list`

---

**🎉 ¡Tu sistema de gestión de cuentas de streaming ahora está completamente protegido con un sistema de login profesional y seguro!**
