#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestor de Cuentas de Streaming - Aplicación Web
Sistema web para gestionar inventario de cuentas de streaming desde cualquier dispositivo
ADAPTADO PARA INFINITYFREE
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# Función para manejar collations según el tipo de base de datos
def get_collation():
    """Retorna la collation apropiada según el tipo de base de datos"""
    if os.getenv('FLASK_ENV') == 'development' or not os.getenv('DB_HOST'):
        return None  # SQLite no soporta collations personalizadas
    else:
        return 'utf8mb4_unicode_ci'  # MySQL

app = Flask(__name__)

# Configuración para InfinityFree
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'tu-clave-secreta-aqui-infinityfree')

# Configuración de base de datos
# Para desarrollo local usa SQLite, para producción usa MySQL
if os.getenv('FLASK_ENV') == 'development' or not os.getenv('DB_HOST'):
    # Configuración para desarrollo local con SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///streaming_accounts.db'
    print("🔧 Modo desarrollo: Usando SQLite")
else:
    # Configuración para MySQL en InfinityFree
    DB_HOST = os.getenv('DB_HOST', 'sql.infinityfree.com')
    DB_NAME = os.getenv('DB_NAME', 'tu_base_datos')
    DB_USER = os.getenv('DB_USER', 'tu_usuario')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'tu_contraseña')
    
    # Construir la URI de MySQL para InfinityFree usando PyMySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    print("🚀 Modo producción: Usando MySQL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración del motor de base de datos
if os.getenv('FLASK_ENV') == 'development' or not os.getenv('DB_HOST'):
    # Configuración para SQLite (desarrollo)
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True
    }
else:
    # Configuración optimizada para MySQL en InfinityFree con PyMySQL
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 5,  # Reducido para InfinityFree
        'pool_timeout': 10,
        'pool_recycle': 3600,  # Reciclar conexiones cada hora
        'max_overflow': 2,
        'connect_args': {
            'charset': 'utf8mb4',  # Soporte completo para caracteres especiales
            'connect_timeout': 10
        }
    }

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Modelo de Usuario
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80, collation=get_collation()), unique=True, nullable=False)
    email = db.Column(db.String(120, collation=get_collation()), unique=True, nullable=False)
    password_hash = db.Column(db.String(200, collation=get_collation()), nullable=False)
    es_admin = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    
    # Relación con cuentas
    cuentas = db.relationship('Cuenta', backref='usuario', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Modelo de Cuenta (actualizado para MySQL)
class Cuenta(db.Model):
    """Modelo de la base de datos para las cuentas"""
    id = db.Column(db.Integer, primary_key=True)
    plataforma = db.Column(db.String(100, collation=get_collation()), nullable=False)
    email = db.Column(db.String(120, collation=get_collation()), nullable=False)
    password = db.Column(db.String(200, collation=get_collation()), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    fecha_compra = db.Column(db.Date, nullable=False)
    notas = db.Column(db.Text(collation=get_collation()))
    estado = db.Column(db.String(20, collation=get_collation()), default='Disponible')
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_venta = db.Column(db.DateTime)
    nombre_comprador = db.Column(db.String(100, collation=get_collation()))
    whatsapp_comprador = db.Column(db.String(20, collation=get_collation()))
    fecha_vencimiento = db.Column(db.Date)
    
    # Nuevo campo para asociar cuentas con usuarios
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE'), nullable=False)
    
    def to_dict(self):
        """Convertir objeto a diccionario para JSON"""
        return {
            'id': self.id,
            'plataforma': self.plataforma,
            'email': self.email,
            'password': self.password,
            'precio': self.precio,
            'fecha_compra': self.fecha_compra.strftime('%Y-%m-%d') if self.fecha_compra else None,
            'notas': self.notas,
            'estado': self.estado,
            'fecha_creacion': self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_creacion else None,
            'fecha_venta': self.fecha_venta.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_venta else None,
            'nombre_comprador': self.nombre_comprador,
            'whatsapp_comprador': self.whatsapp_comprador,
            'fecha_vencimiento': self.fecha_vencimiento.strftime('%Y-%m-%d') if self.fecha_vencimiento else None,
            'usuario_id': self.usuario_id,
        }

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Primero buscar el usuario sin filtrar por activo
        usuario = Usuario.query.filter_by(username=username).first()
        
        if usuario:
            # Verificar si el usuario está inactivo
            if not usuario.activo:
                flash('Usuario vencido. Contacta a tu administrador por WhatsApp.', 'error')
                return render_template('login.html', usuario_inactivo=True, nombre_usuario=username)
            
            # Verificar contraseña
            if usuario.check_password(password):
                login_user(usuario)
                flash(f'¡Bienvenido, {usuario.username}!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Contraseña incorrecta', 'error')
        else:
            flash('Usuario no encontrado', 'error')
    
    return render_template('login.html')

@app.route('/perfil')
@login_required
def perfil():
    """Perfil del usuario actual"""
    return render_template('perfil.html', usuario=current_user)

@app.route('/perfil/cambiar_password', methods=['POST'])
@login_required
def cambiar_password():
    """Cambiar contraseña del usuario actual"""
    password_actual = request.form.get('password_actual')
    nueva_password = request.form.get('nueva_password')
    confirmar_password = request.form.get('confirmar_password')
    
    if not current_user.check_password(password_actual):
        flash('La contraseña actual es incorrecta', 'error')
        return redirect(url_for('perfil'))
    
    if nueva_password != confirmar_password:
        flash('Las contraseñas nuevas no coinciden', 'error')
        return redirect(url_for('perfil'))
    
    if len(nueva_password) < 6:
        flash('La nueva contraseña debe tener al menos 6 caracteres', 'error')
        return redirect(url_for('perfil'))
    
    current_user.set_password(nueva_password)
    db.session.commit()
    
    flash('Contraseña cambiada correctamente', 'success')
    return redirect(url_for('perfil'))

@app.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    logout_user()
    flash('Has cerrado sesión correctamente', 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    """Página principal con estadísticas"""
    if current_user.es_admin:
        # Administrador ve todas las cuentas
        total_cuentas = Cuenta.query.count()
        cuentas_disponibles = Cuenta.query.filter_by(estado='Disponible').count()
        cuentas_vendidas = Cuenta.query.filter_by(estado='Vendida').count()
        
        # Calcular valor total del inventario (solo cuentas disponibles)
        valor_inventario_admin = db.session.query(db.func.sum(Cuenta.precio)).filter_by(estado='Disponible').scalar() or 0
        
        # Calcular valor total de las ventas
        valor_total_ventas_admin = db.session.query(db.func.sum(Cuenta.precio)).filter_by(estado='Vendida').scalar() or 0
        
        # Obtener cuentas próximas a vencer (menos de 7 días)
        today = date.today()
        cuentas_proximas_vencer = Cuenta.query.filter(
            Cuenta.fecha_vencimiento.isnot(None),
            Cuenta.fecha_vencimiento >= today,
            Cuenta.fecha_vencimiento <= today + timedelta(days=7)
        ).order_by(Cuenta.fecha_vencimiento.asc()).all()
        
        # Calcular total de cuentas por vencer
        total_cuentas_por_vencer = len(cuentas_proximas_vencer)
        
        # Calcular cuentas activas (con fecha de vencimiento futura)
        cuentas_activas = Cuenta.query.filter(
            Cuenta.fecha_vencimiento.isnot(None),
            Cuenta.fecha_vencimiento > today
        ).count()
        
        # Estadísticas por usuario
        usuarios_stats = db.session.query(
            Usuario.username,
            db.func.count(Cuenta.id).label('total_cuentas'),
            db.func.count(Cuenta.id).filter(Cuenta.estado == 'Disponible').label('cuentas_disponibles'),
            db.func.count(Cuenta.id).filter(Cuenta.estado == 'Vendida').label('cuentas_vendidas')
        ).outerjoin(Cuenta).group_by(Usuario.id, Usuario.username).all()
        
        # Últimas cuentas agregadas por todos los usuarios
        ultimas_cuentas = db.session.query(Cuenta).join(Usuario).order_by(Cuenta.fecha_creacion.desc()).limit(10).all()
        
    else:
        # Usuario normal solo ve sus propias cuentas
        total_cuentas = Cuenta.query.filter_by(usuario_id=current_user.id).count()
        cuentas_disponibles = Cuenta.query.filter_by(usuario_id=current_user.id, estado='Disponible').count()
        cuentas_vendidas = Cuenta.query.filter_by(usuario_id=current_user.id, estado='Vendida').count()
        
        # Calcular valor del inventario del usuario (solo cuentas disponibles)
        valor_inventario_usuario = db.session.query(db.func.sum(Cuenta.precio)).filter_by(
            usuario_id=current_user.id, 
            estado='Disponible'
        ).scalar() or 0
        
        # Calcular valor total de las ventas del usuario
        valor_total_ventas_usuario = db.session.query(db.func.sum(Cuenta.precio)).filter_by(
            usuario_id=current_user.id, 
            estado='Vendida'
        ).scalar() or 0
        
        # Obtener cuentas próximas a vencer del usuario (menos de 7 días)
        today = date.today()
        cuentas_proximas_vencer = Cuenta.query.filter(
            Cuenta.usuario_id == current_user.id,
            Cuenta.fecha_vencimiento.isnot(None),
            Cuenta.fecha_vencimiento >= today,
            Cuenta.fecha_vencimiento <= today + timedelta(days=7)
        ).order_by(Cuenta.fecha_vencimiento.asc()).all()
        
        # Calcular total de cuentas por vencer
        total_cuentas_por_vencer = len(cuentas_proximas_vencer)
        
        # Calcular cuentas activas del usuario (con fecha de vencimiento futura)
        cuentas_activas_usuario = Cuenta.query.filter(
            Cuenta.usuario_id == current_user.id,
            Cuenta.fecha_vencimiento.isnot(None),
            Cuenta.fecha_vencimiento > today
        ).count()
        
        usuarios_stats = None
        ultimas_cuentas = Cuenta.query.filter_by(usuario_id=current_user.id).order_by(Cuenta.fecha_creacion.desc()).limit(5).all()
    
    # Cuentas por plataforma (todas las cuentas, independientemente del estado)
    if current_user.es_admin:
        plataformas = db.session.query(
            Cuenta.plataforma, 
            db.func.count(Cuenta.id).label('cantidad')
        ).group_by(Cuenta.plataforma).all()
    else:
        plataformas = db.session.query(
            Cuenta.plataforma, 
            db.func.count(Cuenta.id).label('cantidad')
        ).filter_by(usuario_id=current_user.id).group_by(Cuenta.plataforma).all()
    
    return render_template('index.html',
                         total_cuentas=total_cuentas,
                         cuentas_disponibles=cuentas_disponibles,
                         cuentas_vendidas=cuentas_vendidas,
                         cuentas_activas=cuentas_activas if current_user.es_admin else cuentas_activas_usuario,
                         plataformas=plataformas,
                         ultimas_cuentas=ultimas_cuentas,
                         usuarios_stats=usuarios_stats,
                         valor_inventario_admin=valor_inventario_admin if current_user.es_admin else 0,
                         valor_inventario_usuario=valor_inventario_usuario if not current_user.es_admin else 0,
                         valor_total_ventas_admin=valor_total_ventas_admin if current_user.es_admin else 0,
                         valor_total_ventas_usuario=valor_total_ventas_usuario if not current_user.es_admin else 0,
                         cuentas_proximas_vencer=cuentas_proximas_vencer,
                         total_cuentas_por_vencer=total_cuentas_por_vencer,
                         today=today)

@app.route('/cuentas')
@login_required
def cuentas():
    """Lista de cuentas"""
    plataforma = request.args.get('plataforma', '')
    estado = request.args.get('estado', '')
    today = datetime.now().date()
    
    if current_user.es_admin:
        # Administrador ve todas las cuentas
        query = Cuenta.query
        if plataforma:
            query = query.filter_by(plataforma=plataforma)
        if estado:
            if estado == 'Por Vencer':
                # Cuentas que vencen en los próximos 7 días
                query = query.filter(
                    Cuenta.fecha_vencimiento.isnot(None),
                    Cuenta.fecha_vencimiento >= today,
                    Cuenta.fecha_vencimiento <= today + timedelta(days=7)
                )
            elif estado == 'Vencida':
                # Cuentas que ya vencieron
                query = query.filter(
                    Cuenta.fecha_vencimiento.isnot(None),
                    Cuenta.fecha_vencimiento < today
                )
            else:
                # Estados normales (Disponible, Vendida)
                query = query.filter_by(estado=estado)
    else:
        # Usuario normal solo ve sus propias cuentas
        query = Cuenta.query.filter_by(usuario_id=current_user.id)
        if plataforma:
            query = query.filter_by(plataforma=plataforma)
        if estado:
            if estado == 'Por Vencer':
                # Cuentas que vencen en los próximos 7 días
                query = query.filter(
                    Cuenta.fecha_vencimiento.isnot(None),
                    Cuenta.fecha_vencimiento >= today,
                    Cuenta.fecha_vencimiento <= today + timedelta(days=7)
                )
            elif estado == 'Vencida':
                # Cuentas que ya vencieron
                query = query.filter(
                    Cuenta.fecha_vencimiento.isnot(None),
                    Cuenta.fecha_vencimiento < today
                )
            else:
                # Estados normales (Disponible, Vendida)
                query = query.filter_by(estado=estado)
    
    cuentas = query.order_by(Cuenta.fecha_creacion.desc()).all()
    plataformas_disponibles = db.session.query(Cuenta.plataforma).distinct().all()
    
    # Calcular estadísticas completas
    total_cuentas = len(cuentas)
    cuentas_disponibles = len([c for c in cuentas if c.estado == 'Disponible'])
    cuentas_vendidas = len([c for c in cuentas if c.estado == 'Vendida'])
    
    # Calcular cuentas por vencer y vencidas
    cuentas_por_vencer = len([c for c in cuentas if c.fecha_vencimiento and 
                              c.fecha_vencimiento >= today and 
                              c.fecha_vencimiento <= today + timedelta(days=7)])
    cuentas_vencidas = len([c for c in cuentas if c.fecha_vencimiento and 
                           c.fecha_vencimiento < today])
    
    # Calcular valor total de las ventas
    valor_total_ventas = sum(c.precio for c in cuentas if c.estado == 'Vendida')
    
    return render_template('cuentas.html', 
                         cuentas=cuentas, 
                         plataformas_disponibles=plataformas_disponibles,
                         filtro_estado=estado,
                         filtro_plataforma=plataforma,
                         total_cuentas=total_cuentas,
                         cuentas_disponibles=cuentas_disponibles,
                         cuentas_vendidas=cuentas_vendidas,
                         cuentas_por_vencer=cuentas_por_vencer,
                         cuentas_vencidas=cuentas_vencidas,
                         valor_total_ventas=valor_total_ventas,
                         today=today)

@app.route('/nueva_cuenta', methods=['GET', 'POST'])
@login_required
def nueva_cuenta():
    """Agregar nueva cuenta"""
    if request.method == 'POST':
        plataforma = request.form.get('plataforma')
        if plataforma == 'Otro':
            plataforma = request.form.get('plataforma_otro')
        
        email = request.form.get('email')
        password = request.form.get('password')
        precio = float(request.form.get('precio', 0))
        fecha_compra = datetime.strptime(request.form.get('fecha_compra'), '%Y-%m-%d').date()
        notas = request.form.get('notas', '')
        
        # Permitir correos duplicados - múltiples cuentas pueden tener el mismo email
        
        nueva_cuenta = Cuenta(
            plataforma=plataforma,
            email=email,
            password=password,
            precio=precio,
            fecha_compra=fecha_compra,
            notas=notas,
            usuario_id=current_user.id
        )
        
        db.session.add(nueva_cuenta)
        db.session.commit()
        
        flash('Cuenta agregada correctamente', 'success')
        return redirect(url_for('cuentas'))
    
    return render_template('nueva_cuenta.html', today=datetime.now().strftime('%Y-%m-%d'))

@app.route('/editar_cuenta/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_cuenta(id):
    """Editar cuenta existente"""
    cuenta = Cuenta.query.get_or_404(id)
    
    # Verificar que el usuario pueda editar esta cuenta
    if not current_user.es_admin and cuenta.usuario_id != current_user.id:
        flash('No tienes permisos para editar esta cuenta', 'error')
        return redirect(url_for('cuentas'))
    
    if request.method == 'POST':
        plataforma = request.form.get('plataforma')
        if plataforma == 'Otro':
            plataforma = request.form.get('plataforma_otro')
        
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Permitir correos duplicados - múltiples cuentas pueden tener el mismo email
        
        cuenta.plataforma = plataforma
        cuenta.email = email
        cuenta.password = password
        cuenta.precio = float(request.form.get('precio', 0))
        cuenta.fecha_compra = datetime.strptime(request.form.get('fecha_compra'), '%Y-%m-%d').date()
        cuenta.notas = request.form.get('notas', '')
        
        db.session.commit()
        flash('Cuenta actualizada correctamente', 'success')
        return redirect(url_for('cuentas'))
    
    return render_template('editar_cuenta.html', cuenta=cuenta)

@app.route('/ver_cuenta/<int:id>')
@login_required
def ver_cuenta(id):
    """Ver detalles de una cuenta"""
    cuenta = Cuenta.query.get_or_404(id)
    
    # Verificar que el usuario pueda ver esta cuenta
    if not current_user.es_admin and cuenta.usuario_id != current_user.id:
        flash('No tienes permisos para ver esta cuenta', 'error')
        return redirect(url_for('cuentas'))
    
    return render_template('ver_cuenta.html', cuenta=cuenta)

@app.route('/vender_cuenta/<int:id>', methods=['POST'])
@login_required
def vender_cuenta(id):
    """Marcar cuenta como vendida"""
    cuenta = Cuenta.query.get_or_404(id)
    
    # Verificar que el usuario pueda vender esta cuenta
    if not current_user.es_admin and cuenta.usuario_id != current_user.id:
        flash('No tienes permisos para vender esta cuenta', 'error')
        return redirect(url_for('cuentas'))
    
    if cuenta.estado == 'Disponible':
        # Obtener datos del formulario
        nombre_comprador = request.form.get('nombre_comprador')
        whatsapp_comprador = request.form.get('whatsapp_comprador')
        fecha_vencimiento = request.form.get('fecha_vencimiento')
        
        if nombre_comprador and whatsapp_comprador:
            try:
                # Convertir fecha de vencimiento
                if fecha_vencimiento:
                    fecha_vencimiento = datetime.strptime(fecha_vencimiento, '%Y-%m-%d').date()
                
                # Actualizar cuenta
                cuenta.estado = 'Vendida'
                cuenta.fecha_venta = datetime.now()
                cuenta.nombre_comprador = nombre_comprador
                cuenta.whatsapp_comprador = whatsapp_comprador
                cuenta.fecha_vencimiento = fecha_vencimiento
                
                db.session.commit()
                
                flash('Cuenta marcada como vendida correctamente', 'success')
                return redirect(url_for('ver_cuenta', id=id))
                
            except Exception as e:
                db.session.rollback()
                flash(f'Error al vender la cuenta: {str(e)}', 'error')
                return redirect(url_for('ver_cuenta', id=id))
        else:
            flash('Debes completar todos los campos obligatorios', 'error')
            return redirect(url_for('ver_cuenta', id=id))
    else:
        flash('La cuenta no está disponible para la venta', 'error')
        return redirect(url_for('ver_cuenta', id=id))

def generar_mensaje_whatsapp(cuenta):
    """Genera el mensaje de WhatsApp con los datos de la cuenta vendida"""
    mensaje = f"""🎉 *¡Tu cuenta de {cuenta.plataforma} está lista!*

📱 *Plataforma:* {cuenta.plataforma}
📧 *Email:* {cuenta.email}
🔑 *Contraseña:* {cuenta.password}
🎬 *Plataforma:* {cuenta.plataforma}
📅 *Fecha de compra:* {cuenta.fecha_venta.strftime('%d/%m/%Y')}
⏰ *Vencimiento:* {cuenta.fecha_vencimiento.strftime('%d/%m/%Y')}

✅ *Estado:* Cuenta activa y funcional

⚠️ *Importante:* 
• Guarda estos datos en un lugar seguro
• No compartas la contraseña con nadie
• La cuenta vence el {cuenta.fecha_vencimiento.strftime('%d/%m/%Y')}

🆘 Si tienes algún problema, contáctanos.

¡Disfruta de tu cuenta! 🎬"""
    
    return mensaje

@app.route('/cuentas/<int:id>/renovar', methods=['POST'])
@login_required
def renovar_cuenta(id):
    """Renovar cuenta extendiendo la fecha de vencimiento por un mes"""
    cuenta = Cuenta.query.get_or_404(id)
    
    # Verificar que el usuario pueda renovar esta cuenta
    if not current_user.es_admin and cuenta.usuario_id != current_user.id:
        flash('No tienes permisos para renovar esta cuenta', 'error')
        return redirect(url_for('cuentas'))
    
    # Verificar que la cuenta tenga fecha de vencimiento
    if not cuenta.fecha_vencimiento:
        flash('Esta cuenta no tiene fecha de vencimiento configurada', 'warning')
        return redirect(url_for('cuentas'))
    
    try:
        # Calcular nueva fecha de vencimiento (un mes más)
        from dateutil.relativedelta import relativedelta
        
        nueva_fecha_vencimiento = cuenta.fecha_vencimiento + relativedelta(months=1)
        
        # Actualizar la cuenta
        cuenta.fecha_vencimiento = nueva_fecha_vencimiento
        
        db.session.commit()
        
        flash(f'Cuenta renovada exitosamente. Nueva fecha de vencimiento: {nueva_fecha_vencimiento.strftime("%d/%m/%Y")}', 'success')
        return redirect(url_for('cuentas'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al renovar la cuenta: {str(e)}', 'error')
        return redirect(url_for('cuentas'))

@app.route('/cuentas/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_cuenta(id):
    """Eliminar una cuenta (usuarios pueden eliminar sus propias cuentas, admins pueden eliminar todas)"""
    cuenta = Cuenta.query.get_or_404(id)
    
    # Verificar permisos: usuarios solo pueden eliminar sus propias cuentas
    if not current_user.es_admin and cuenta.usuario_id != current_user.id:
        flash('❌ No tienes permisos para eliminar esta cuenta', 'error')
        return redirect(url_for('cuentas'))
    
    try:
        db.session.delete(cuenta)
        db.session.commit()
        flash('🗑️ Cuenta eliminada exitosamente', 'success')
        return redirect(url_for('cuentas'))
    except Exception as e:
        flash(f'❌ Error al eliminar cuenta: {str(e)}', 'error')
        db.session.rollback()
        return redirect(url_for('cuentas'))

@app.route('/api/estadisticas')
@login_required
def api_estadisticas():
    """API para obtener estadísticas en formato JSON"""
    total_cuentas = Cuenta.query.count()
    cuentas_disponibles = Cuenta.query.filter_by(estado='Disponible').count()
    cuentas_vendidas = Cuenta.query.filter_by(estado='Vendida').count()
    # Valor total eliminado - ya no se usa el campo precio
    
    plataformas = db.session.query(
        Cuenta.plataforma, 
        db.func.count(Cuenta.id).label('cantidad')
    ).filter_by(estado='Disponible').group_by(Cuenta.plataforma).all()
    
    return jsonify({
        'total': total_cuentas,
        'disponibles': cuentas_disponibles,
        'vendidas': cuentas_vendidas,
        'valor_total': valor_total,
        'plataformas': [{'plataforma': p.plataforma, 'cantidad': p.cantidad} for p in plataformas]
    })

@app.route('/usuarios')
@login_required
def usuarios():
    """Lista de usuarios (solo para administradores)"""
    if not current_user.es_admin:
        flash('No tienes permisos para acceder a esta página', 'error')
        return redirect(url_for('index'))
    
    usuarios = Usuario.query.order_by(Usuario.fecha_creacion.desc()).all()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuarios/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_usuario():
    """Crear nuevo usuario (solo para administradores)"""
    if not current_user.es_admin:
        flash('No tienes permisos para acceder a esta página', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        es_admin = request.form.get('es_admin') == 'on'
        
        # Verificar que el username y email no existan
        if Usuario.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe', 'error')
            return render_template('nuevo_usuario.html')
        
        if Usuario.query.filter_by(email=email).first():
            flash('El email ya existe', 'error')
            return render_template('nuevo_usuario.html')
        
        nuevo_usuario = Usuario(
            username=username,
            email=email,
            es_admin=es_admin
        )
        nuevo_usuario.set_password(password)
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash('Usuario creado correctamente', 'success')
        return redirect(url_for('usuarios'))
    
    return render_template('nuevo_usuario.html')

@app.route('/usuarios/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    """Editar usuario existente (solo para administradores)"""
    if not current_user.es_admin:
        flash('No tienes permisos para acceder a esta página', 'error')
        return redirect(url_for('index'))
    
    usuario = Usuario.query.get_or_404(id)
    
    # No permitir editar el propio usuario admin
    if usuario.id == current_user.id:
        flash('No puedes editar tu propio usuario', 'error')
        return redirect(url_for('usuarios'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        es_admin = request.form.get('es_admin') == 'on'
        activo = request.form.get('activo') == 'on'
        
        # Verificar que el username y email no existan en otros usuarios
        usuario_existente = Usuario.query.filter(
            Usuario.username == username,
            Usuario.id != id
        ).first()
        if usuario_existente:
            flash('El nombre de usuario ya existe', 'error')
            return render_template('editar_usuario.html', usuario=usuario)
        
        usuario_existente = Usuario.query.filter(
            Usuario.email == email,
            Usuario.id != id
        ).first()
        if usuario_existente:
            flash('El email ya existe', 'error')
            return render_template('editar_usuario.html', usuario=usuario)
        
        usuario.username = username
        usuario.email = email
        usuario.es_admin = es_admin
        usuario.activo = activo
        
        # Cambiar contraseña si se proporciona
        nueva_password = request.form.get('nueva_password')
        if nueva_password:
            usuario.set_password(nueva_password)
        
        db.session.commit()
        flash('Usuario actualizado correctamente', 'success')
        return redirect(url_for('usuarios'))
    
    return render_template('editar_usuario.html', usuario=usuario)

@app.route('/usuarios/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_usuario(id):
    """Eliminar usuario (solo para administradores)"""
    print(f"DEBUG: Intento de eliminar usuario ID: {id}")
    print(f"DEBUG: Usuario actual: {current_user.username}, es_admin: {current_user.es_admin}")
    
    if not current_user.es_admin:
        print("DEBUG: Usuario no es administrador")
        flash('No tienes permisos para realizar esta acción', 'error')
        return redirect(url_for('index'))
    
    usuario = Usuario.query.get_or_404(id)
    print(f"DEBUG: Usuario encontrado: {usuario.username}")
    
    # No permitir eliminar el propio usuario
    if usuario.id == current_user.id:
        print("DEBUG: Intento de eliminar propio usuario")
        flash('No puedes eliminar tu propio usuario', 'error')
        return redirect(url_for('usuarios'))
    
    # Verificar si el usuario tiene cuentas
    if usuario.cuentas:
        print(f"DEBUG: Usuario tiene {len(usuario.cuentas)} cuentas asociadas")
        flash('No se puede eliminar un usuario que tiene cuentas asociadas', 'error')
        return redirect(url_for('usuarios'))
    
    try:
        db.session.delete(usuario)
        db.session.commit()
        print(f"DEBUG: Usuario {usuario.username} eliminado exitosamente")
        flash('Usuario eliminado correctamente', 'success')
    except Exception as e:
        print(f"DEBUG: Error al eliminar usuario: {str(e)}")
        db.session.rollback()
        flash('Error al eliminar el usuario', 'error')
    
    return redirect(url_for('usuarios'))

@app.route('/test_eliminacion')
def test_eliminacion():
    """Página de prueba para verificar eliminación de usuarios"""
    return render_template('test_eliminacion.html')

@app.route('/apk')
@login_required
def apk():
    """Página para crear APK de la aplicación"""
    return render_template('apk.html')

@app.route('/api/cuentas')
@login_required
def api_cuentas():
    """API para obtener cuentas en formato JSON"""
    estado = request.args.get('estado', '')
    plataforma = request.args.get('plataforma', '')
    
    query = Cuenta.query
    
    if estado:
        query = query.filter_by(estado=estado)
    if plataforma:
        query = query.filter_by(plataforma=plataforma)
    
    cuentas = query.order_by(Cuenta.fecha_creacion.desc()).all()
    return jsonify([cuenta.to_dict() for cuenta in cuentas])

@app.route('/api/cuenta/<int:id>/mensaje-whatsapp')
@login_required
def api_mensaje_whatsapp(id):
    """API para obtener el mensaje de WhatsApp de una cuenta vendida"""
    if not current_user.es_admin:
        return jsonify({'error': 'No tienes permisos para acceder a esta información'}), 403
    
    cuenta = Cuenta.query.get_or_404(id)
    
    if cuenta.estado != 'Vendida':
        return jsonify({'error': 'La cuenta no ha sido vendida'}), 400
    
    mensaje = generar_mensaje_whatsapp(cuenta)
    return jsonify({
        'mensaje': mensaje,
        'whatsapp': cuenta.whatsapp_comprador,
        'nombre_comprador': cuenta.nombre_comprador
    })

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_interno(error):
    return render_template('500.html'), 500

@app.route('/exportar_cuentas_vendidas')
@login_required
def exportar_cuentas_vendidas():
    """Exportar cuentas vendidas a archivo de texto"""
    from flask import send_file
    import io
    from datetime import datetime
    
    # Obtener cuentas vendidas
    if current_user.es_admin:
        # Administrador ve todas las cuentas vendidas
        cuentas_vendidas = Cuenta.query.filter_by(estado='Vendida').order_by(Cuenta.fecha_venta.desc()).all()
    else:
        # Usuario normal solo ve sus propias cuentas vendidas
        cuentas_vendidas = Cuenta.query.filter_by(estado='Vendida', usuario_id=current_user.id).order_by(Cuenta.fecha_venta.desc()).all()
    
    if not cuentas_vendidas:
        flash('No hay cuentas vendidas para exportar', 'warning')
        return redirect(url_for('cuentas'))
    
    # Crear archivo de texto en memoria
    output = io.StringIO()
    
    # Escribir encabezado del archivo
    output.write("=" * 80 + "\n")
    output.write("REPORTE DE CUENTAS VENDIDAS\n")
    output.write("=" * 80 + "\n")
    output.write(f"Fecha de exportación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    output.write(f"Total de cuentas vendidas: {len(cuentas_vendidas)}\n")
    output.write("=" * 80 + "\n\n")
    
    # Escribir datos de cada cuenta
    for i, cuenta in enumerate(cuentas_vendidas, 1):
        output.write(f"CUENTA #{i}\n")
        output.write("-" * 40 + "\n")
        output.write(f"ID: {cuenta.id}\n")
        output.write(f"Plataforma: {cuenta.plataforma}\n")
        output.write(f"Email: {cuenta.email}\n")
        output.write(f"Contraseña: {cuenta.password}\n")
        output.write(f"Precio: ${cuenta.precio:.2f}\n")
        output.write(f"Fecha de Compra: {cuenta.fecha_compra.strftime('%d/%m/%Y') if cuenta.fecha_compra else 'N/A'}\n")
        output.write(f"Fecha de Venta: {cuenta.fecha_venta.strftime('%d/%m/%Y %H:%M') if cuenta.fecha_venta else 'N/A'}\n")
        output.write(f"Nombre del Comprador: {cuenta.nombre_comprador or 'N/A'}\n")
        output.write(f"WhatsApp del Comprador: {cuenta.whatsapp_comprador or 'N/A'}\n")
        output.write(f"Fecha de Vencimiento: {cuenta.fecha_vencimiento.strftime('%d/%m/%Y') if cuenta.fecha_vencimiento else 'N/A'}\n")
        if cuenta.notas:
            output.write(f"Notas: {cuenta.notas}\n")
        output.write("\n" + "=" * 80 + "\n\n")
    
    # Escribir resumen final
    output.write("RESUMEN FINAL\n")
    output.write("-" * 40 + "\n")
    output.write(f"Total de cuentas exportadas: {len(cuentas_vendidas)}\n")
    output.write(f"Valor total de ventas: ${sum(c.precio for c in cuentas_vendidas):.2f}\n")
    output.write(f"Fecha de exportación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    output.write("=" * 80 + "\n")
    
    # Preparar respuesta
    output.seek(0)
    
    # Generar nombre de archivo con fecha
    fecha_actual = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'cuentas_vendidas_{fecha_actual}.txt'
    
    # Crear respuesta con archivo de texto
    response = send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/plain',
        as_attachment=True,
        download_name=filename
    )
    
    # Agregar headers para evitar problemas de caché
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response

@app.route('/exportar_cuentas_disponibles')
@login_required
def exportar_cuentas_disponibles():
    """Exportar cuentas disponibles a archivo de texto"""
    from flask import send_file
    import io
    from datetime import datetime
    
    # Obtener cuentas disponibles
    if current_user.es_admin:
        # Administrador ve todas las cuentas disponibles
        cuentas_disponibles = Cuenta.query.filter_by(estado='Disponible').order_by(Cuenta.fecha_creacion.desc()).all()
    else:
        # Usuario normal solo ve sus propias cuentas disponibles
        cuentas_disponibles = Cuenta.query.filter_by(estado='Disponible', usuario_id=current_user.id).order_by(Cuenta.fecha_creacion.desc()).all()
    
    if not cuentas_disponibles:
        flash('No hay cuentas disponibles para exportar', 'warning')
        return redirect(url_for('cuentas'))
    
    # Crear archivo de texto en memoria
    output = io.StringIO()
    
    # Escribir encabezado del archivo
    output.write("=" * 80 + "\n")
    output.write("REPORTE DE CUENTAS DISPONIBLES\n")
    output.write("=" * 80 + "\n")
    output.write(f"Fecha de exportación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    output.write(f"Total de cuentas disponibles: {len(cuentas_disponibles)}\n")
    output.write("=" * 80 + "\n\n")
    
    # Escribir datos de cada cuenta
    for i, cuenta in enumerate(cuentas_disponibles, 1):
        output.write(f"CUENTA #{i}\n")
        output.write("-" * 40 + "\n")
        output.write(f"ID: {cuenta.id}\n")
        output.write(f"Plataforma: {cuenta.plataforma}\n")
        output.write(f"Email: {cuenta.email}\n")
        output.write(f"Contraseña: {cuenta.password}\n")
        output.write(f"Precio: ${cuenta.precio:.2f}\n")
        output.write(f"Fecha de Compra: {cuenta.fecha_compra.strftime('%d/%m/%Y') if cuenta.fecha_compra else 'N/A'}\n")
        output.write(f"Fecha de Creación: {cuenta.fecha_creacion.strftime('%d/%m/%Y %H:%M:%S') if cuenta.fecha_creacion else 'N/A'}\n")
        if cuenta.fecha_vencimiento:
            output.write(f"Fecha de Vencimiento: {cuenta.fecha_vencimiento.strftime('%d/%m/%Y')}\n")
            # Calcular días restantes
            dias_restantes = (cuenta.fecha_vencimiento - datetime.now().date()).days
            if dias_restantes > 0:
                output.write(f"Días Restantes: {dias_restantes} día{'s' if dias_restantes != 1 else ''}\n")
            elif dias_restantes == 0:
                output.write("Días Restantes: VENCE HOY ⚠️\n")
            else:
                output.write(f"Días Restantes: VENCIDA hace {abs(dias_restantes)} día{'s' if abs(dias_restantes) != 1 else ''} ❌\n")
        if cuenta.notas:
            output.write(f"Notas: {cuenta.notas}\n")
        output.write("\n" + "=" * 80 + "\n\n")
    
    # Escribir resumen final
    output.write("RESUMEN FINAL\n")
    output.write("-" * 40 + "\n")
    output.write(f"Total de cuentas exportadas: {len(cuentas_disponibles)}\n")
    output.write(f"Valor total del inventario: ${sum(c.precio for c in cuentas_disponibles):.2f}\n")
    output.write(f"Fecha de exportación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    output.write("=" * 80 + "\n")
    
    # Preparar respuesta
    output.seek(0)
    
    # Generar nombre de archivo con fecha
    fecha_actual = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'cuentas_disponibles_{fecha_actual}.txt'
    
    # Crear respuesta con archivo de texto
    response = send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/plain',
        as_attachment=True,
        download_name=filename
    )
    
    # Agregar headers para evitar problemas de caché
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response

@app.route('/exportar_usuarios')
@login_required
def exportar_usuarios():
    """Exportar usuarios a archivo de texto (solo para administradores)"""
    from flask import send_file
    import io
    from datetime import datetime
    
    # Verificar que solo los administradores puedan exportar usuarios
    if not current_user.es_admin:
        flash('No tienes permisos para acceder a esta función', 'error')
        return redirect(url_for('index'))
    
    # Obtener todos los usuarios
    usuarios = Usuario.query.order_by(Usuario.fecha_creacion.desc()).all()
    
    if not usuarios:
        flash('No hay usuarios para exportar', 'warning')
        return redirect(url_for('usuarios'))
    
    # Crear archivo de texto en memoria
    output = io.StringIO()
    
    # Escribir encabezado del archivo
    output.write("=" * 80 + "\n")
    output.write("REPORTE DE USUARIOS DEL SISTEMA\n")
    output.write("=" * 80 + "\n")
    output.write(f"Fecha de exportación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    output.write(f"Total de usuarios: {len(usuarios)}\n")
    output.write(f"Exportado por: {current_user.username} (Administrador)\n")
    output.write("=" * 80 + "\n\n")
    
    # Escribir datos de cada usuario
    for i, usuario in enumerate(usuarios, 1):
        output.write(f"USUARIO #{i}\n")
        output.write("-" * 40 + "\n")
        output.write(f"ID: {usuario.id}\n")
        output.write(f"Nombre de Usuario: {usuario.username}\n")
        output.write(f"Email: {usuario.email}\n")
        output.write(f"Tipo de Usuario: {'Administrador' if usuario.es_admin else 'Usuario Normal'}\n")
        output.write(f"Estado: {'Activo' if usuario.activo else 'Inactivo'}\n")
        output.write(f"Fecha de Creación: {usuario.fecha_creacion.strftime('%d/%m/%Y %H:%M:%S')}\n")
        
        # Contar cuentas del usuario
        total_cuentas = len(usuario.cuentas)
        cuentas_disponibles = len([c for c in usuario.cuentas if c.estado == 'Disponible'])
        cuentas_vendidas = len([c for c in usuario.cuentas if c.estado == 'Vendida'])
        
        output.write(f"Total de Cuentas: {total_cuentas}\n")
        output.write(f"  - Disponibles: {cuentas_disponibles}\n")
        output.write(f"  - Vendidas: {cuentas_vendidas}\n")
        
        # Calcular valor del inventario del usuario
        valor_inventario = sum(c.precio for c in usuario.cuentas if c.estado == 'Disponible')
        valor_ventas = sum(c.precio for c in usuario.cuentas if c.estado == 'Vendida')
        
        output.write(f"Valor del Inventario: ${valor_inventario:.2f}\n")
        output.write(f"Valor Total de Ventas: ${valor_ventas:.2f}\n")
        
        # Información adicional
        if usuario.id == current_user.id:
            output.write("NOTA: Este es tu usuario actual\n")
        
        output.write("\n" + "=" * 80 + "\n\n")
    
    # Escribir resumen final
    output.write("RESUMEN FINAL DEL SISTEMA\n")
    output.write("-" * 40 + "\n")
    output.write(f"Total de usuarios exportados: {len(usuarios)}\n")
    
    # Estadísticas generales
    total_cuentas_sistema = sum(len(u.cuentas) for u in usuarios)
    total_cuentas_disponibles = sum(len([c for c in u.cuentas if c.estado == 'Disponible']) for u in usuarios)
    total_cuentas_vendidas = sum(len([c for c in u.cuentas if c.estado == 'Vendida']) for u in usuarios)
    valor_total_inventario = sum(sum(c.precio for c in u.cuentas if c.estado == 'Disponible') for u in usuarios)
    valor_total_ventas = sum(sum(c.precio for c in u.cuentas if c.estado == 'Vendida') for u in usuarios)
    
    output.write(f"Total de cuentas en el sistema: {total_cuentas_sistema}\n")
    output.write(f"Total de cuentas disponibles: {total_cuentas_disponibles}\n")
    output.write(f"Total de cuentas vendidas: {total_cuentas_vendidas}\n")
    output.write(f"Valor total del inventario: ${valor_total_inventario:.2f}\n")
    output.write(f"Valor total de ventas: ${valor_total_ventas:.2f}\n")
    output.write(f"Fecha de exportación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    output.write("=" * 80 + "\n")
    
    # Preparar respuesta
    output.seek(0)
    
    # Generar nombre de archivo con fecha
    fecha_actual = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'usuarios_sistema_{fecha_actual}.txt'
    
    # Crear respuesta con archivo de texto
    response = send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/plain',
        as_attachment=True,
        download_name=filename
    )
    
    # Agregar headers para evitar problemas de caché
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response

@app.route('/importar_cuentas_vendidas', methods=['GET', 'POST'])
@login_required
def importar_cuentas_vendidas():
    """Importar cuentas vendidas desde archivo de texto"""
    if request.method == 'POST':
        if 'archivo' not in request.files:
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(request.url)
        
        archivo = request.files['archivo']
        if archivo.filename == '':
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(request.url)
        
        if not archivo.filename.endswith('.txt'):
            flash('El archivo debe ser de tipo .txt', 'error')
            return redirect(request.url)
        
        try:
            contenido = archivo.read().decode('utf-8')
            cuentas_importadas = 0
            cuentas_duplicadas = 0
            errores = []
            
            # Procesar el archivo línea por línea
            lineas = contenido.split('\n')
            cuenta_actual = {}
            
            for linea in lineas:
                linea = linea.strip()
                
                if linea.startswith('CUENTA #'):
                    # Nueva cuenta, guardar la anterior si existe
                    if cuenta_actual and 'email' in cuenta_actual:
                        resultado = procesar_cuenta_vendida_importada(cuenta_actual, current_user.id)
                        if resultado['exito']:
                            cuentas_importadas += 1
                        elif resultado['duplicado']:
                            cuentas_duplicadas += 1
                        else:
                            errores.append(resultado['error'])
                    
                    # Iniciar nueva cuenta
                    cuenta_actual = {}
                    
                elif ':' in linea:
                    clave, valor = linea.split(':', 1)
                    clave = clave.strip()
                    valor = valor.strip()
                    
                    if clave == 'Plataforma':
                        cuenta_actual['plataforma'] = valor
                    elif clave == 'Email':
                        cuenta_actual['email'] = valor
                    elif clave == 'Contraseña':
                        cuenta_actual['password'] = valor
                    elif clave == 'Precio':
                        # Extraer solo el número del precio
                        try:
                            precio_str = valor.replace('$', '').replace(',', '').strip()
                            cuenta_actual['precio'] = float(precio_str)
                        except ValueError:
                            cuenta_actual['precio'] = 0.0
                    elif clave == 'Fecha de Compra':
                        try:
                            if valor != 'N/A':
                                # Convertir formato dd/mm/yyyy a yyyy-mm-dd
                                if '/' in valor:
                                    dia, mes, anio = valor.split('/')
                                    cuenta_actual['fecha_compra'] = f"{anio}-{mes.zfill(2)}-{dia.zfill(2)}"
                                else:
                                    cuenta_actual['fecha_compra'] = valor
                        except:
                            cuenta_actual['fecha_compra'] = None
                    elif clave == 'Fecha de Venta':
                        try:
                            if valor != 'N/A':
                                # Convertir formato dd/mm/yyyy HH:MM a datetime
                                if '/' in valor and ':' in valor:
                                    fecha_partes = valor.split(' ')
                                    fecha = fecha_partes[0]
                                    hora = fecha_partes[1] if len(fecha_partes) > 1 else '00:00'
                                    dia, mes, anio = fecha.split('/')
                                    cuenta_actual['fecha_venta'] = f"{anio}-{mes.zfill(2)}-{dia.zfill(2)} {hora}"
                                else:
                                    cuenta_actual['fecha_venta'] = valor
                        except:
                            cuenta_actual['fecha_venta'] = None
                    elif clave == 'Nombre del Comprador':
                        cuenta_actual['nombre_comprador'] = valor if valor != 'N/A' else None
                    elif clave == 'WhatsApp del Comprador':
                        cuenta_actual['whatsapp_comprador'] = valor if valor != 'N/A' else None
                    elif clave == 'Fecha de Vencimiento':
                        try:
                            if valor != 'N/A':
                                if '/' in valor:
                                    dia, mes, anio = valor.split('/')
                                    cuenta_actual['fecha_vencimiento'] = f"{anio}-{mes.zfill(2)}-{dia.zfill(2)}"
                                else:
                                    cuenta_actual['fecha_vencimiento'] = valor
                        except:
                            cuenta_actual['fecha_vencimiento'] = None
                    elif clave == 'Notas':
                        cuenta_actual['notas'] = valor if valor != 'N/A' else None
            
            # Procesar la última cuenta
            if cuenta_actual and 'email' in cuenta_actual:
                resultado = procesar_cuenta_vendida_importada(cuenta_actual, current_user.id)
                if resultado['exito']:
                    cuentas_importadas += 1
                elif resultado['duplicado']:
                    cuentas_duplicadas += 1
                else:
                    errores.append(resultado['error'])
            
            # Mensaje de resultado
            mensaje = f"Importación completada: {cuentas_importadas} cuentas importadas"
            if cuentas_duplicadas > 0:
                mensaje += f", {cuentas_duplicadas} duplicadas"
            if errores:
                mensaje += f", {len(errores)} errores"
            
            if cuentas_importadas > 0:
                flash(mensaje, 'success')
            elif cuentas_duplicadas > 0:
                flash(mensaje, 'warning')
            else:
                flash(mensaje, 'error')
            
            return redirect(url_for('cuentas'))
            
        except Exception as e:
            flash(f'Error al procesar el archivo: {str(e)}', 'error')
            return redirect(request.url)
    
    return render_template('importar_cuentas_vendidas.html')

@app.route('/importar_cuentas_disponibles', methods=['GET', 'POST'])
@login_required
def importar_cuentas_disponibles():
    """Importar cuentas disponibles desde archivo de texto"""
    if request.method == 'POST':
        if 'archivo' not in request.files:
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(request.url)
        
        archivo = request.files['archivo']
        if archivo.filename == '':
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(request.url)
        
        if not archivo.filename.endswith('.txt'):
            flash('El archivo debe ser de tipo .txt', 'error')
            return redirect(request.url)
        
        try:
            contenido = archivo.read().decode('utf-8')
            cuentas_importadas = 0
            cuentas_duplicadas = 0
            errores = []
            
            # Procesar el archivo línea por línea
            lineas = contenido.split('\n')
            cuenta_actual = {}
            
            for linea in lineas:
                linea = linea.strip()
                
                if linea.startswith('CUENTA #'):
                    # Nueva cuenta, guardar la anterior si existe
                    if cuenta_actual and 'email' in cuenta_actual:
                        resultado = procesar_cuenta_disponible_importada(cuenta_actual, current_user.id)
                        if resultado['exito']:
                            cuentas_importadas += 1
                        elif resultado['duplicado']:
                            cuentas_duplicadas += 1
                        else:
                            errores.append(resultado['error'])
                    
                    # Iniciar nueva cuenta
                    cuenta_actual = {}
                    
                elif ':' in linea:
                    clave, valor = linea.split(':', 1)
                    clave = clave.strip()
                    valor = valor.strip()
                    
                    if clave == 'Plataforma':
                        cuenta_actual['plataforma'] = valor
                    elif clave == 'Email':
                        cuenta_actual['email'] = valor
                    elif clave == 'Contraseña':
                        cuenta_actual['password'] = valor
                    elif clave == 'Precio':
                        # Extraer solo el número del precio
                        try:
                            precio_str = valor.replace('$', '').replace(',', '').strip()
                            cuenta_actual['precio'] = float(precio_str)
                        except ValueError:
                            cuenta_actual['precio'] = 0.0
                    elif clave == 'Fecha de Compra':
                        try:
                            if valor != 'N/A':
                                # Convertir formato dd/mm/yyyy a yyyy-mm-dd
                                if '/' in valor:
                                    dia, mes, anio = valor.split('/')
                                    cuenta_actual['fecha_compra'] = f"{anio}-{mes.zfill(2)}-{dia.zfill(2)}"
                                else:
                                    cuenta_actual['fecha_compra'] = valor
                        except:
                            cuenta_actual['fecha_compra'] = None
                    elif clave == 'Fecha de Vencimiento':
                        try:
                            if valor != 'N/A':
                                if '/' in valor:
                                    dia, mes, anio = valor.split('/')
                                    cuenta_actual['fecha_vencimiento'] = f"{anio}-{mes.zfill(2)}-{dia.zfill(2)}"
                                else:
                                    cuenta_actual['fecha_vencimiento'] = valor
                        except:
                            cuenta_actual['fecha_vencimiento'] = None
                    elif clave == 'Notas':
                        cuenta_actual['notas'] = valor if valor != 'N/A' else None
            
            # Procesar la última cuenta
            if cuenta_actual and 'email' in cuenta_actual:
                resultado = procesar_cuenta_disponible_importada(cuenta_actual, current_user.id)
                if resultado['exito']:
                    cuentas_importadas += 1
                elif resultado['duplicado']:
                    cuentas_duplicadas += 1
                else:
                    errores.append(resultado['error'])
            
            # Mensaje de resultado
            mensaje = f"Importación completada: {cuentas_importadas} cuentas importadas"
            if cuentas_duplicadas > 0:
                mensaje += f", {cuentas_duplicadas} duplicadas"
            if errores:
                mensaje += f", {len(errores)} errores"
            
            if cuentas_importadas > 0:
                flash(mensaje, 'success')
            elif cuentas_duplicadas > 0:
                flash(mensaje, 'warning')
            else:
                flash(mensaje, 'error')
            
            return redirect(url_for('cuentas'))
            
        except Exception as e:
            flash(f'Error al procesar el archivo: {str(e)}', 'error')
            return redirect(request.url)
    
    return render_template('importar_cuentas_disponibles.html')

def procesar_cuenta_vendida_importada(datos_cuenta, usuario_id):
    """Procesar una cuenta vendida importada"""
    try:
        # Verificar si la cuenta ya existe (por email)
        cuenta_existente = Cuenta.query.filter_by(
            email=datos_cuenta['email'],
            usuario_id=usuario_id
        ).first()
        
        if cuenta_existente:
            return {'exito': False, 'duplicado': True, 'error': f"Cuenta con email {datos_cuenta['email']} ya existe"}
        
        # Crear nueva cuenta
        nueva_cuenta = Cuenta(
            plataforma=datos_cuenta.get('plataforma', 'Desconocida'),
            email=datos_cuenta['email'],
            password=datos_cuenta.get('password', ''),
            precio=datos_cuenta.get('precio', 0.0),
            estado='Vendida',
            usuario_id=usuario_id,
            notas=datos_cuenta.get('notas')
        )
        
        # Procesar fechas
        if datos_cuenta.get('fecha_compra'):
            try:
                nueva_cuenta.fecha_compra = datetime.strptime(datos_cuenta['fecha_compra'], '%Y-%m-%d').date()
            except:
                nueva_cuenta.fecha_compra = datetime.now().date()
        
        if datos_cuenta.get('fecha_venta'):
            try:
                nueva_cuenta.fecha_venta = datetime.strptime(datos_cuenta['fecha_venta'], '%Y-%m-%d %H:%M')
            except:
                nueva_cuenta.fecha_venta = datetime.now()
        
        if datos_cuenta.get('fecha_vencimiento'):
            try:
                nueva_cuenta.fecha_vencimiento = datetime.strptime(datos_cuenta['fecha_vencimiento'], '%Y-%m-%d').date()
            except:
                pass
        
        # Datos de venta
        nueva_cuenta.nombre_comprador = datos_cuenta.get('nombre_comprador')
        nueva_cuenta.whatsapp_comprador = datos_cuenta.get('whatsapp_comprador')
        
        db.session.add(nueva_cuenta)
        db.session.commit()
        
        return {'exito': True, 'duplicado': False, 'error': None}
        
    except Exception as e:
        db.session.rollback()
        return {'exito': False, 'duplicado': False, 'error': str(e)}

def procesar_cuenta_disponible_importada(datos_cuenta, usuario_id):
    """Procesar una cuenta disponible importada"""
    try:
        # Verificar si la cuenta ya existe (por email)
        cuenta_existente = Cuenta.query.filter_by(
            email=datos_cuenta['email'],
            usuario_id=usuario_id
        ).first()
        
        if cuenta_existente:
            return {'exito': False, 'duplicado': True, 'error': f"Cuenta con email {datos_cuenta['email']} ya existe"}
        
        # Crear nueva cuenta
        nueva_cuenta = Cuenta(
            plataforma=datos_cuenta.get('plataforma', 'Desconocida'),
            email=datos_cuenta['email'],
            password=datos_cuenta.get('password', ''),
            precio=datos_cuenta.get('precio', 0.0),
            estado='Disponible',
            usuario_id=usuario_id,
            notas=datos_cuenta.get('notas')
        )
        
        # Procesar fechas
        if datos_cuenta.get('fecha_compra'):
            try:
                nueva_cuenta.fecha_compra = datetime.strptime(datos_cuenta['fecha_compra'], '%Y-%m-%d').date()
            except:
                nueva_cuenta.fecha_compra = datetime.now().date()
        
        if datos_cuenta.get('fecha_vencimiento'):
            try:
                nueva_cuenta.fecha_vencimiento = datetime.strptime(datos_cuenta['fecha_vencimiento'], '%Y-%m-%d').date()
            except:
                pass
        
        db.session.add(nueva_cuenta)
        db.session.commit()
        
        return {'exito': True, 'duplicado': False, 'error': None}
        
    except Exception as e:
        db.session.rollback()
        return {'exito': False, 'duplicado': False, 'error': str(e)}

@app.route('/importar_usuarios', methods=['GET', 'POST'])
@login_required
def importar_usuarios():
    """Importar usuarios desde archivo de texto (solo para administradores)"""
    # Verificar que solo los administradores puedan importar usuarios
    if not current_user.es_admin:
        flash('No tienes permisos para acceder a esta función', 'error')
        return redirect(url_for('usuarios'))
    
    if request.method == 'POST':
        if 'archivo' not in request.files:
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(request.url)
        
        archivo = request.files['archivo']
        if archivo.filename == '':
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(request.url)
        
        if not archivo.filename.endswith('.txt'):
            flash('El archivo debe ser de tipo .txt', 'error')
            return redirect(request.url)
        
        try:
            contenido = archivo.read().decode('utf-8')
            usuarios_importados = 0
            usuarios_duplicados = 0
            errores = []
            
            # Procesar el archivo línea por línea
            lineas = contenido.split('\n')
            usuario_actual = {}
            
            for linea in lineas:
                linea = linea.strip()
                
                if linea.startswith('USUARIO #'):
                    # Nuevo usuario, guardar el anterior si existe
                    if usuario_actual and 'username' in usuario_actual:
                        resultado = procesar_usuario_importado(usuario_actual)
                        if resultado['exito']:
                            usuarios_importados += 1
                        elif resultado['duplicado']:
                            usuarios_duplicados += 1
                        else:
                            errores.append(resultado['error'])
                    
                    # Iniciar nuevo usuario
                    usuario_actual = {}
                    
                elif ':' in linea:
                    clave, valor = linea.split(':', 1)
                    clave = clave.strip()
                    valor = valor.strip()
                    
                    if clave == 'Nombre de Usuario':
                        usuario_actual['username'] = valor
                    elif clave == 'Email':
                        usuario_actual['email'] = valor
                    elif clave == 'Tipo de Usuario':
                        usuario_actual['es_admin'] = valor == 'Administrador'
                    elif clave == 'Estado':
                        usuario_actual['activo'] = valor == 'Activo'
                    elif clave == 'Fecha de Creación':
                        try:
                            if valor != 'N/A':
                                # Convertir formato dd/mm/yyyy HH:MM:SS a datetime
                                if '/' in valor and ':' in valor:
                                    fecha_partes = valor.split(' ')
                                    fecha = fecha_partes[0]
                                    hora = fecha_partes[1] if len(fecha_partes) > 1 else '00:00:00'
                                    dia, mes, anio = fecha.split('/')
                                    usuario_actual['fecha_creacion'] = f"{anio}-{mes.zfill(2)}-{dia.zfill(2)} {hora}"
                                else:
                                    usuario_actual['fecha_creacion'] = valor
                        except:
                            usuario_actual['fecha_creacion'] = None
            
            # Procesar el último usuario
            if usuario_actual and 'username' in usuario_actual:
                resultado = procesar_usuario_importado(usuario_actual)
                if resultado['exito']:
                    usuarios_importados += 1
                elif resultado['duplicado']:
                    usuarios_duplicados += 1
                else:
                    errores.append(resultado['error'])
            
            # Mensaje de resultado
            mensaje = f"Importación completada: {usuarios_importados} usuarios importados"
            if usuarios_duplicados > 0:
                mensaje += f", {usuarios_duplicados} duplicados"
            if errores:
                mensaje += f", {len(errores)} errores"
            
            if usuarios_importados > 0:
                flash(mensaje, 'success')
            elif usuarios_duplicados > 0:
                flash(mensaje, 'warning')
            else:
                flash(mensaje, 'error')
            
            return redirect(url_for('usuarios'))
            
        except Exception as e:
            flash(f'Error al procesar el archivo: {str(e)}', 'error')
            return redirect(request.url)
    
    return redirect(url_for('usuarios'))

def procesar_usuario_importado(datos_usuario):
    """Procesar un usuario importado"""
    try:
        # Verificar si el usuario ya existe (por username o email)
        usuario_existente = Usuario.query.filter(
            (Usuario.username == datos_usuario['username']) |
            (Usuario.email == datos_usuario['email'])
        ).first()
        
        if usuario_existente:
            return {'exito': False, 'duplicado': True, 'error': f"Usuario con username {datos_usuario['username']} o email {datos_usuario['email']} ya existe"}
        
        # Crear nuevo usuario
        nuevo_usuario = Usuario(
            username=datos_usuario['username'],
            email=datos_usuario['email'],
            es_admin=datos_usuario.get('es_admin', False),
            activo=datos_usuario.get('activo', True)
        )
        
        # Establecer contraseña por defecto
        nuevo_usuario.set_password('password123')
        
        # Procesar fecha de creación
        if datos_usuario.get('fecha_creacion'):
            try:
                nuevo_usuario.fecha_creacion = datetime.strptime(datos_usuario['fecha_creacion'], '%Y-%m-%d %H:%M:%S')
            except:
                nuevo_usuario.fecha_creacion = datetime.now()
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return {'exito': True, 'duplicado': False, 'error': None}
        
    except Exception as e:
        db.session.rollback()
        return {'exito': False, 'duplicado': False, 'error': str(e)}

def crear_admin_inicial():
    """Crear usuario administrador inicial si no existe"""
    admin = Usuario.query.filter_by(es_admin=True).first()
    if not admin:
        admin = Usuario(
            username='admin',
            email='admin@gestor.com',
            es_admin=True,
            activo=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuario administrador creado:")
        print("   Usuario: admin")
        print("   Contraseña: admin123")
        print("   ⚠️  IMPORTANTE: Cambia la contraseña después del primer inicio de sesión")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        crear_admin_inicial()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    # Configuración para producción (InfinityFree)
    with app.app_context():
        db.create_all()
        crear_admin_inicial()
