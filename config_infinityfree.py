#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración para InfinityFree
"""

import os

# Configuración para InfinityFree
# Este archivo contiene la configuración de la base de datos MySQL

# Configuración de la base de datos MySQL en InfinityFree
DB_HOST = 'sql.infinityfree.com'
DB_NAME = 'if0_39819776_hplay_gestor_db'  # Cambiar por el nombre real de tu base de datos
DB_USER = 'if0_39819776'      # Cambiar por tu usuario de base de datos
DB_PASSWORD = 'tKG8hdlcWWT8X'  # Cambiar por tu contraseña de base de datos

# Configuración de la aplicación
SECRET_KEY = 'alfredo0152025'

# Configuración de MySQL optimizada para InfinityFree
MYSQL_CONFIG = {
    'pool_size': 5,
    'pool_timeout': 10,
    'pool_recycle': 3600,
    'max_overflow': 2,
    'connect_timeout': 10,
    'charset': 'utf8mb4'
}

# URL de la base de datos
DATABASE_URL = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

class Config:
    """Configuración base"""
    SECRET_KEY = 'tu_clave_secreta_aqui_2024_infinityfree'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración para InfinityFree
    DEBUG = False
    TESTING = False
    
    # Base de datos en memoria (se reinicia cada vez que se reinicia la aplicación)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Configuración de sesión
    SESSION_COOKIE_SECURE = False  # InfinityFree no siempre tiene HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configuración de archivos
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB máximo (límite de InfinityFree)
    
    # Configuración de logging
    LOG_LEVEL = 'INFO'

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///cuentas_streaming.db'

class ProductionConfig(Config):
    """Configuración para producción (InfinityFree)"""
    DEBUG = False
    
    # Intentar usar variables de entorno si están disponibles
    SECRET_KEY = os.environ.get('SECRET_KEY', Config.SECRET_KEY)

# Configuración por defecto
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}
