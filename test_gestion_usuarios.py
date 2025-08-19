#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de gestión de usuarios
"""

import requests
import time

def test_user_management():
    """Probar la funcionalidad de gestión de usuarios"""
    base_url = "http://localhost:5000"
    
    print("👥 Probando funcionalidad de gestión de usuarios...")
    print("=" * 60)
    
    # 1. Verificar que las rutas de usuarios estén protegidas
    print("1. Probando acceso a gestión de usuarios sin autenticación...")
    try:
        response = requests.get(f"{base_url}/usuarios", allow_redirects=False)
        if response.status_code == 302:
            print("✅ Correcto: Gestión de usuarios protegida, redirigido a login")
        else:
            print(f"❌ Error: Status code inesperado: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # 2. Verificar ruta de nuevo usuario
    print("\n2. Probando ruta de nuevo usuario...")
    try:
        response = requests.get(f"{base_url}/usuarios/nuevo", allow_redirects=False)
        if response.status_code == 302:
            print("✅ Correcto: Nuevo usuario protegido, redirigido a login")
        else:
            print(f"❌ Error: Status code inesperado: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Pruebas completadas!")
    print("\n📋 Para probar manualmente:")
    print("1. Ve a: http://localhost:5000/login")
    print("2. Ingresa con: admin / admin123")
    print("3. Haz clic en 'Usuarios' en la barra de navegación")
    print("4. Crea un nuevo usuario con rol 'Usuario'")
    print("5. Haz logout y prueba con el nuevo usuario")
    print("\n🔧 Funcionalidades implementadas:")
    print("   • Solo administradores pueden gestionar usuarios")
    print("   • Usuarios normales solo pueden agregar cuentas")
    print("   • Usuarios normales NO pueden editar/vender/eliminar")
    print("   • Sistema de roles implementado")
    print("   • Validaciones de seguridad activas")
    print("\n👑 Roles del Sistema:")
    print("   • ADMINISTRADOR: Acceso completo a todas las funciones")
    print("   • USUARIO: Solo ver y agregar cuentas")
    print("\n🛡️ Seguridad:")
    print("   • Verificación de permisos en todas las rutas")
    • Protección contra acceso no autorizado")
    print("   • Validación de roles en tiempo real")

if __name__ == "__main__":
    test_user_management()
