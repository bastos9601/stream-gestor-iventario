#!/usr/bin/env python3
"""
Script simple para crear la base de datos desde cero con la nueva estructura
"""

import os
import sys
from datetime import datetime

# Agregar el directorio actual al path para importar app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Usuario, Cuenta

def crear_base_datos():
    """Crear la base de datos desde cero"""
    print("🚀 Creando base de datos desde cero...")
    
    with app.app_context():
        try:
            # Eliminar todas las tablas existentes
            db.drop_all()
            print("🗑️  Tablas existentes eliminadas")
            
            # Crear todas las tablas con la nueva estructura
            db.create_all()
            print("✅ Nuevas tablas creadas correctamente")
            
            # Crear usuario administrador por defecto
            admin = Usuario(
                username='admin',
                email='admin@example.com',
                es_admin=True,
                activo=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("👑 Usuario administrador creado: admin/admin123")
            
            # Verificar estructura
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('cuenta')]
            
            print(f"\n📋 Estructura de la tabla 'cuenta':")
            for col in columns:
                print(f"   - {col}")
            
            print(f"\n🎉 ¡Base de datos creada exitosamente!")
            print("   Usuario: admin")
            print("   Contraseña: admin123")
            print("   ⚠️  IMPORTANTE: Cambia la contraseña después del primer inicio de sesión")
            
        except Exception as e:
            print(f"❌ Error al crear la base de datos: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 CREADOR DE BASE DE DATOS")
    print("=" * 50)
    crear_base_datos()
    print("\n" + "=" * 50)
    print("✅ Base de datos lista")
    print("   Ejecuta: python app.py")
