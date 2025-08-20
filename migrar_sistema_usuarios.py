#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de migración para el sistema de usuarios
Este script convierte la base de datos existente al nuevo sistema de usuarios
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Agregar el directorio actual al path para importar app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Usuario, Cuenta

load_dotenv()

def migrar_sistema_usuarios():
    """Migrar la base de datos al nuevo sistema de usuarios"""
    
    with app.app_context():
        print("🚀 Iniciando migración al sistema de usuarios...")
        
        try:
            # Crear las nuevas tablas si no existen
            db.create_all()
            print("✅ Tablas creadas/actualizadas correctamente")
            
            # Verificar si ya existe un usuario administrador
            admin_existente = Usuario.query.filter_by(es_admin=True).first()
            
            if not admin_existente:
                # Crear usuario administrador por defecto
                admin = Usuario(
                    username='admin',
                    email='admin@gestor.com',
                    es_admin=True,
                    activo=True,
                    fecha_creacion=datetime.utcnow()
                )
                admin.set_password('admin123')
                db.session.add(admin)
                print("✅ Usuario administrador creado")
            else:
                print("ℹ️  Usuario administrador ya existe")
            
            # Verificar si hay cuentas existentes sin usuario_id
            cuentas_sin_usuario = Cuenta.query.filter_by(usuario_id=None).all()
            
            if cuentas_sin_usuario:
                print(f"📊 Encontradas {len(cuentas_sin_usuario)} cuentas sin usuario asignado")
                
                # Asignar todas las cuentas existentes al administrador
                admin = Usuario.query.filter_by(es_admin=True).first()
                
                for cuenta in cuentas_sin_usuario:
                    cuenta.usuario_id = admin.id
                
                print("✅ Todas las cuentas existentes asignadas al administrador")
            else:
                print("ℹ️  No hay cuentas sin usuario asignado")
            
            # Verificar si hay campos que necesiten migración
            cuentas_con_campos_antiguos = Cuenta.query.filter(
                Cuenta.estado.in_(['disponible', 'vendida'])
            ).all()
            
            if cuentas_con_campos_antiguos:
                print(f"🔄 Migrando {len(cuentas_con_campos_antiguos)} cuentas con campos antiguos...")
                
                for cuenta in cuentas_con_campos_antiguos:
                    # Migrar estado
                    if cuenta.estado == 'disponible':
                        cuenta.estado = 'Disponible'
                    elif cuenta.estado == 'vendida':
                        cuenta.estado = 'Vendida'
                    
                    # Migrar fecha_creacion si no existe
                    if not hasattr(cuenta, 'fecha_creacion') or cuenta.fecha_creacion is None:
                        if hasattr(cuenta, 'created_at') and cuenta.created_at:
                            cuenta.fecha_creacion = cuenta.created_at
                        else:
                            cuenta.fecha_creacion = datetime.utcnow()
                    
                    # Migrar fecha_venta si no existe
                    if not hasattr(cuenta, 'fecha_venta') or cuenta.fecha_venta is None:
                        if hasattr(cuenta, 'fecha_venta_old') and cuenta.fecha_venta_old:
                            cuenta.fecha_venta = datetime.combine(cuenta.fecha_venta_old, datetime.min.time())
                        elif cuenta.estado == 'Vendida':
                            cuenta.fecha_venta = datetime.utcnow()
                
                print("✅ Campos de cuentas migrados correctamente")
            
            # Commit de todos los cambios
            db.session.commit()
            print("✅ Cambios guardados en la base de datos")
            
            # Mostrar resumen final
            total_usuarios = Usuario.query.count()
            total_cuentas = Cuenta.query.count()
            cuentas_disponibles = Cuenta.query.filter_by(estado='Disponible').count()
            cuentas_vendidas = Cuenta.query.filter_by(estado='Vendida').count()
            
            print("\n📊 RESUMEN DE LA MIGRACIÓN:")
            print(f"   👥 Usuarios: {total_usuarios}")
            print(f"   📺 Cuentas totales: {total_cuentas}")
            print(f"   ✅ Cuentas disponibles: {cuentas_disponibles}")
            print(f"   💰 Cuentas vendidas: {cuentas_vendidas}")
            
            if admin_existente or Usuario.query.filter_by(es_admin=True).first():
                admin = Usuario.query.filter_by(es_admin=True).first()
                print(f"\n👑 Usuario administrador: {admin.username}")
                print(f"   📧 Email: {admin.email}")
                print(f"   🔑 Contraseña: admin123")
                print("   ⚠️  IMPORTANTE: Cambia la contraseña después del primer inicio de sesión")
            
            print("\n🎉 ¡Migración completada exitosamente!")
            print("   La aplicación está lista para usar el nuevo sistema de usuarios")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error durante la migración: {str(e)}")
            print("   Revisa los logs y verifica la configuración de la base de datos")
            return False
        
        return True

def verificar_estado_migracion():
    """Verificar el estado actual de la migración"""
    
    with app.app_context():
        print("🔍 Verificando estado de la migración...")
        
        try:
            # Verificar tablas
            inspector = db.inspect(db.engine)
            tablas_existentes = inspector.get_table_names()
            
            print(f"📋 Tablas existentes: {', '.join(tablas_existentes)}")
            
            # Verificar usuarios
            total_usuarios = Usuario.query.count()
            admin = Usuario.query.filter_by(es_admin=True).first()
            
            print(f"👥 Total de usuarios: {total_usuarios}")
            if admin:
                print(f"👑 Administrador: {admin.username} ({admin.email})")
            else:
                print("❌ No hay usuario administrador")
            
            # Verificar cuentas
            total_cuentas = Cuenta.query.count()
            cuentas_sin_usuario = Cuenta.query.filter_by(usuario_id=None).count()
            
            print(f"📺 Total de cuentas: {total_cuentas}")
            print(f"⚠️  Cuentas sin usuario: {cuentas_sin_usuario}")
            
            if cuentas_sin_usuario > 0:
                print("   ⚠️  Se requiere ejecutar la migración")
            else:
                print("   ✅ La migración ya está completa")
            
        except Exception as e:
            print(f"❌ Error al verificar estado: {str(e)}")

if __name__ == '__main__':
    print("=" * 60)
    print("🔄 MIGRADOR DEL SISTEMA DE USUARIOS")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--verificar':
        verificar_estado_migracion()
    else:
        print("Ejecutando migración completa...")
        if migrar_sistema_usuarios():
            print("\n✅ Migración exitosa. Puedes ejecutar la aplicación ahora.")
        else:
            print("\n❌ La migración falló. Revisa los errores arriba.")
            sys.exit(1)
    
    print("\n" + "=" * 60)
