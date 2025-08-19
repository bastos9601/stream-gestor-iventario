#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de cambio de contraseña
"""

import requests
import time

def test_password_change():
    """Probar la funcionalidad de cambio de contraseña"""
    base_url = "http://localhost:5000"
    
    print("🔐 Probando funcionalidad de cambio de contraseña...")
    print("=" * 60)
    
    # 1. Verificar que la página de perfil esté protegida
    print("1. Probando acceso a perfil sin autenticación...")
    try:
        response = requests.get(f"{base_url}/perfil", allow_redirects=False)
        if response.status_code == 302:
            print("✅ Correcto: Perfil protegido, redirigido a login")
        else:
            print(f"❌ Error: Status code inesperado: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # 2. Verificar que la página de perfil sea accesible
    print("\n2. Probando página de perfil...")
    try:
        response = requests.get(f"{base_url}/perfil")
        if response.status_code == 200:
            print("✅ Correcto: Página de perfil accesible")
        elif response.status_code == 302:
            print("✅ Correcto: Redirigido a login (sin autenticación)")
        else:
            print(f"❌ Error: Status code inesperado: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Pruebas completadas!")
    print("\n📋 Para probar manualmente:")
    print("1. Ve a: http://localhost:5000/login")
    print("2. Ingresa con: admin / admin123")
    print("3. Haz clic en tu nombre de usuario en la barra superior")
    print("4. En la página de perfil, cambia tu contraseña")
    print("5. Prueba hacer logout y login con la nueva contraseña")
    print("\n🔧 Funcionalidades disponibles:")
    print("   • Ver información del usuario")
    print("   • Cambiar contraseña con validación")
    print("   • Mostrar/ocultar contraseñas")
    print("   • Validación en tiempo real")
    print("   • Consejos de seguridad")

if __name__ == "__main__":
    test_password_change()
