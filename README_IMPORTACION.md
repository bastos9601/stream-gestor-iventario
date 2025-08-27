# Funcionalidad de Importación de Cuentas

## Descripción

Se ha implementado la funcionalidad para importar cuentas vendidas y disponibles desde archivos de texto (.txt) que han sido exportados previamente desde la aplicación.

## Características

### ✅ Funcionalidades Implementadas

1. **Importar Cuentas Vendidas**
   - Botón amarillo en la interfaz principal
   - Modal con instrucciones claras
   - Validación de archivos .txt
   - Prevención de duplicados

2. **Importar Cuentas Disponibles**
   - Botón azul en la interfaz principal
   - Modal con instrucciones claras
   - Validación de archivos .txt
   - Prevención de duplicados



3. **Procesamiento Inteligente**
   - Análisis automático del formato de archivo
   - Conversión de fechas (dd/mm/yyyy → yyyy-mm-dd)
   - Extracción de precios (con símbolo $)
   - Manejo de campos opcionales

4. **Seguridad y Validación**
   - Verificación de duplicados por email
   - Rollback en caso de errores
   - Validación de formato de archivo
   - Manejo de excepciones

## Cómo Usar

### 1. Acceso a la Funcionalidad

**Para Cuentas:**
Los botones de importación se encuentran en la sección de filtros de la página principal de cuentas:

- **Importar Cuentas Vendidas** (Botón amarillo)
- **Importar Cuentas Disponibles** (Botón azul)



### 2. Proceso de Importación

1. Haz clic en el botón correspondiente
2. Se abrirá un modal con instrucciones
3. Selecciona el archivo .txt a importar
4. Haz clic en "Importar Cuentas"
5. La aplicación procesará el archivo
6. Recibirás un mensaje de confirmación

### 3. Formato de Archivo Requerido

**Para Cuentas:**
El archivo debe ser un .txt exportado previamente desde la aplicación con el formato estándar:

```
CUENTA #1
----------------------------------------
ID: 101
Plataforma: Netflix
Email: ejemplo@gmail.com
Contraseña: password123
Precio: $15.00
Fecha de Compra: 01/01/2025
...
```



## Casos de Uso

### 🔄 Restauración de Datos
- Recuperar cuentas después de un fallo del sistema
- Restaurar desde backups
- Migrar datos entre instancias

### 👥 Colaboración
- Compartir inventario entre usuarios
- Importar cuentas desde otros sistemas
- Sincronización de datos

### 📊 Gestión de Inventario
- Restaurar cuentas vendidas al historial
- Agregar cuentas disponibles al inventario
- Mantener consistencia de datos

## Características Técnicas

### Rutas Implementadas

- `/importar_cuentas_vendidas` - POST para importar cuentas vendidas
- `/importar_cuentas_disponibles` - POST para importar cuentas disponibles


### Funciones de Procesamiento

- `procesar_cuenta_vendida_importada()` - Procesa cuentas vendidas
- `procesar_cuenta_disponible_importada()` - Procesa cuentas disponibles
- `procesar_usuario_importado()` - Procesa usuarios

### Validaciones

- Formato de archivo (.txt)
- Estructura del contenido
- Duplicados por email
- Formato de fechas
- Campos requeridos

## Archivos de Ejemplo

Se incluyen archivos de ejemplo para probar la funcionalidad:

- `ejemplo_cuentas_vendidas.txt` - Ejemplo de cuentas vendidas
- `ejemplo_cuentas_disponibles.txt` - Ejemplo de cuentas disponibles
- `ejemplo_usuarios.txt` - Ejemplo de usuarios

## Consideraciones Importantes

### ⚠️ Cuentas Vendidas
- Se importan con estado "Vendida"
- No estarán disponibles para venta
- Mantienen historial completo de venta

### ✅ Cuentas Disponibles
- Se importan con estado "Disponible"
- Estarán disponibles para venta
- Se agregan al inventario activo

### 🔒 Seguridad
- Solo usuarios autenticados pueden importar cuentas
- Solo administradores pueden importar usuarios
- Las cuentas se asocian al usuario que importa
- No se pueden importar cuentas de otros usuarios
- Los usuarios importados tienen contraseña por defecto "password123"

## Mensajes del Sistema

### Éxito
- "Importación completada: X cuentas importadas"

### Advertencia
- "X cuentas duplicadas" (si hay duplicados)

### Error
- "Error al procesar el archivo: [descripción]"
- "No se seleccionó ningún archivo"
- "El archivo debe ser de tipo .txt"

## Compatibilidad

- ✅ Archivos exportados desde la aplicación actual
- ✅ Formato estándar de exportación
- ✅ Codificación UTF-8
- ✅ Extensiones .txt

## Solución de Problemas

### Error: "No se seleccionó ningún archivo"
- Asegúrate de seleccionar un archivo antes de enviar

### Error: "El archivo debe ser de tipo .txt"
- Verifica que el archivo tenga extensión .txt

### Error: "Error al procesar el archivo"
- Verifica que el archivo tenga el formato correcto
- Asegúrate de que sea un archivo exportado desde la aplicación

### No se importan todas las cuentas
- Verifica que no haya cuentas duplicadas
- Revisa el formato del archivo
- Comprueba que los campos requeridos estén presentes

## Futuras Mejoras

- [ ] Soporte para archivos CSV
- [ ] Importación masiva con validación previa
- [ ] Plantillas de importación personalizables
- [ ] Logs detallados de importación
- [ ] Rollback selectivo de importaciones
- [ ] Importación desde otros formatos (Excel, JSON)
- [ ] Importación de usuarios con contraseñas personalizadas
- [ ] Validación de permisos más granular

## Soporte

Para reportar problemas o solicitar mejoras, contacta al equipo de desarrollo.

---

**Versión:** 1.0  
**Fecha:** Enero 2025  
**Autor:** Sistema de Gestión de Cuentas
