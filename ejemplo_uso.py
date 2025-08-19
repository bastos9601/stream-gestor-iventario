#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplo de uso del Gestor de Cuentas de Streaming
Este script demuestra cómo usar la clase GestorCuentas programáticamente
"""

from gestor_cuentas import GestorCuentas
from datetime import datetime

def ejemplo_uso():
    """Ejemplo completo de uso del gestor de cuentas"""
    
    print("🎬 EJEMPLO DE USO DEL GESTOR DE CUENTAS DE STREAMING")
    print("=" * 60)
    
    # Crear instancia del gestor
    gestor = GestorCuentas("ejemplo_cuentas.db")
    
    # Agregar algunas cuentas de ejemplo
    print("\n📝 Agregando cuentas de ejemplo...")
    
    cuentas_ejemplo = [
        {
            "plataforma": "Netflix",
            "email": "netflix1@ejemplo.com",
            "password": "pass123",
            "precio": 12.99,
            "notas": "Cuenta premium 4K, 4 pantallas"
        },
        {
            "plataforma": "Disney+",
            "email": "disney1@ejemplo.com",
            "password": "disney456",
            "precio": 8.99,
            "notas": "Cuenta familiar, 4K HDR"
        },
        {
            "plataforma": "HBO Max",
            "email": "hbo1@ejemplo.com",
            "password": "hbo789",
            "precio": 14.99,
            "notas": "Cuenta premium, sin anuncios"
        },
        {
            "plataforma": "Netflix",
            "email": "netflix2@ejemplo.com",
            "password": "netflix2024",
            "precio": 15.99,
            "notas": "Cuenta estándar, 2 pantallas"
        }
    ]
    
    for cuenta in cuentas_ejemplo:
        gestor.agregar_cuenta(
            cuenta["plataforma"],
            cuenta["email"],
            cuenta["password"],
            cuenta["precio"],
            notas=cuenta["notas"]
        )
    
    # Mostrar estadísticas iniciales
    print("\n📊 Estadísticas iniciales:")
    stats = gestor.obtener_estadisticas()
    if stats:
        print(f"Total de cuentas: {stats['total']}")
        print(f"Cuentas disponibles: {stats['disponibles']}")
        print(f"Valor total del inventario: ${stats['valor_total']:.2f}")
    
    # Listar todas las cuentas
    print("\n📋 Todas las cuentas en el inventario:")
    cuentas = gestor.listar_cuentas()
    for cuenta in cuentas:
        estado_icono = "✅" if cuenta['estado'] == 'disponible' else "💰"
        print(f"{estado_icono} {cuenta['plataforma']} - {cuenta['email']} - ${cuenta['precio']} - {cuenta['estado']}")
    
    # Buscar una cuenta específica
    print("\n🔍 Buscando cuenta específica...")
    cuenta_encontrada = gestor.buscar_cuenta("netflix1@ejemplo.com")
    if cuenta_encontrada:
        print(f"Cuenta encontrada: {cuenta_encontrada['plataforma']} - {cuenta_encontrada['email']}")
    
    # Vender una cuenta
    print("\n💰 Vendiendo una cuenta...")
    gestor.vender_cuenta("disney1@ejemplo.com")
    
    # Mostrar estadísticas después de la venta
    print("\n📊 Estadísticas después de la venta:")
    stats_actualizadas = gestor.obtener_estadisticas()
    if stats_actualizadas:
        print(f"Total de cuentas: {stats_actualizadas['total']}")
        print(f"Cuentas disponibles: {stats_actualizadas['disponibles']}")
        print(f"Cuentas vendidas: {stats_actualizadas['vendidas']}")
        print(f"Valor total del inventario: ${stats_actualizadas['valor_total']:.2f}")
    
    # Listar cuentas por plataforma
    print("\n🏷️ Cuentas por plataforma:")
    if stats_actualizadas and stats_actualizadas['por_plataforma']:
        for plataforma in stats_actualizadas['por_plataforma']:
            print(f"  {plataforma['plataforma']}: {plataforma['cantidad']} cuentas")
    
    # Listar solo cuentas disponibles
    print("\n✅ Cuentas disponibles para venta:")
    cuentas_disponibles = gestor.listar_cuentas(estado="disponible")
    for cuenta in cuentas_disponibles:
        print(f"  {cuenta['plataforma']} - {cuenta['email']} - ${cuenta['precio']}")
    
    print("\n🎉 ¡Ejemplo completado!")
    print("Puedes ejecutar 'python gestor_cuentas.py' para usar la interfaz interactiva.")

if __name__ == "__main__":
    ejemplo_uso()
