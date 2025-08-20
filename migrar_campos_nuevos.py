#!/usr/bin/env python3
"""
Script para migrar la base de datos y agregar los campos:
- precio
- fecha_compra  
- notas

Este script debe ejecutarse después de migrar_sistema_usuarios.py
"""

import os
import sys
from datetime import datetime, date
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Agregar el directorio actual al path para importar app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Cuenta, Usuario

def migrar_campos_nuevos():
    """Migrar la base de datos para agregar los nuevos campos"""
    print("🔄 Iniciando migración de campos nuevos...")
    
    with app.app_context():
        try:
            # Crear todas las tablas (esto agregará las nuevas columnas)
            db.create_all()
            print("✅ Tablas creadas/actualizadas correctamente")
            
            # Verificar si las nuevas columnas existen
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('cuenta')]
            
            print(f"📋 Columnas actuales en tabla 'cuenta': {columns}")
            
            # Verificar si necesitamos migrar datos existentes
            cuentas_sin_precio = Cuenta.query.filter_by(precio=None).all()
            cuentas_sin_fecha_compra = Cuenta.query.filter_by(fecha_compra=None).all()
            
            if cuentas_sin_precio or cuentas_sin_fecha_compra:
                print(f"🔄 Encontradas {len(cuentas_sin_precio)} cuentas sin precio y {len(cuentas_sin_fecha_compra)} sin fecha de compra")
                print("🔄 Migrando datos existentes...")
                
                # Migrar cuentas existentes
                for cuenta in Cuenta.query.all():
                    if cuenta.precio is None:
                        cuenta.precio = 0.0  # Precio por defecto
                        print(f"  💰 Cuenta {cuenta.id}: precio establecido a $0.00")
                    
                    if cuenta.fecha_compra is None:
                        # Usar fecha de creación como fecha de compra por defecto
                        if cuenta.fecha_creacion:
                            cuenta.fecha_compra = cuenta.fecha_creacion.date()
                        else:
                            cuenta.fecha_compra = date.today()
                        print(f"  📅 Cuenta {cuenta.id}: fecha_compra establecida a {cuenta.fecha_compra}")
                    
                    if cuenta.notas is None:
                        cuenta.notas = ""
                
                # Guardar cambios
                db.session.commit()
                print("✅ Datos migrados correctamente")
            else:
                print("✅ Todas las cuentas ya tienen los campos requeridos")
            
            # Verificar estado final
            total_cuentas = Cuenta.query.count()
            cuentas_con_precio = Cuenta.query.filter(Cuenta.precio.isnot(None)).count()
            cuentas_con_fecha_compra = Cuenta.query.filter(Cuenta.fecha_compra.isnot(None)).count()
            
            print(f"\n📊 Estado final de la migración:")
            print(f"  Total de cuentas: {total_cuentas}")
            print(f"  Cuentas con precio: {cuentas_con_precio}")
            print(f"  Cuentas con fecha_compra: {cuentas_con_fecha_compra}")
            
            if total_cuentas == cuentas_con_precio == cuentas_con_fecha_compra:
                print("🎉 ¡Migración completada exitosamente!")
            else:
                print("⚠️  Algunas cuentas pueden no tener todos los campos")
                
        except Exception as e:
            print(f"❌ Error durante la migración: {str(e)}")
            db.session.rollback()
            raise

def verificar_estado_migracion():
    """Verificar el estado actual de la migración"""
    print("🔍 Verificando estado de la migración...")
    
    with app.app_context():
        try:
            # Verificar estructura de la tabla
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('cuenta')]
            
            print(f"📋 Columnas en tabla 'cuenta': {columns}")
            
            # Verificar campos requeridos
            campos_requeridos = ['precio', 'fecha_compra', 'notas']
            campos_faltantes = [campo for campo in campos_requeridos if campo not in columns]
            
            if campos_faltantes:
                print(f"❌ Campos faltantes: {campos_faltantes}")
                print("🔄 Ejecuta la migración para agregar estos campos")
            else:
                print("✅ Todos los campos requeridos están presentes")
                
                # Verificar datos
                total_cuentas = Cuenta.query.count()
                cuentas_con_precio = Cuenta.query.filter(Cuenta.precio.isnot(None)).count()
                cuentas_con_fecha_compra = Cuenta.query.filter(Cuenta.fecha_compra.isnot(None)).count()
                
                print(f"📊 Estado de los datos:")
                print(f"  Total de cuentas: {total_cuentas}")
                print(f"  Cuentas con precio: {cuentas_con_precio}")
                print(f"  Cuentas con fecha_compra: {cuentas_con_fecha_compra}")
                
        except Exception as e:
            print(f"❌ Error al verificar estado: {str(e)}")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--verificar':
        verificar_estado_migracion()
    else:
        print("🚀 Migración de campos nuevos para Gestor de Cuentas")
        print("=" * 50)
        migrar_campos_nuevos()
        print("\n" + "=" * 50)
        print("✅ Migración completada")
        print("\nPara verificar el estado, ejecuta: python migrar_campos_nuevos.py --verificar")
