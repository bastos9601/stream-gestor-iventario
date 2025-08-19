#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar la aplicación antes del despliegue en InfinityFree
"""

import sys
import os

def test_imports():
    """Probar que todas las importaciones funcionen"""
    print("🔍 Probando importaciones...")
    
    try:
        from flask import Flask
        print("✅ Flask importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando Flask: {e}")
        return False
    
    try:
        from flask_sqlalchemy import SQLAlchemy
        print("✅ Flask-SQLAlchemy importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando Flask-SQLAlchemy: {e}")
        return False
    
    try:
        from flask_login import LoginManager
        print("✅ Flask-Login importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando Flask-Login: {e}")
        return False
    
    try:
        from werkzeug.security import generate_password_hash
        print("✅ Werkzeug importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando Werkzeug: {e}")
        return False
    
    return True

def test_app_creation():
    """Probar la creación de la aplicación"""
    print("\n🔍 Probando creación de aplicación...")
    
    try:
        # Importar la aplicación
        from app_infinityfree import app, db
        
        print("✅ Aplicación Flask creada correctamente")
        print("✅ Base de datos SQLAlchemy configurada")
        
        # Verificar configuración
        if app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:':
            print("✅ Base de datos en memoria configurada correctamente")
        else:
            print("⚠️  Base de datos no está en memoria")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando aplicación: {e}")
        return False

def test_database_operations():
    """Probar operaciones básicas de base de datos"""
    print("\n🔍 Probando operaciones de base de datos...")
    
    try:
        from app_infinityfree import app, db, Usuario, Cuenta
        
        with app.app_context():
            # Crear tablas
            db.create_all()
            print("✅ Tablas creadas correctamente")
            
            # Crear usuario de prueba
            usuario = Usuario(
                username='test_user',
                email='test@example.com',
                es_admin=False
            )
            usuario.set_password('test123')
            
            db.session.add(usuario)
            db.session.commit()
            print("✅ Usuario de prueba creado correctamente")
            
            # Verificar usuario
            usuario_verificado = Usuario.query.filter_by(username='test_user').first()
            if usuario_verificado and usuario_verificado.check_password('test123'):
                print("✅ Verificación de contraseña funcionando")
            else:
                print("❌ Error en verificación de contraseña")
                return False
            
            # Crear cuenta de prueba
            cuenta = Cuenta(
                plataforma='Netflix',
                email='netflix@example.com',
                password='password123',
                precio=15.99,
                fecha_compra=datetime.now().date()
            )
            
            db.session.add(cuenta)
            db.session.commit()
            print("✅ Cuenta de prueba creada correctamente")
            
            # Limpiar datos de prueba
            db.session.delete(usuario)
            db.session.delete(cuenta)
            db.session.commit()
            print("✅ Datos de prueba eliminados correctamente")
            
        return True
        
    except Exception as e:
        print(f"❌ Error en operaciones de base de datos: {e}")
        return False

def test_routes():
    """Probar que las rutas estén configuradas"""
    print("\n🔍 Probando configuración de rutas...")
    
    try:
        from app_infinityfree import app
        
        # Verificar rutas principales
        routes = [
            '/', '/login', '/logout', '/perfil', '/cuentas',
            '/cuenta/nueva', '/usuarios', '/usuario/nuevo'
        ]
        
        for route in routes:
            if route in [rule.rule for rule in app.url_map.iter_rules()]:
                print(f"✅ Ruta {route} configurada")
            else:
                print(f"❌ Ruta {route} no encontrada")
                return False
        
        print("✅ Todas las rutas principales están configuradas")
        return True
        
    except Exception as e:
        print(f"❌ Error verificando rutas: {e}")
        return False

def test_templates():
    """Verificar que las plantillas existan"""
    print("\n🔍 Verificando plantillas...")
    
    required_templates = [
        'base.html', 'login.html', 'cuentas.html', 'nueva_cuenta.html',
        'editar_cuenta.html', 'ver_cuenta.html', 'usuarios.html',
        'nuevo_usuario.html', 'perfil.html', '404.html', '500.html'
    ]
    
    missing_templates = []
    
    for template in required_templates:
        if os.path.exists(f'templates/{template}'):
            print(f"✅ Plantilla {template} encontrada")
        else:
            print(f"❌ Plantilla {template} no encontrada")
            missing_templates.append(template)
    
    if missing_templates:
        print(f"\n⚠️  Plantillas faltantes: {', '.join(missing_templates)}")
        return False
    
    print("✅ Todas las plantillas están presentes")
    return True

def test_static_files():
    """Verificar archivos estáticos"""
    print("\n🔍 Verificando archivos estáticos...")
    
    static_dirs = ['static', 'static/icons']
    
    for static_dir in static_dirs:
        if os.path.exists(static_dir):
            print(f"✅ Directorio {static_dir} encontrado")
        else:
            print(f"❌ Directorio {static_dir} no encontrado")
            return False
    
    # Verificar archivos importantes
    important_files = [
        'static/manifest.json',
        'static/sw.js',
        '.htaccess',
        'requirements_infinityfree.txt'
    ]
    
    for file_path in important_files:
        if os.path.exists(file_path):
            print(f"✅ Archivo {file_path} encontrado")
        else:
            print(f"❌ Archivo {file_path} no encontrado")
            return False
    
    print("✅ Todos los archivos estáticos están presentes")
    return True

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas para InfinityFree...\n")
    
    tests = [
        test_imports,
        test_app_creation,
        test_database_operations,
        test_routes,
        test_templates,
        test_static_files
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"❌ Prueba {test.__name__} falló")
        except Exception as e:
            print(f"❌ Error en prueba {test.__name__}: {e}")
    
    print(f"\n📊 Resultados de las pruebas:")
    print(f"✅ Aprobadas: {passed}/{total}")
    print(f"❌ Fallidas: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 ¡Todas las pruebas pasaron! Tu aplicación está lista para InfinityFree.")
        print("📋 Sigue las instrucciones en README_INFINITYFREE.md para el despliegue.")
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisa los errores antes del despliegue.")
        return 1
    
    return 0

if __name__ == '__main__':
    # Agregar el directorio actual al path para importaciones
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Importar datetime para las pruebas
    from datetime import datetime
    
    exit(main())
