# 👥 Sistema de Usuarios - Gestor de Cuentas de Streaming

## 🎯 Descripción General

Se ha implementado un sistema completo de usuarios con permisos diferenciados que permite:

- **Administradores**: Acceso completo + gestión de usuarios + ver todas las cuentas
- **Usuarios normales**: Gestión de sus propias cuentas (sin ver las de otros usuarios)
- **Aislamiento de datos**: Cada usuario solo ve y gestiona sus propias cuentas
- **Supervisión**: Los administradores pueden ver y gestionar todas las cuentas

## 🔐 Tipos de Usuario

### 👑 Administrador
- ✅ Puede hacer todo lo que hacen los usuarios normales
- ✅ Puede crear, editar y eliminar usuarios
- ✅ Puede ver todas las cuentas de todos los usuarios
- ✅ Puede gestionar el sistema completo
- ✅ Acceso a estadísticas globales

### 👤 Usuario Normal
- ✅ Puede crear, editar y vender sus propias cuentas
- ✅ Puede ver solo sus propias cuentas
- ✅ Puede cambiar su contraseña
- ❌ NO puede gestionar usuarios
- ❌ NO puede ver cuentas de otros usuarios

## 🚀 Instalación y Configuración

### 1. Ejecutar la Migración

```bash
# Migración completa
python migrar_sistema_usuarios.py

# Verificar estado (opcional)
python migrar_sistema_usuarios.py --verificar
```

### 2. Usuario por Defecto

Después de la migración, se crea automáticamente:

- **Usuario**: `admin`
- **Contraseña**: `admin123`
- **Email**: `admin@gestor.com`
- **Rol**: Administrador

⚠️ **IMPORTANTE**: Cambia la contraseña del administrador después del primer inicio de sesión.

## 📱 Funcionalidades del Sistema

### 🔑 Autenticación
- Login/logout seguro
- Sesiones persistentes
- Protección de rutas con `@login_required`

### 👥 Gestión de Usuarios (Solo Administradores)
- **Crear usuarios**: `/usuarios/nuevo`
- **Editar usuarios**: `/usuarios/<id>/editar`
- **Eliminar usuarios**: `/usuarios/<id>/eliminar`
- **Listar usuarios**: `/usuarios`

### 👤 Perfil de Usuario
- **Ver información**: `/perfil`
- **Cambiar contraseña**: `/perfil/cambiar_password`
- **Estadísticas personales**: Cuentas totales, disponibles, vendidas

### 📺 Gestión de Cuentas
- **Crear cuenta**: Solo para el usuario autenticado
- **Editar cuenta**: Solo si es propietario o administrador
- **Ver cuenta**: Solo si es propietario o administrador
- **Vender cuenta**: Solo si es propietario o administrador

## 🗄️ Estructura de la Base de Datos

### Tabla `usuario`
```sql
- id (Primary Key)
- username (Unique)
- email (Unique)
- password_hash
- es_admin (Boolean)
- fecha_creacion
- activo (Boolean)
```

### Tabla `cuenta` (Actualizada)
```sql
- id (Primary Key)
- plataforma
- email
- password
- estado ('Disponible' o 'Vendida')
- fecha_creacion
- fecha_venta
- nombre_comprador
- whatsapp_comprador
- fecha_vencimiento
- usuario_id (Foreign Key a usuario.id)
```

## 🔒 Seguridad y Permisos

### Validaciones Implementadas
- ✅ Verificación de autenticación en todas las rutas protegidas
- ✅ Verificación de permisos de administrador
- ✅ Verificación de propiedad de cuentas
- ✅ Validación de contraseñas seguras
- ✅ Prevención de acceso a cuentas de otros usuarios

### Reglas de Negocio
1. **Usuarios normales** solo pueden acceder a sus propias cuentas
2. **Administradores** pueden acceder a todas las cuentas
3. **No se pueden eliminar usuarios** que tengan cuentas asociadas
4. **Las contraseñas** deben cumplir requisitos mínimos de seguridad

## 📊 Estadísticas y Reportes

### Para Administradores
- Total de cuentas en el sistema
- Estadísticas por usuario
- Cuentas disponibles y vendidas globales
- Últimas cuentas agregadas por todos los usuarios

### Para Usuarios Normales
- Total de sus propias cuentas
- Sus cuentas disponibles y vendidas
- Últimas cuentas agregadas por el usuario

## 🛠️ Comandos Útiles

### Verificar Estado de la Migración
```bash
python migrar_sistema_usuarios.py --verificar
```

### Ejecutar Migración Completa
```bash
python migrar_sistema_usuarios.py
```

### Ejecutar la Aplicación
```bash
python app.py
```

## 🔧 Personalización

### Crear Nuevos Roles
Para agregar nuevos roles, modifica el modelo `Usuario` en `app.py`:

```python
class Usuario(UserMixin, db.Model):
    # ... campos existentes ...
    rol = db.Column(db.String(20), default='usuario')  # Nuevo campo
```

### Agregar Nuevos Permisos
Crea decoradores personalizados en `app.py`:

```python
def requiere_rol(rol_requerido):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.rol != rol_requerido:
                flash('No tienes permisos para acceder a esta página', 'error')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

## 🚨 Solución de Problemas

### Error: "No tienes permisos para acceder a esta página"
- Verifica que el usuario esté autenticado
- Verifica que tenga el rol de administrador si es necesario
- Revisa la configuración de la base de datos

### Error: "Usuario o contraseña incorrectos"
- Verifica que el usuario exista y esté activo
- Verifica que la contraseña sea correcta
- Ejecuta la migración si es la primera vez

### Error: "No tienes permisos para editar esta cuenta"
- Verifica que la cuenta pertenezca al usuario actual
- Verifica que el usuario sea administrador
- Revisa la relación `usuario_id` en la tabla `cuenta`

## 📝 Notas de Desarrollo

### Cambios Principales
1. **Nuevo modelo Usuario** con sistema de roles
2. **Relación uno-a-muchos** entre Usuario y Cuenta
3. **Sistema de permisos** basado en roles
4. **Aislamiento de datos** por usuario
5. **Interfaz de gestión** de usuarios para administradores

### Archivos Modificados
- `app.py`: Lógica principal y modelos
- `templates/base.html`: Navegación y estructura base
- `templates/login.html`: Formulario de autenticación
- `templates/usuarios.html`: Gestión de usuarios
- `templates/nuevo_usuario.html`: Crear usuarios
- `templates/editar_usuario.html`: Editar usuarios
- `templates/perfil.html`: Perfil del usuario

### Archivos Nuevos
- `migrar_sistema_usuarios.py`: Script de migración
- `README_SISTEMA_USUARIOS.md`: Esta documentación

## 🎉 Próximas Mejoras

- [ ] Sistema de auditoría (logs de acciones)
- [ ] Recuperación de contraseñas por email
- [ ] Verificación en dos pasos
- [ ] Roles personalizables
- [ ] Permisos granulares por funcionalidad
- [ ] API REST para integraciones externas

---

**¿Necesitas ayuda?** Revisa los logs de la aplicación y ejecuta el script de verificación para diagnosticar problemas.
