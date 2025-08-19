#!/usr/bin/env python3
"""
Script de prueba para verificar que la aplicación esté lista para despliegue en Render
"""

import os
import sys
import importlib.util

def test_dependencies():
    """Verificar que todas las dependencias estén disponibles"""
    print("🔍 Verificando dependencias...")
    
    required_packages = [
        'flask',
        'flask_sqlalchemy', 
        'flask_login',
        'werkzeug',
        'gunicorn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - NO INSTALADO")
    
    if missing_packages:
        print(f"\n❌ Faltan dependencias: {', '.join(missing_packages)}")
        print("Ejecuta: pip install -r requirements.txt")
        return False
    
    print("✅ Todas las dependencias están instaladas")
    return True

def test_files():
    """Verificar que todos los archivos necesarios existan"""
    print("\n📁 Verificando archivos de configuración...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'render.yaml',
        'Procfile',
        'runtime.txt',
        '.gitignore'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            missing_files.append(file)
            print(f"❌ {file} - NO ENCONTRADO")
    
    if missing_files:
        print(f"\n❌ Faltan archivos: {', '.join(missing_files)}")
        return False
    
    print("✅ Todos los archivos de configuración están presentes")
    return True

def test_app_structure():
    """Verificar la estructura de la aplicación"""
    print("\n🏗️ Verificando estructura de la aplicación...")
    
    required_dirs = [
        'templates',
        'static'
    ]
    
    required_templates = [
        'templates/base.html',
        'templates/login.html',
        'templates/index.html',
        'templates/usuarios.html',
        'templates/nuevo_usuario.html',
        'templates/perfil.html'
    ]
    
    # Verificar directorios
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ Directorio: {dir_name}")
        else:
            print(f"❌ Directorio: {dir_name} - NO ENCONTRADO")
    
    # Verificar plantillas
    for template in required_templates:
        if os.path.exists(template):
            print(f"✅ Plantilla: {template}")
        else:
            print(f"❌ Plantilla: {template} - NO ENCONTRADA")
    
    return True

def test_requirements_txt():
    """Verificar que requirements.txt esté correcto"""
    print("\n📦 Verificando requirements.txt...")
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
            
        required_packages = [
            'Flask==',
            'Flask-SQLAlchemy==',
            'Flask-Login==',
            'Werkzeug==',
            'gunicorn=='
        ]
        
        missing_packages = []
        for package in required_packages:
            if package in content:
                print(f"✅ {package}")
            else:
                missing_packages.append(package)
                print(f"❌ {package} - NO ENCONTRADO")
        
        if missing_packages:
            print(f"\n❌ Faltan paquetes en requirements.txt: {', '.join(missing_packages)}")
            return False
        
        print("✅ requirements.txt está correctamente configurado")
        return True
        
    except FileNotFoundError:
        print("❌ requirements.txt no encontrado")
        return False

def test_render_config():
    """Verificar configuración de Render"""
    print("\n⚙️ Verificando configuración de Render...")
    
    try:
        with open('render.yaml', 'r') as f:
            content = f.read()
            
        required_configs = [
            'type: web',
            'env: python',
            'plan: free',
            'buildCommand:',
            'startCommand:',
            'gunicorn app:app'
        ]
        
        missing_configs = []
        for config in required_configs:
            if config in content:
                print(f"✅ {config}")
            else:
                missing_configs.append(config)
                print(f"❌ {config} - NO ENCONTRADO")
        
        if missing_configs:
            print(f"\n❌ Falta configuración en render.yaml: {', '.join(missing_configs)}")
            return False
        
        print("✅ render.yaml está correctamente configurado")
        return True
        
    except FileNotFoundError:
        print("❌ render.yaml no encontrado")
        return False

def main():
    """Función principal de verificación"""
    print("🚀 VERIFICACIÓN PARA DESPLIEGUE EN RENDER")
    print("=" * 50)
    
    tests = [
        test_dependencies,
        test_files,
        test_app_structure,
        test_requirements_txt,
        test_render_config
    ]
    
    all_passed = True
    
    for test in tests:
        try:
            if not test():
                all_passed = False
        except Exception as e:
            print(f"❌ Error en prueba: {e}")
            all_passed = False
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("🎉 ¡TODAS LAS VERIFICACIONES PASARON!")
        print("✅ Tu aplicación está lista para desplegar en Render")
        print("\n📋 Próximos pasos:")
        print("1. Sube tu código a GitHub")
        print("2. Ve a render.com y crea un nuevo Web Service")
        print("3. Conecta tu repositorio de GitHub")
        print("4. Render detectará automáticamente la configuración")
        print("5. Haz clic en 'Create Web Service'")
        print("\n🌐 Tu aplicación estará disponible en:")
        print("https://gestor-cuentas-streaming.onrender.com")
    else:
        print("❌ ALGUNAS VERIFICACIONES FALLARON")
        print("🔧 Revisa los errores antes de desplegar")
        print("\n💡 Consejos:")
        print("- Ejecuta: pip install -r requirements.txt")
        print("- Verifica que todos los archivos estén presentes")
        print("- Asegúrate de que la aplicación funcione localmente")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
