#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear un archivo ZIP del proyecto listo para InfinityFree
"""

import os
import zipfile
import shutil
from datetime import datetime

def crear_zip_infinityfree():
    """Crear archivo ZIP para InfinityFree"""
    
    print("🚀 Preparando proyecto para InfinityFree...")
    
    # Nombre del archivo ZIP
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"proyecto_infinityfree_{timestamp}.zip"
    
    # Archivos y carpetas que SÍ incluir
    archivos_incluir = [
        'app_infinityfree.py',
        'requirements_infinityfree.txt',
        '.htaccess',
        'config_infinityfree.py',
        'README_INFINITYFREE.md',
        'templates/',
        'static/'
    ]
    
    # Archivos y carpetas que NO incluir
    archivos_excluir = [
        'app.py',  # Archivo original
        'crear_zip_infinityfree.py',  # Este script
        'test_infinityfree.py',  # Script de pruebas
        'instance/',
        '.git/',
        '__pycache__/',
        '*.pyc',
        '*.db',
        '*.log',
        'venv/',
        'env/',
        'node_modules/',
        '.env',
        '.gitignore'
    ]
    
    try:
        # Crear archivo ZIP
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            
            print("📁 Agregando archivos al ZIP...")
            
            for item in archivos_incluir:
                if os.path.exists(item):
                    if os.path.isfile(item):
                        # Es un archivo
                        zipf.write(item, item)
                        print(f"✅ Agregado: {item}")
                    elif os.path.isdir(item):
                        # Es una carpeta
                        for root, dirs, files in os.walk(item):
                            # Excluir archivos y carpetas no deseados
                            dirs[:] = [d for d in dirs if d not in archivos_excluir]
                            
                            for file in files:
                                if not any(file.endswith(ext) for ext in ['.pyc', '.log', '.db']):
                                    file_path = os.path.join(root, file)
                                    arcname = file_path
                                    zipf.write(file_path, arcname)
                                    print(f"✅ Agregado: {arcname}")
                else:
                    print(f"⚠️  No encontrado: {item}")
            
            print(f"\n🎉 ZIP creado exitosamente: {zip_filename}")
            
            # Mostrar información del ZIP
            zip_size = os.path.getsize(zip_filename) / (1024 * 1024)  # MB
            print(f"📊 Tamaño del ZIP: {zip_size:.2f} MB")
            
            # Verificar que no exceda el límite de InfinityFree (10MB)
            if zip_size > 10:
                print("⚠️  ADVERTENCIA: El ZIP excede 10MB. InfinityFree puede rechazarlo.")
                print("💡 Considera eliminar archivos grandes o comprimir imágenes.")
            else:
                print("✅ El ZIP está dentro del límite de 10MB de InfinityFree")
            
            return zip_filename
            
    except Exception as e:
        print(f"❌ Error creando ZIP: {e}")
        return None

def verificar_archivos_requeridos():
    """Verificar que todos los archivos requeridos estén presentes"""
    
    print("\n🔍 Verificando archivos requeridos...")
    
    archivos_requeridos = [
        'app_infinityfree.py',
        'requirements_infinityfree.txt',
        '.htaccess',
        'templates/',
        'static/'
    ]
    
    archivos_faltantes = []
    
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo}")
            archivos_faltantes.append(archivo)
    
    if archivos_faltantes:
        print(f"\n⚠️  Archivos faltantes: {', '.join(archivos_faltantes)}")
        print("💡 Asegúrate de que todos los archivos estén presentes antes de crear el ZIP")
        return False
    
    print("\n✅ Todos los archivos requeridos están presentes")
    return True

def mostrar_instrucciones_despues_zip(zip_filename):
    """Mostrar instrucciones para después de crear el ZIP"""
    
    print(f"\n📋 INSTRUCCIONES PARA SUBIR A INFINITYFREE:")
    print("=" * 50)
    print(f"1. 📦 Archivo ZIP creado: {zip_filename}")
    print("2. 🌐 Ve a tu panel de control de InfinityFree")
    print("3. 📁 Haz clic en 'Gestor de archivos'")
    print("4. ⬆️  Sube el archivo ZIP")
    print("5. 📂 Extrae el ZIP en el servidor")
    print("6. 🗑️  Elimina el archivo ZIP para ahorrar espacio")
    print("7. 🐍 Instala las dependencias Python")
    print("8. 🚀 Prueba tu aplicación")
    print("\n💡 Credenciales por defecto:")
    print("   Usuario: admin")
    print("   Contraseña: admin123")

def main():
    """Función principal"""
    
    print("🚀 CREADOR DE ZIP PARA INFINITYFREE")
    print("=" * 40)
    
    # Verificar archivos requeridos
    if not verificar_archivos_requeridos():
        print("\n❌ No se puede crear el ZIP. Faltan archivos requeridos.")
        return
    
    # Crear el ZIP
    zip_filename = crear_zip_infinityfree()
    
    if zip_filename:
        # Mostrar instrucciones
        mostrar_instrucciones_despues_zip(zip_filename)
        
        print(f"\n🎯 Tu proyecto está listo para subir a InfinityFree!")
        print(f"📁 Archivo: {zip_filename}")
        
        # Abrir la carpeta donde se creó el ZIP
        try:
            import subprocess
            import platform
            
            if platform.system() == "Windows":
                os.startfile(os.getcwd())
            elif platform.system() == "Darwin":  # macOS
                subprocess.call(["open", os.getcwd()])
            else:  # Linux
                subprocess.call(["xdg-open", os.getcwd()])
                
            print("📂 Carpeta abierta automáticamente")
        except:
            print(f"📂 El ZIP se creó en: {os.getcwd()}")
    
    else:
        print("\n❌ No se pudo crear el ZIP. Revisa los errores anteriores.")

if __name__ == "__main__":
    main()
