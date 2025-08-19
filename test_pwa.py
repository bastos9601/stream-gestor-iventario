#!/usr/bin/env python3
"""
Script de prueba para verificar la configuración PWA
"""

import os
import json
import requests

def test_manifest():
    """Verificar que el manifest.json sea válido"""
    print("🔍 Verificando manifest.json...")
    
    try:
        with open('static/manifest.json', 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        required_fields = ['name', 'short_name', 'start_url', 'display', 'theme_color']
        missing_fields = []
        
        for field in required_fields:
            if field not in manifest:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"❌ Campos faltantes en manifest: {', '.join(missing_fields)}")
            return False
        
        print("✅ manifest.json es válido")
        print(f"   Nombre: {manifest.get('name')}")
        print(f"   Nombre corto: {manifest.get('short_name')}")
        print(f"   URL de inicio: {manifest.get('start_url')}")
        print(f"   Modo de visualización: {manifest.get('display')}")
        
        return True
        
    except FileNotFoundError:
        print("❌ manifest.json no encontrado")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Error en JSON: {e}")
        return False

def test_service_worker():
    """Verificar que el service worker exista"""
    print("\n🔍 Verificando service worker...")
    
    if os.path.exists('static/sw.js'):
        print("✅ sw.js encontrado")
        
        # Verificar contenido básico
        with open('static/sw.js', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'CACHE_NAME' in content and 'install' in content:
            print("✅ Service worker tiene funcionalidad básica")
            return True
        else:
            print("❌ Service worker parece estar incompleto")
            return False
    else:
        print("❌ sw.js no encontrado")
        return False

def test_icons():
    """Verificar que los iconos existan"""
    print("\n🔍 Verificando iconos...")
    
    icon_dir = 'static/icons'
    if not os.path.exists(icon_dir):
        print("❌ Directorio de iconos no encontrado")
        return False
    
    required_icons = [
        'icon-72x72.png',
        'icon-96x96.png',
        'icon-128x128.png',
        'icon-144x144.png',
        'icon-152x152.png',
        'icon-192x192.png',
        'icon-384x384.png',
        'icon-512x512.png'
    ]
    
    missing_icons = []
    for icon in required_icons:
        if not os.path.exists(os.path.join(icon_dir, icon)):
            missing_icons.append(icon)
    
    if missing_icons:
        print(f"❌ Iconos faltantes: {', '.join(missing_icons)}")
        print("💡 Ejecuta: python generate_icons.py")
        return False
    
    print("✅ Todos los iconos están presentes")
    return True

def test_pwa_files():
    """Verificar archivos de configuración PWA"""
    print("\n🔍 Verificando archivos de configuración PWA...")
    
    pwa_files = [
        'twa-manifest.json',
        'pwa-builder.json',
        'templates/apk.html'
    ]
    
    missing_files = []
    for file in pwa_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Archivos faltantes: {', '.join(missing_files)}")
        return False
    
    print("✅ Todos los archivos de configuración PWA están presentes")
    return True

def test_base_template():
    """Verificar que base.html tenga la configuración PWA"""
    print("\n🔍 Verificando configuración PWA en base.html...")
    
    try:
        with open('templates/base.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_elements = [
            'manifest.json',
            'theme-color',
            'apple-mobile-web-app-capable',
            'serviceWorker.register'
        ]
        
        missing_elements = []
        for element in required_elements:
            if element not in content:
                missing_elements.append(element)
        
        if missing_elements:
            print(f"❌ Elementos PWA faltantes: {', '.join(missing_elements)}")
            return False
        
        print("✅ base.html tiene configuración PWA completa")
        return True
        
    except FileNotFoundError:
        print("❌ base.html no encontrado")
        return False

def test_apk_route():
    """Verificar que la ruta /apk esté configurada"""
    print("\n🔍 Verificando ruta /apk...")
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if '@app.route(\'/apk\')' in content:
            print("✅ Ruta /apk configurada en app.py")
            return True
        else:
            print("❌ Ruta /apk no encontrada en app.py")
            return False
            
    except FileNotFoundError:
        print("❌ app.py no encontrado")
        return False

def main():
    """Función principal de verificación PWA"""
    print("📱 VERIFICACIÓN DE CONFIGURACIÓN PWA")
    print("=" * 50)
    
    tests = [
        test_manifest,
        test_service_worker,
        test_icons,
        test_pwa_files,
        test_base_template,
        test_apk_route
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
        print("🎉 ¡TODAS LAS VERIFICACIONES PWA PASARON!")
        print("✅ Tu aplicación está lista para generar APK")
        print("\n📋 Próximos pasos:")
        print("1. Despliega tu aplicación en Render")
        print("2. Ve a PWA Builder: https://www.pwabuilder.com/")
        print("3. Pega la URL: https://gestor-cuentas-streaming.onrender.com")
        print("4. Haz clic en 'Build My PWA'")
        print("5. Descarga el APK para Android")
        print("\n🌐 URL de producción:")
        print("https://gestor-cuentas-streaming.onrender.com")
        print("\n📱 Características PWA implementadas:")
        print("   • Manifest completo y válido")
        print("   • Service Worker para offline")
        print("   • Iconos en todos los tamaños")
        print("   • Configuración para PWA Builder")
        print("   • Página de instrucciones APK")
        print("   • Integración completa en base.html")
    else:
        print("❌ ALGUNAS VERIFICACIONES PWA FALLARON")
        print("🔧 Revisa los errores antes de generar APK")
        print("\n💡 Consejos:")
        print("- Ejecuta: python generate_icons.py")
        print("- Verifica que todos los archivos estén presentes")
        print("- Confirma que la configuración PWA esté completa")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
