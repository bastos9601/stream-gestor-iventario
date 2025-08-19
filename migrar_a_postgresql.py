#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para migrar datos de SQLite a PostgreSQL
Ejecutar este script después de configurar PostgreSQL en Render
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import sqlite3

def migrar_datos():
    """Migrar datos de SQLite a PostgreSQL"""
    
    # Configuración de la base de datos SQLite (origen)
    sqlite_db = 'instance/cuentas_streaming.db'
    
    # Verificar que existe la base de datos SQLite
    if not os.path.exists(sqlite_db):
        print(f"❌ No se encontró la base de datos SQLite: {sqlite_db}")
        return False
    
    # Obtener URL de PostgreSQL desde variables de entorno
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ No se encontró la variable de entorno DATABASE_URL")
        print("Asegúrate de que tu aplicación esté configurada para usar PostgreSQL")
        return False
    
    # Convertir postgres:// a postgresql:// para SQLAlchemy
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    try:
        # Conectar a PostgreSQL
        print("🔌 Conectando a PostgreSQL...")
        pg_engine = create_engine(database_url)
        pg_session = sessionmaker(bind=pg_engine)()
        
        # Conectar a SQLite
        print("🔌 Conectando a SQLite...")
        sqlite_conn = sqlite3.connect(sqlite_db)
        sqlite_cursor = sqlite_conn.cursor()
        
        # Obtener lista de tablas
        sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = sqlite_cursor.fetchall()
        
        print(f"📋 Tablas encontradas: {[tabla[0] for tabla in tablas]}")
        
        for tabla in tablas:
            nombre_tabla = tabla[0]
            print(f"\n📊 Migrando tabla: {nombre_tabla}")
            
            # Obtener estructura de la tabla
            sqlite_cursor.execute(f"PRAGMA table_info({nombre_tabla});")
            columnas = sqlite_cursor.fetchall()
            
            # Obtener datos
            sqlite_cursor.execute(f"SELECT * FROM {nombre_tabla};")
            datos = sqlite_cursor.fetchall()
            
            if datos:
                print(f"   📥 {len(datos)} registros encontrados")
                
                # Crear tabla en PostgreSQL si no existe
                columnas_sql = []
                for col in columnas:
                    nombre = col[1]
                    tipo = col[2]
                    not_null = "NOT NULL" if col[3] else ""
                    pk = "PRIMARY KEY" if col[5] else ""
                    
                    # Mapear tipos de SQLite a PostgreSQL
                    if tipo == "INTEGER":
                        tipo_pg = "INTEGER"
                    elif tipo == "TEXT":
                        tipo_pg = "TEXT"
                    elif tipo == "REAL":
                        tipo_pg = "REAL"
                    elif tipo == "BLOB":
                        tipo_pg = "BYTEA"
                    else:
                        tipo_pg = "TEXT"
                    
                    col_sql = f"{nombre} {tipo_pg} {not_null} {pk}".strip()
                    columnas_sql.append(col_sql)
                
                create_table_sql = f"""
                CREATE TABLE IF NOT EXISTS {nombre_tabla} (
                    {', '.join(columnas_sql)}
                );
                """
                
                try:
                    pg_session.execute(text(create_table_sql))
                    pg_session.commit()
                    print(f"   ✅ Tabla {nombre_tabla} creada en PostgreSQL")
                except Exception as e:
                    print(f"   ⚠️  Error creando tabla {nombre_tabla}: {e}")
                    continue
                
                # Insertar datos
                if columnas:
                    placeholders = ', '.join(['%s'] * len(columnas))
                    insert_sql = f"INSERT INTO {nombre_tabla} VALUES ({placeholders});"
                    
                    try:
                        for dato in datos:
                            pg_session.execute(text(insert_sql), dato)
                        pg_session.commit()
                        print(f"   ✅ {len(datos)} registros migrados a {nombre_tabla}")
                    except Exception as e:
                        print(f"   ❌ Error migrando datos a {nombre_tabla}: {e}")
                        pg_session.rollback()
            else:
                print(f"   ℹ️  Tabla {nombre_tabla} está vacía")
        
        print("\n🎉 Migración completada!")
        return True
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        return False
    
    finally:
        # Cerrar conexiones
        if 'sqlite_conn' in locals():
            sqlite_conn.close()
        if 'pg_session' in locals():
            pg_session.close()

if __name__ == "__main__":
    print("🚀 Iniciando migración de SQLite a PostgreSQL...")
    print("=" * 50)
    
    if migrar_datos():
        print("\n✅ Migración exitosa!")
        print("Ahora puedes usar PostgreSQL como tu base de datos principal.")
    else:
        print("\n❌ La migración falló.")
        print("Revisa los errores y asegúrate de que PostgreSQL esté configurado correctamente.")
        sys.exit(1)
