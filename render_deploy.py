#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de despliegue para Render.com
Configura y despliega la aplicación con la base de datos PostgreSQL
"""

import os
import subprocess
import sys
from pathlib import Path

def verificar_archivos_requeridos():
    """Verificar que todos los archivos necesarios estén presentes"""
    archivos_requeridos = [
        'app.py',
        'requirements.txt',
        'Procfile',
        'render.yaml',
        'runtime.txt'
    ]
    
    print("🔍 Verificando archivos requeridos...")
    for archivo in archivos_requeridos:
        if Path(archivo).exists():
            print(f"  ✅ {archivo}")
        else:
            print(f"  ❌ {archivo} - NO ENCONTRADO")
            return False
    
    return True

def verificar_git():
    """Verificar que Git esté configurado correctamente"""
    try:
        # Verificar si es un repositorio Git
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Repositorio Git configurado")
            
            # Verificar el remote de Render
            result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
            if 'render' in result.stdout.lower():
                print("✅ Remote de Render configurado")
                return True
            else:
                print("⚠️  No se encontró remote de Render")
                return False
        else:
            print("❌ No es un repositorio Git")
            return False
            
    except FileNotFoundError:
        print("❌ Git no está instalado")
        return False

def configurar_git_remote():
    """Configurar el remote de Git para Render"""
    print("\n🔧 Configurando remote de Git para Render...")
    
    # Solicitar la URL del repositorio de Render
    print("📝 Para configurar el remote de Render, necesito la URL del repositorio.")
    print("   Puedes encontrarla en tu dashboard de Render.com")
    print("   Ejemplo: https://git.render.com/username/repo-name.git")
    
    url_render = input("🔗 URL del repositorio de Render: ").strip()
    
    if not url_render:
        print("❌ URL no proporcionada")
        return False
    
    try:
        # Agregar remote de Render
        subprocess.run(['git', 'remote', 'add', 'render', url_render], check=True)
        print("✅ Remote de Render agregado exitosamente")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al agregar remote: {e}")
        return False

def hacer_commit_y_push():
    """Hacer commit de los cambios y push a Render"""
    print("\n📤 Haciendo commit y push a Render...")
    
    try:
        # Agregar todos los archivos
        subprocess.run(['git', 'add', '.'], check=True)
        print("✅ Archivos agregados al staging")
        
        # Hacer commit
        commit_message = "🚀 Actualización: Nuevas funcionalidades y tarjeta de valor del inventario"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        print("✅ Commit realizado")
        
        # Push a Render
        subprocess.run(['git', 'push', 'render', 'main'], check=True)
        print("✅ Push a Render completado")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en Git: {e}")
        return False

def mostrar_instrucciones_manuales():
    """Mostrar instrucciones para despliegue manual"""
    print("\n" + "="*60)
    print("📋 INSTRUCCIONES PARA DESPLIEGUE MANUAL EN RENDER")
    print("="*60)
    
    print("\n1️⃣ **Preparar el repositorio Git:**")
    print("   git add .")
    print("   git commit -m '🚀 Actualización: Nuevas funcionalidades'")
    print("   git push origin main")
    
    print("\n2️⃣ **En Render.com:**")
    print("   - Ve a tu dashboard de Render")
    print("   - Selecciona tu servicio web 'gestor-cuentas-stream'")
    print("   - Haz clic en 'Manual Deploy'")
    print("   - Selecciona la rama 'main'")
    print("   - Haz clic en 'Deploy Latest Commit'")
    
    print("\n3️⃣ **Verificar la base de datos:**")
    print("   - En Render, ve a tu base de datos 'gestor-cuentas-db'")
    print("   - Verifica que esté en estado 'Available'")
    print("   - La aplicación se conectará automáticamente")
    
    print("\n4️⃣ **Probar la aplicación:**")
    print("   - Espera a que el despliegue termine")
    print("   - Visita la URL de tu aplicación")
    print("   - Verifica que las 5 tarjetas del dashboard aparezcan")
    
    print("\n" + "="*60)

def main():
    """Función principal del script de despliegue"""
    print("🚀 DESPLIEGUE AUTOMÁTICO EN RENDER.COM")
    print("="*50)
    
    # Verificar archivos requeridos
    if not verificar_archivos_requeridos():
        print("\n❌ Faltan archivos requeridos. No se puede continuar.")
        return
    
    # Verificar configuración de Git
    if not verificar_git():
        print("\n⚠️  Git no está configurado correctamente.")
        configurar = input("¿Quieres configurar Git ahora? (s/n): ").lower().strip()
        
        if configurar == 's':
            if not configurar_git_remote():
                print("❌ No se pudo configurar Git. Usando despliegue manual.")
                mostrar_instrucciones_manuales()
                return
        else:
            print("📋 Usando despliegue manual...")
            mostrar_instrucciones_manuales()
            return
    
    # Intentar despliegue automático
    print("\n🚀 Intentando despliegue automático...")
    if hacer_commit_y_push():
        print("\n🎉 ¡Despliegue automático completado!")
        print("⏳ Espera unos minutos para que Render procese los cambios")
        print("🌐 Tu aplicación estará disponible en la URL de Render")
    else:
        print("\n⚠️  El despliegue automático falló.")
        print("📋 Usando despliegue manual...")
        mostrar_instrucciones_manuales()

if __name__ == "__main__":
    main()
