#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de migración para PostgreSQL en Render
Actualiza la base de datos con los nuevos campos agregados al modelo Cuenta
"""

import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def conectar_postgresql():
    """Conectar a la base de datos PostgreSQL en Render"""
    try:
        # Obtener la URL de la base de datos desde las variables de entorno
        database_url = os.getenv('DATABASE_URL')
        
        if not database_url:
            print("❌ Error: No se encontró la variable DATABASE_URL")
            return None
        
        # Conectar a la base de datos
        conn = psycopg2.connect(database_url)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        print("✅ Conexión exitosa a PostgreSQL en Render")
        return conn
        
    except Exception as e:
        print(f"❌ Error al conectar a PostgreSQL: {e}")
        return None

def verificar_campos_existentes(cursor, table_name):
    """Verificar qué campos ya existen en la tabla"""
    try:
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = %s
            ORDER BY ordinal_position
        """, (table_name,))
        
        campos_existentes = {row[0]: row[1] for row in cursor.fetchall()}
        return campos_existentes
        
    except Exception as e:
        print(f"❌ Error al verificar campos existentes: {e}")
        return {}

def agregar_campo_si_no_existe(cursor, table_name, column_name, column_definition):
    """Agregar un campo si no existe"""
    try:
        # Verificar si el campo ya existe
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = %s AND column_name = %s
        """, (table_name, column_name))
        
        if cursor.fetchone():
            print(f"✅ Campo '{column_name}' ya existe en la tabla '{table_name}'")
            return True
        else:
            # Agregar el campo
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}")
            print(f"✅ Campo '{column_name}' agregado exitosamente a la tabla '{table_name}'")
            return True
            
    except Exception as e:
        print(f"❌ Error al agregar campo '{column_name}': {e}")
        return False

def migrar_base_datos():
    """Ejecutar la migración completa de la base de datos"""
    print("🚀 Iniciando migración de la base de datos PostgreSQL en Render...")
    
    # Conectar a la base de datos
    conn = conectar_postgresql()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Verificar campos existentes
        print("\n📋 Verificando estructura actual de la tabla 'cuenta'...")
        campos_existentes = verificar_campos_existentes(cursor, 'cuenta')
        
        if campos_existentes:
            print("Campos existentes:")
            for campo, tipo in campos_existentes.items():
                print(f"  - {campo}: {tipo}")
        else:
            print("⚠️  La tabla 'cuenta' no existe o está vacía")
        
        print("\n🔧 Agregando nuevos campos...")
        
        # Lista de campos a agregar con sus definiciones
        campos_nuevos = [
            ("precio", "DECIMAL(10,2) NOT NULL DEFAULT 0.00"),
            ("fecha_compra", "DATE NOT NULL DEFAULT CURRENT_DATE"),
            ("notas", "TEXT"),
            ("fecha_venta", "TIMESTAMP"),
            ("nombre_comprador", "VARCHAR(100)"),
            ("whatsapp_comprador", "VARCHAR(20)"),
            ("fecha_vencimiento", "DATE"),
            ("usuario_id", "INTEGER NOT NULL DEFAULT 1")
        ]
        
        # Agregar cada campo
        for campo, definicion in campos_nuevos:
            if agregar_campo_si_no_existe(cursor, 'cuenta', campo, definicion):
                print(f"  ✅ {campo}: {definicion}")
            else:
                print(f"  ❌ Error al agregar {campo}")
        
        # Verificar si la tabla usuario existe, si no, crearla
        print("\n👥 Verificando tabla 'usuario'...")
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'usuario'
            )
        """)
        
        if not cursor.fetchone()[0]:
            print("📝 Creando tabla 'usuario'...")
            cursor.execute("""
                CREATE TABLE usuario (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(80) UNIQUE NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    password_hash VARCHAR(200) NOT NULL,
                    es_admin BOOLEAN DEFAULT FALSE,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    activo BOOLEAN DEFAULT TRUE
                )
            """)
            print("✅ Tabla 'usuario' creada exitosamente")
            
            # Crear usuario administrador por defecto
            print("👑 Creando usuario administrador por defecto...")
            cursor.execute("""
                INSERT INTO usuario (username, email, password_hash, es_admin) 
                VALUES ('admin', 'admin@gestor.com', 'pbkdf2:sha256:600000$admin123', TRUE)
                ON CONFLICT (username) DO NOTHING
            """)
            print("✅ Usuario administrador creado/verificado")
        
        # Crear índices para mejorar el rendimiento
        print("\n📊 Creando índices...")
        indices = [
            ("idx_cuenta_usuario_id", "cuenta", "usuario_id"),
            ("idx_cuenta_estado", "cuenta", "estado"),
            ("idx_cuenta_plataforma", "cuenta", "plataforma"),
            ("idx_usuario_username", "usuario", "username")
        ]
        
        for nombre_indice, tabla, columna in indices:
            try:
                cursor.execute(f"CREATE INDEX IF NOT EXISTS {nombre_indice} ON {tabla} ({columna})")
                print(f"  ✅ Índice '{nombre_indice}' creado/verificado")
            except Exception as e:
                print(f"  ⚠️  Índice '{nombre_indice}': {e}")
        
        # Confirmar cambios
        conn.commit()
        print("\n🎉 ¡Migración completada exitosamente!")
        
        # Mostrar resumen final
        print("\n📋 Resumen de la migración:")
        campos_finales = verificar_campos_existentes(cursor, 'cuenta')
        print(f"Total de campos en tabla 'cuenta': {len(campos_finales)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        conn.rollback()
        return False
        
    finally:
        if conn:
            conn.close()
            print("🔌 Conexión cerrada")

if __name__ == "__main__":
    print("=" * 60)
    print("🔄 MIGRADOR DE BASE DE DATOS POSTGRESQL - RENDER")
    print("=" * 60)
    
    # Verificar variables de entorno
    if not os.getenv('DATABASE_URL'):
        print("⚠️  ADVERTENCIA: No se encontró DATABASE_URL")
        print("   Asegúrate de tener configurada la variable de entorno")
        print("   o ejecutar este script desde Render")
    
    # Ejecutar migración
    if migrar_base_datos():
        print("\n✅ La base de datos ha sido actualizada correctamente")
        print("🚀 Tu aplicación está lista para usar en Render")
    else:
        print("\n❌ La migración falló. Revisa los errores anteriores")
    
    print("=" * 60)
