# Gestor de Cuentas de Streaming

Sistema web para gestionar inventario de cuentas de streaming desde cualquier dispositivo.

## 🚀 Despliegue en Koyeb

### Prerrequisitos
- Cuenta en [Koyeb](https://koyeb.com)
- Repositorio en GitHub, GitLab o Bitbucket

### Pasos para Desplegar

1. **Preparar el Repositorio**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/tu-usuario/tu-repositorio.git
   git push -u origin main
   ```

2. **Crear Aplicación en Koyeb**
   - Ve a [Koyeb Dashboard](https://app.koyeb.com)
   - Haz clic en "Create App"
   - Conecta tu repositorio de Git
   - Selecciona el repositorio y branch

3. **Configurar Variables de Entorno**
   En la sección "Environment Variables" de Koyeb, agrega:
   ```
   FLASK_ENV=production
   SECRET_KEY=tu-clave-secreta-muy-segura-aqui
   DB_HOST=tu-host-mysql-koyeb
   DB_NAME=tu-nombre-base-datos
   DB_USER=tu-usuario-mysql
   DB_PASSWORD=tu-contraseña-mysql
   ```

4. **Configurar Base de Datos MySQL**
   - En Koyeb, ve a "Databases"
   - Crea una nueva base de datos MySQL
   - Copia las credenciales de conexión
   - Actualiza las variables de entorno con estas credenciales

5. **Desplegar**
   - Koyeb detectará automáticamente que es una aplicación Python
   - Usará el `Procfile` para iniciar la aplicación
   - La aplicación estará disponible en la URL proporcionada por Koyeb

### 🔧 Configuración Local

Para desarrollo local:

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar en modo desarrollo
python app.py
```

La aplicación usará SQLite automáticamente en modo desarrollo.

### 📁 Estructura del Proyecto

```
├── app.py              # Aplicación principal Flask
├── requirements.txt    # Dependencias Python
├── Procfile           # Configuración para Koyeb
├── runtime.txt        # Versión de Python
├── .gitignore         # Archivos a ignorar en Git
└── env.example        # Ejemplo de variables de entorno
```

### 🔐 Seguridad

- Cambia la contraseña del usuario administrador después del primer inicio
- Usa una SECRET_KEY segura en producción
- Configura HTTPS en Koyeb para mayor seguridad

### 📞 Soporte

Si tienes problemas con el despliegue, revisa:
- Los logs de la aplicación en Koyeb
- Las variables de entorno están configuradas correctamente
- La base de datos MySQL está accesible