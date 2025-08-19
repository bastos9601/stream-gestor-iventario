#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración para InfinityFree
"""

import os

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
