#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración del Gestor de Cuentas de Streaming
Configuraciones para diferentes entornos
"""

import os
from datetime import timedelta
import re

def get_database_url():
    """Obtener y formatear la URL de la base de datos"""
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # Render usa postgres:// pero SQLAlchemy necesita postgresql://
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        return database_url
    
    return 'sqlite:///cuentas_streaming.db'

class Config:
    """Configuración base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu_clave_secreta_aqui_2024'
    SQLALCHEMY_DATABASE_URI = get_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de sesión
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Configuración de archivos
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Configuración de seguridad
    SESSION_COOKIE_SECURE = False  # Cambiar a True en producción con HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configuración de la aplicación
    APP_NAME = 'Gestor de Cuentas de Streaming'
    APP_VERSION = '1.0.0'
    APP_DESCRIPTION = 'Sistema web para gestionar inventario de cuentas de streaming'

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_ECHO = False
    
    # Configuraciones de seguridad para producción
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'

class TestingConfig(Config):
    """Configuración para pruebas"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Obtener configuración basada en variable de entorno"""
    config_name = os.environ.get('FLASK_ENV', 'default')
    return config[config_name]
