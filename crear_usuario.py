#!/usr/bin/env python3
"""
Script para crear usuarios en el sistema de gestión de cuentas de streaming
"""

from app import app, db, Usuario

def crear_usuario(username, email, password, es_admin=False):
    """Crear un nuevo usuario en el sistema"""
    with app.app_context():
        # Verificar si el usuario ya existe
        usuario_existente = Usuario.query.filter_by(username=username).first()
        if usuario_existente:
            print(f"❌ El usuario '{username}' ya existe")
            return False
        
        # Crear nuevo usuario
        nuevo_usuario = Usuario(
            username=username,
            email=email,
            es_admin=es_admin
        )
        nuevo_usuario.set_password(password)
        
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            print(f"✅ Usuario '{username}' creado exitosamente")
            print(f"   Email: {email}")
            print(f"   Admin: {'Sí' if es_admin else 'No'}")
            return True
        except Exception as e:
            print(f"❌ Error al crear usuario: {str(e)}")
            db.session.rollback()
            return False

def listar_usuarios():
    """Listar todos los usuarios del sistema"""
    with app.app_context():
        usuarios = Usuario.query.all()
        if not usuarios:
            print("No hay usuarios en el sistema")
            return
        
        print("\n📋 Usuarios del sistema:")
        print("-" * 50)
        for usuario in usuarios:
            print(f"👤 {usuario.username}")
            print(f"   📧 {usuario.email}")
            print(f"   🔑 Admin: {'Sí' if usuario.es_admin else 'No'}")
            print(f"   📅 Registro: {usuario.fecha_registro.strftime('%d/%m/%Y %H:%M')}")
            print("-" * 50)

def main():
    print("🔐 Sistema de Gestión de Usuarios")
    print("=" * 40)
    
    while True:
        print("\nOpciones:")
        print("1. Crear usuario")
        print("2. Listar usuarios")
        print("3. Salir")
        
        opcion = input("\nSelecciona una opción (1-3): ").strip()
        
        if opcion == "1":
            print("\n📝 Crear nuevo usuario:")
            username = input("Usuario: ").strip()
            email = input("Email: ").strip()
            password = input("Contraseña: ").strip()
            
            if not username or not email or not password:
                print("❌ Todos los campos son obligatorios")
                continue
            
            es_admin_input = input("¿Es administrador? (s/n): ").strip().lower()
            es_admin = es_admin_input in ['s', 'si', 'sí', 'y', 'yes']
            
            crear_usuario(username, email, password, es_admin)
            
        elif opcion == "2":
            listar_usuarios()
            
        elif opcion == "3":
            print("👋 ¡Hasta luego!")
            break
            
        else:
            print("❌ Opción no válida")

if __name__ == "__main__":
    main()
