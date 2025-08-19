# Gestor de Cuentas de Streaming

Un sistema completo para gestionar inventario de cuentas de streaming, ideal para mantener un stock organizado y facilitar la venta posterior.

## 🚀 Características

- **Gestión de Inventario**: Agregar, listar y buscar cuentas
- **Control de Estado**: Seguimiento de cuentas disponibles y vendidas
- **Base de Datos SQLite**: Almacenamiento persistente y confiable
- **Interfaz de Línea de Comandos**: Fácil de usar con menús intuitivos
- **Estadísticas en Tiempo Real**: Resumen del inventario y valor total
- **Filtros Avanzados**: Búsqueda por plataforma y estado
- **Historial Completo**: Fechas de compra y venta

## 📋 Requisitos

- Python 3.6 o superior
- pip (gestor de paquetes de Python)

## 🛠️ Instalación

1. **Clona o descarga el proyecto**
2. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Uso

### Ejecutar el programa:
```bash
python gestor_cuentas.py
```

### Funcionalidades disponibles:

1. **Agregar nueva cuenta**: Ingresa plataforma, email, contraseña, precio y notas
2. **Listar cuentas disponibles**: Ver solo las cuentas en stock
3. **Listar todas las cuentas**: Ver el inventario completo con estados
4. **Buscar cuenta por email**: Encontrar una cuenta específica
5. **Vender cuenta**: Marcar una cuenta como vendida
6. **Ver estadísticas**: Resumen del inventario y valor total
7. **Salir**: Cerrar el programa

## 🗄️ Estructura de la Base de Datos

La aplicación crea automáticamente una base de datos SQLite con la siguiente estructura:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Identificador único (auto-incremento) |
| plataforma | TEXT | Nombre de la plataforma (Netflix, Disney+, etc.) |
| email | TEXT | Email de la cuenta (único) |
| password | TEXT | Contraseña de la cuenta |
| estado | TEXT | Estado actual (disponible/vendida) |
| precio | REAL | Precio de venta |
| fecha_compra | DATE | Fecha de adquisición |
| fecha_venta | DATE | Fecha de venta (NULL si disponible) |
| notas | TEXT | Notas adicionales |
| created_at | TIMESTAMP | Fecha de creación del registro |

## 💡 Ejemplos de Uso

### Agregar una cuenta de Netflix:
- Plataforma: Netflix
- Email: usuario@ejemplo.com
- Contraseña: contraseña123
- Precio: 15.99
- Notas: Cuenta premium 4K

### Vender una cuenta:
- Selecciona opción 5
- Ingresa el email de la cuenta
- La cuenta se marca automáticamente como vendida

## 🔍 Filtros y Búsquedas

- **Por estado**: Solo disponibles, solo vendidas, o todas
- **Por plataforma**: Filtrar por servicio específico
- **Por email**: Búsqueda exacta de cuentas

## 📊 Estadísticas

El sistema proporciona estadísticas en tiempo real:
- Total de cuentas en inventario
- Cuentas disponibles para venta
- Cuentas ya vendidas
- Valor total del inventario disponible
- Distribución por plataforma

## 🛡️ Seguridad

- Las contraseñas se almacenan en texto plano (considera encriptar para producción)
- Base de datos local (no se comparte información)
- Validación de datos de entrada

## 🚧 Limitaciones Actuales

- No incluye encriptación de contraseñas
- Interfaz solo de línea de comandos
- No incluye sistema de usuarios múltiples

## 🔮 Futuras Mejoras

- [ ] Interfaz gráfica (GUI)
- [ ] Encriptación de contraseñas
- [ ] Sistema de usuarios y permisos
- [ ] Exportación de datos (CSV, Excel)
- [ ] Backup automático de la base de datos
- [ ] Notificaciones de stock bajo
- [ ] Historial de cambios y auditoría

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para sugerencias y mejoras.

## 📞 Soporte

Si tienes problemas o preguntas, por favor abre un issue en el repositorio del proyecto.

---

**¡Disfruta gestionando tu inventario de cuentas de streaming de manera eficiente!** 🎬✨
