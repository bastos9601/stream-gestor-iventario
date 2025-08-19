# Migración a PostgreSQL en Render

Este documento te guía para migrar tu aplicación de SQLite a PostgreSQL en Render, solucionando el problema de pérdida de datos por reinicios.

## 🚨 Problema Actual

- **SQLite**: Se almacena localmente en el servidor de Render
- **Problema**: Cuando Render detecta inactividad, reinicia el servidor y pierdes todos los datos
- **Solución**: Usar PostgreSQL como base de datos persistente

## ✅ Beneficios de PostgreSQL en Render

- **Persistencia**: Los datos se mantienen aunque se reinicie la aplicación
- **Escalabilidad**: Mejor rendimiento con múltiples usuarios
- **Confiabilidad**: Base de datos robusta y estable
- **Backups automáticos**: Render hace backups automáticos de PostgreSQL

## 🚀 Pasos para la Migración

### 1. Crear Base de Datos PostgreSQL en Render

1. Ve a tu [dashboard de Render](https://dashboard.render.com)
2. Haz clic en **"New +"** → **"PostgreSQL"**
3. Configura:
   - **Name**: `gestor-cuentas-db`
   - **Database**: `cuentas_streaming`
   - **User**: `cuentas_user`
   - **Plan**: `Free` (o el plan que prefieras)
   - **Region**: La misma que tu aplicación web

### 2. Obtener Variables de Entorno

Después de crear la base de datos, Render te proporcionará:
- **Internal Database URL**: Para conexiones desde tu aplicación
- **External Database URL**: Para conexiones externas (no la uses en producción)

### 3. Actualizar Variables de Entorno en tu Aplicación Web

1. Ve a tu aplicación web en Render
2. En **Environment**, agrega:
   - `DATABASE_URL`: La Internal Database URL de PostgreSQL
   - `FLASK_ENV`: `production`

### 4. Desplegar la Aplicación Actualizada

1. Haz commit y push de los cambios a tu repositorio
2. Render detectará los cambios y hará deploy automáticamente
3. Verifica que la aplicación se conecte a PostgreSQL

### 5. Migrar Datos Existentes

Si tienes datos en SQLite que quieres preservar:

```bash
# En tu servidor local o en Render
python migrar_a_postgresql.py
```

## 🔧 Configuración Técnica

### Archivos Modificados

- `render.yaml`: Configuración de servicios
- `config.py`: Manejo de URLs de base de datos
- `requirements.txt`: Driver de PostgreSQL
- `migrar_a_postgresql.py`: Script de migración

### Variables de Entorno Requeridas

```bash
DATABASE_URL=postgresql://usuario:password@host:puerto/database
FLASK_ENV=production
SECRET_KEY=tu_clave_secreta
```

## 📊 Verificación de la Migración

### 1. Verificar Conexión

Después del deploy, verifica en los logs de Render que:
- La aplicación se conecte exitosamente a PostgreSQL
- No haya errores de conexión a la base de datos

### 2. Verificar Funcionalidad

- Crea una nueva cuenta de streaming
- Verifica que se guarde en PostgreSQL
- Reinicia la aplicación manualmente
- Verifica que los datos persistan

### 3. Verificar Rendimiento

- La aplicación debería funcionar igual o mejor
- Las consultas pueden ser más rápidas
- Mejor manejo de múltiples usuarios simultáneos

## 🛠️ Solución de Problemas

### Error: "psycopg2 not found"

```bash
# Asegúrate de que psycopg2-binary esté en requirements.txt
pip install psycopg2-binary
```

### Error: "Connection refused"

- Verifica que la `DATABASE_URL` sea correcta
- Asegúrate de usar la Internal Database URL
- Verifica que la base de datos esté activa en Render

### Error: "Table does not exist"

- Ejecuta el script de migración
- Verifica que las tablas se creen correctamente
- Revisa los logs de migración

## 🔒 Seguridad

- **Nunca** expongas la External Database URL
- Usa solo la Internal Database URL en producción
- Mantén las credenciales seguras
- Considera usar variables de entorno secretas

## 📈 Monitoreo

### Logs de Render

- Revisa los logs de la aplicación regularmente
- Monitorea errores de conexión a la base de datos
- Verifica el rendimiento de las consultas

### Métricas de PostgreSQL

- Conexiones activas
- Tiempo de respuesta de consultas
- Uso de memoria y CPU

## 🎯 Próximos Pasos

1. **Backup**: Configura backups automáticos
2. **Optimización**: Ajusta índices y consultas
3. **Escalabilidad**: Considera planes de pago para más recursos
4. **Monitoreo**: Implementa alertas de salud de la base de datos

## 📞 Soporte

Si encuentras problemas:

1. Revisa los logs de Render
2. Verifica la configuración de variables de entorno
3. Consulta la [documentación de Render](https://render.com/docs)
4. Revisa los logs de PostgreSQL en el dashboard

---

**¡Con PostgreSQL, tus datos estarán seguros y tu aplicación será más robusta!** 🎉
