# ========================================
# CONFIGURACIÓN DE EJEMPLO PARA INFINITYFREE
# ========================================
# COPIA ESTE ARCHIVO Y RENÓMBRALO A: config_infinityfree.py
# LUEGO CAMBIA LOS VALORES POR LOS REALES DE TU CUENTA

# Configuración de la base de datos MySQL en InfinityFree
DB_HOST = 'sql.infinityfree.com'
DB_NAME = 'gestor_cuentas'        # ← CAMBIA: Nombre de tu base de datos
DB_USER = 'usuario_cuentas'       # ← CAMBIA: Tu usuario de base de datos
DB_PASSWORD = 'mi_contraseña123'  # ← CAMBIA: Tu contraseña de base de datos

# Configuración de la aplicación
SECRET_KEY = 'cambia-esta-clave-por-una-segura-y-única-123456789'

# Configuración de MySQL optimizada para InfinityFree
MYSQL_CONFIG = {
    'pool_size': 5,
    'pool_timeout': 10,
    'pool_recycle': 3600,
    'max_overflow': 2,
    'connect_timeout': 10,
    'charset': 'utf8mb4'
}

# URL de la base de datos (NO CAMBIAR)
DATABASE_URL = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

# ========================================
# INSTRUCCIONES:
# ========================================
# 1. Copia este archivo
# 2. Renómbralo a: config_infinityfree.py
# 3. Cambia los valores marcados con ←
# 4. Sube el archivo a tu hosting en InfinityFree
# 5. ¡Listo!

# ========================================
# EJEMPLO DE VALORES REALES:
# ========================================
# DB_NAME = 'epiz_123456_gestor'
# DB_USER = 'epiz_123456_admin'
# DB_PASSWORD = 'MiContraseñaSegura2024!'
# SECRET_KEY = 'clave-super-secreta-para-mi-app-2024'
