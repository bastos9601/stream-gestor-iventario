#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de migración para PostgreSQL en Render
Este script crea las tablas necesarias en la base de datos PostgreSQL
"""

import os
from app import app, db, Usuario, Cuenta
from datetime import datetime

def migrar_postgresql():
    """Migrar la base de datos a PostgreSQL"""
    with app.app_context():
        try:
            print("🔄 Creando tablas en PostgreSQL...")
            
            # Crear todas las tablas
            db.create_all()
            print("✅ Tablas creadas exitosamente")
            
            # Verificar si ya existe un usuario administrador
            admin = Usuario.query.filter_by(username='admin').first()
            if not admin:
                print("👤 Creando usuario administrador...")
                admin = Usuario(
                    username='admin',
                    email='admin@gestor.com',
                    es_admin=True
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("✅ Usuario administrador creado:")
                print("   Usuario: admin")
                print("   Contraseña: admin123")
            else:
                print("ℹ️ Usuario administrador ya existe")
            
            # Verificar la conexión
            try:
                # Intentar hacer una consulta simple
                total_usuarios = Usuario.query.count()
                total_cuentas = Cuenta.query.count()
                print(f"✅ Conexión exitosa a PostgreSQL:")
                print(f"   Usuarios: {total_usuarios}")
                print(f"   Cuentas: {total_cuentas}")
            except Exception as e:
                print(f"❌ Error al verificar conexión: {str(e)}")
                return False
            
            print("🎉 Migración a PostgreSQL completada exitosamente!")
            return True
            
        except Exception as e:
            print(f"❌ Error durante la migración: {str(e)}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    print("🚀 Iniciando migración a PostgreSQL...")
    print("=" * 50)
    
    # Verificar variables de entorno
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("⚠️ ADVERTENCIA: DATABASE_URL no está configurada")
        print("   La aplicación usará SQLite por defecto")
    
    success = migrar_postgresql()
    
    if success:
        print("=" * 50)
        print("🎯 La aplicación está lista para usar PostgreSQL!")
        print("📝 Recuerda configurar las variables de entorno en Render:")
        print("   - SECRET_KEY")
        print("   - DATABASE_URL")
    else:
        print("=" * 50)
        print("❌ La migración falló. Revisa los errores arriba.")
