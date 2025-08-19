#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para ejecutar la aplicación web del Gestor de Cuentas de Streaming
"""

import os
import sys
from app import app, db
from config import get_config

def main():
    """Función principal para ejecutar la aplicación"""
    
    # Configurar el entorno
    config = get_config()
    app.config.from_object(config)
    
    # Crear la base de datos si no existe
    with app.app_context():
        db.create_all()
        print("✅ Base de datos inicializada correctamente")
    
    # Configuración del servidor
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = config.DEBUG
    
    print(f"🚀 Iniciando Gestor de Cuentas de Streaming...")
    print(f"📱 Aplicación web accesible desde cualquier dispositivo")
    print(f"🌐 URL: http://{host}:{port}")
    print(f"🔧 Modo: {'Desarrollo' if debug else 'Producción'}")
    print(f"💾 Base de datos: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print("\n" + "="*60)
    print("📱 ACCESO DESDE DISPOSITIVOS:")
    print("="*60)
    print(f"💻 Laptop/PC: http://localhost:{port}")
    print(f"📱 Celular/Tablet: http://[TU_IP_LOCAL]:{port}")
    print(f"🌍 Red local: http://{host}:{port}")
    print("="*60)
    print("\n💡 Para acceder desde otros dispositivos:")
    print("   1. Encuentra tu IP local (ipconfig en Windows, ifconfig en Mac/Linux)")
    print("   2. Asegúrate de que el firewall permita conexiones al puerto {port}")
    print("   3. Accede desde http://[TU_IP]:{port}")
    print("\n⏹️  Presiona Ctrl+C para detener el servidor")
    print("="*60)
    
    try:
        # Ejecutar la aplicación
        app.run(
            host=host,
            port=port,
            debug=debug,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor detenido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error al iniciar el servidor: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
