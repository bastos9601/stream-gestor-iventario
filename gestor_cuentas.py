#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestor de Cuentas de Streaming
Sistema para gestionar inventario de cuentas de streaming
"""

import sqlite3
import os
from datetime import datetime
from colorama import init, Fore, Style
from tabulate import tabulate

# Inicializar colorama para colores en terminal
init(autoreset=True)

class GestorCuentas:
    def __init__(self, db_name="cuentas_streaming.db"):
        """Inicializar el gestor de cuentas"""
        self.db_name = db_name
        self.conn = None
        self.crear_tabla()
    
    def conectar_db(self):
        """Conectar a la base de datos SQLite"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.row_factory = sqlite3.Row
            return True
        except sqlite3.Error as e:
            print(f"{Fore.RED}Error al conectar a la base de datos: {e}{Style.RESET_ALL}")
            return False
    
    def desconectar_db(self):
        """Desconectar de la base de datos"""
        if self.conn:
            self.conn.close()
    
    def crear_tabla(self):
        """Crear la tabla de cuentas si no existe"""
        if not self.conectar_db():
            return
        
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cuentas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plataforma TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    estado TEXT DEFAULT 'disponible',
                    precio REAL NOT NULL,
                    fecha_compra DATE NOT NULL,
                    fecha_venta DATE,
                    notas TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.conn.commit()
            print(f"{Fore.GREEN}✓ Base de datos inicializada correctamente{Style.RESET_ALL}")
        except sqlite3.Error as e:
            print(f"{Fore.RED}Error al crear la tabla: {e}{Style.RESET_ALL}")
        finally:
            self.desconectar_db()
    
    def agregar_cuenta(self, plataforma, email, password, precio, fecha_compra=None, notas=""):
        """Agregar una nueva cuenta al inventario"""
        if not self.conectar_db():
            return False
        
        if fecha_compra is None:
            fecha_compra = datetime.now().strftime('%Y-%m-%d')
        
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO cuentas (plataforma, email, password, precio, fecha_compra, notas)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (plataforma, email, password, precio, fecha_compra, notas))
            self.conn.commit()
            print(f"{Fore.GREEN}✓ Cuenta agregada exitosamente{Style.RESET_ALL}")
            return True
        except sqlite3.IntegrityError:
            print(f"{Fore.RED}✗ Error: El email ya existe en la base de datos{Style.RESET_ALL}")
            return False
        except sqlite3.Error as e:
            print(f"{Fore.RED}Error al agregar cuenta: {e}{Style.RESET_ALL}")
            return False
        finally:
            self.desconectar_db()
    
    def listar_cuentas(self, estado=None, plataforma=None):
        """Listar todas las cuentas o filtrar por estado/plataforma"""
        if not self.conectar_db():
            return []
        
        try:
            cursor = self.conn.cursor()
            
            if estado and plataforma:
                cursor.execute('''
                    SELECT * FROM cuentas 
                    WHERE estado = ? AND plataforma = ?
                    ORDER BY fecha_compra DESC
                ''', (estado, plataforma))
            elif estado:
                cursor.execute('''
                    SELECT * FROM cuentas 
                    WHERE estado = ?
                    ORDER BY fecha_compra DESC
                ''', (estado,))
            elif plataforma:
                cursor.execute('''
                    SELECT * FROM cuentas 
                    WHERE plataforma = ?
                    ORDER BY fecha_compra DESC
                ''', (plataforma,))
            else:
                cursor.execute('SELECT * FROM cuentas ORDER BY fecha_compra DESC')
            
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"{Fore.RED}Error al listar cuentas: {e}{Style.RESET_ALL}")
            return []
        finally:
            self.desconectar_db()
    
    def buscar_cuenta(self, email):
        """Buscar una cuenta por email"""
        if not self.conectar_db():
            return None
        
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM cuentas WHERE email = ?', (email,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"{Fore.RED}Error al buscar cuenta: {e}{Style.RESET_ALL}")
            return None
        finally:
            self.desconectar_db()
    
    def vender_cuenta(self, email):
        """Marcar una cuenta como vendida"""
        if not self.conectar_db():
            return False
        
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE cuentas 
                SET estado = 'vendida', fecha_venta = ?
                WHERE email = ? AND estado = 'disponible'
            ''', (datetime.now().strftime('%Y-%m-%d'), email))
            
            if cursor.rowcount > 0:
                self.conn.commit()
                print(f"{Fore.GREEN}✓ Cuenta vendida exitosamente{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.YELLOW}✗ Cuenta no encontrada o ya vendida{Style.RESET_ALL}")
                return False
        except sqlite3.Error as e:
            print(f"{Fore.RED}Error al vender cuenta: {e}{Style.RESET_ALL}")
            return False
        finally:
            self.desconectar_db()
    
    def obtener_estadisticas(self):
        """Obtener estadísticas del inventario"""
        if not self.conectar_db():
            return {}
        
        try:
            cursor = self.conn.cursor()
            
            # Total de cuentas
            cursor.execute('SELECT COUNT(*) as total FROM cuentas')
            total = cursor.fetchone()['total']
            
            # Cuentas disponibles
            cursor.execute('SELECT COUNT(*) as disponibles FROM cuentas WHERE estado = "disponible"')
            disponibles = cursor.fetchone()['disponibles']
            
            # Cuentas vendidas
            cursor.execute('SELECT COUNT(*) as vendidas FROM cuentas WHERE estado = "vendida"')
            vendidas = cursor.fetchone()['vendidas']
            
            # Valor total del inventario
            cursor.execute('SELECT SUM(precio) as valor_total FROM cuentas WHERE estado = "disponible"')
            valor_total = cursor.fetchone()['valor_total'] or 0
            
            # Cuentas por plataforma
            cursor.execute('''
                SELECT plataforma, COUNT(*) as cantidad 
                FROM cuentas 
                WHERE estado = "disponible"
                GROUP BY plataforma
            ''')
            por_plataforma = cursor.fetchall()
            
            return {
                'total': total,
                'disponibles': disponibles,
                'vendidas': vendidas,
                'valor_total': valor_total,
                'por_plataforma': por_plataforma
            }
        except sqlite3.Error as e:
            print(f"{Fore.RED}Error al obtener estadísticas: {e}{Style.RESET_ALL}")
            return {}
        finally:
            self.desconectar_db()

def mostrar_menu():
    """Mostrar el menú principal"""
    print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║                GESTOR DE CUENTAS DE STREAMING                ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}Opciones disponibles:{Style.RESET_ALL}")
    print("1. Agregar nueva cuenta")
    print("2. Listar cuentas disponibles")
    print("3. Listar todas las cuentas")
    print("4. Buscar cuenta por email")
    print("5. Vender cuenta")
    print("6. Ver estadísticas")
    print("7. Salir")
    print(f"\n{Fore.BLUE}Selecciona una opción (1-7):{Style.RESET_ALL} ", end="")

def main():
    """Función principal del programa"""
    gestor = GestorCuentas()
    
    while True:
        mostrar_menu()
        opcion = input().strip()
        
        if opcion == "1":
            print(f"\n{Fore.GREEN}=== AGREGAR NUEVA CUENTA ==={Style.RESET_ALL}")
            plataforma = input("Plataforma (Netflix, Disney+, etc.): ").strip()
            email = input("Email: ").strip()
            password = input("Contraseña: ").strip()
            precio = input("Precio: ").strip()
            notas = input("Notas (opcional): ").strip()
            
            try:
                precio = float(precio)
                gestor.agregar_cuenta(plataforma, email, password, precio, notas=notas)
            except ValueError:
                print(f"{Fore.RED}✗ Error: El precio debe ser un número válido{Style.RESET_ALL}")
        
        elif opcion == "2":
            print(f"\n{Fore.GREEN}=== CUENTAS DISPONIBLES ==={Style.RESET_ALL}")
            cuentas = gestor.listar_cuentas(estado="disponible")
            if cuentas:
                datos = []
                for cuenta in cuentas:
                    datos.append([
                        cuenta['plataforma'],
                        cuenta['email'],
                        cuenta['precio'],
                        cuenta['fecha_compra'],
                        cuenta['notas'] or "Sin notas"
                    ])
                print(tabulate(datos, headers=['Plataforma', 'Email', 'Precio', 'Fecha Compra', 'Notas'], tablefmt='grid'))
            else:
                print(f"{Fore.YELLOW}No hay cuentas disponibles{Style.RESET_ALL}")
        
        elif opcion == "3":
            print(f"\n{Fore.GREEN}=== TODAS LAS CUENTAS ==={Style.RESET_ALL}")
            cuentas = gestor.listar_cuentas()
            if cuentas:
                datos = []
                for cuenta in cuentas:
                    estado_color = Fore.GREEN if cuenta['estado'] == 'disponible' else Fore.RED
                    datos.append([
                        cuenta['plataforma'],
                        cuenta['email'],
                        estado_color + cuenta['estado'] + Style.RESET_ALL,
                        cuenta['precio'],
                        cuenta['fecha_compra'],
                        cuenta['fecha_venta'] or "N/A"
                    ])
                print(tabulate(datos, headers=['Plataforma', 'Email', 'Estado', 'Precio', 'Fecha Compra', 'Fecha Venta'], tablefmt='grid'))
            else:
                print(f"{Fore.YELLOW}No hay cuentas en el inventario{Style.RESET_ALL}")
        
        elif opcion == "4":
            print(f"\n{Fore.GREEN}=== BUSCAR CUENTA ==={Style.RESET_ALL}")
            email = input("Email a buscar: ").strip()
            cuenta = gestor.buscar_cuenta(email)
            if cuenta:
                print(f"\n{Fore.GREEN}Cuenta encontrada:{Style.RESET_ALL}")
                print(f"Plataforma: {cuenta['plataforma']}")
                print(f"Email: {cuenta['email']}")
                print(f"Estado: {cuenta['estado']}")
                print(f"Precio: ${cuenta['precio']}")
                print(f"Fecha Compra: {cuenta['fecha_compra']}")
                if cuenta['fecha_venta']:
                    print(f"Fecha Venta: {cuenta['fecha_venta']}")
                if cuenta['notas']:
                    print(f"Notas: {cuenta['notas']}")
            else:
                print(f"{Fore.YELLOW}Cuenta no encontrada{Style.RESET_ALL}")
        
        elif opcion == "5":
            print(f"\n{Fore.GREEN}=== VENDER CUENTA ==={Style.RESET_ALL}")
            email = input("Email de la cuenta a vender: ").strip()
            gestor.vender_cuenta(email)
        
        elif opcion == "6":
            print(f"\n{Fore.GREEN}=== ESTADÍSTICAS DEL INVENTARIO ==={Style.RESET_ALL}")
            stats = gestor.obtener_estadisticas()
            if stats:
                print(f"Total de cuentas: {stats['total']}")
                print(f"Cuentas disponibles: {Fore.GREEN}{stats['disponibles']}{Style.RESET_ALL}")
                print(f"Cuentas vendidas: {Fore.RED}{stats['vendidas']}{Style.RESET_ALL}")
                print(f"Valor total del inventario: ${stats['valor_total']:.2f}")
                
                if stats['por_plataforma']:
                    print(f"\n{Fore.CYAN}Cuentas por plataforma:{Style.RESET_ALL}")
                    datos_plataforma = [[p['plataforma'], p['cantidad']] for p in stats['por_plataforma']]
                    print(tabulate(datos_plataforma, headers=['Plataforma', 'Cantidad'], tablefmt='grid'))
        
        elif opcion == "7":
            print(f"\n{Fore.GREEN}¡Gracias por usar el Gestor de Cuentas de Streaming!{Style.RESET_ALL}")
            break
        
        else:
            print(f"{Fore.RED}Opción no válida. Por favor selecciona 1-7.{Style.RESET_ALL}")
        
        input(f"\n{Fore.BLUE}Presiona Enter para continuar...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
