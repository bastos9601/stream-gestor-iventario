#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de logout
"""

import requests
import time

def test_logout_functionality():
    """Probar la funcionalidad de logout"""
    base_url = "http://localhost:5000"
    
    print("🧪 Probando funcionalidad de logout...")
    print("=" * 50)
    
    # 1. Intentar acceder al dashboard sin login (debería redirigir a login)
    print("1. Probando acceso sin autenticación...")
    try:
        response = requests.get(f"{base_url}/", allow_redirects=False)
        if response.status_code == 302:
            print("✅ Correcto: Redirigido a login (sin autenticación)")
        else:
            print(f"❌ Error: Status code inesperado: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # 2. Probar la ruta de login
    print("\n2. Probando página de login...")
    try:
        response = requests.get(f"{base_url}/login")
        if response.status_code == 200:
            print("✅ Correcto: Página de login accesible")
        else:
            print(f"❌ Error: Status code inesperado: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # 3. Probar la ruta de logout
    print("\n3. Probando ruta de logout...")
    try:
        response = requests.get(f"{base_url}/logout", allow_redirects=False)
        if response.status_code == 302:
            print("✅ Correcto: Logout redirige correctamente")
        else:
            print(f"❌ Error: Status code inesperado: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Pruebas completadas!")
    print("\n📋 Para probar manualmente:")
    print("1. Ve a: http://localhost:5000/login")
    print("2. Ingresa con: admin / admin123")
    print("3. Verifica que aparezca el botón 'Cerrar Sesión'")
    print("4. Haz clic en 'Cerrar Sesión' para probar")

if __name__ == "__main__":
    test_logout_functionality()
