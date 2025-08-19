#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestor de Cuentas de Streaming - Aplicación Web para Heroku
Sistema web para gestionar inventario de cuentas de streaming desde cualquier dispositivo
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)

# Configuración para Heroku
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tu_clave_secreta_aqui_2024_heroku')

# Base de datos PostgreSQL para Heroku
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL or 'sqlite:///cuentas_streaming.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    es_admin = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Cuenta(db.Model):
    """Modelo de la base de datos para las cuentas"""
    id = db.Column(db.Integer, primary_key=True)
    plataforma = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    estado = db.Column(db.String(20), default='disponible')
    precio = db.Column(db.Float, nullable=False)
    fecha_compra = db.Column(db.Date, nullable=False)
    fecha_venta = db.Column(db.Date)
    notas = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convertir objeto a diccionario para JSON"""
        return {
            'id': self.id,
            'plataforma': self.plataforma,
            'email': self.email,
            'password': self.password,
            'estado': self.estado,
            'precio': self.precio,
            'fecha_compra': self.fecha_compra.strftime('%Y-%m-%d') if self.fecha_compra else None,
            'fecha_venta': self.fecha_venta.strftime('%Y-%m-%d') if self.fecha_venta else None,
            'notas': self.notas,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }

@app.route('/')
def index():
    """Página principal"""
    if current_user.is_authenticated:
        return redirect(url_for('cuentas'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = Usuario.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('index')
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(next_page)
        else:
            flash('Usuario o contraseña incorrectos. Inténtalo de nuevo.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('login'))

@app.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    """Página de perfil del usuario"""
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not current_user.check_password(current_password):
            flash('❌ Contraseña actual incorrecta', 'error')
        elif new_password != confirm_password:
            flash('❌ Las contraseñas nuevas no coinciden', 'error')
        elif len(new_password) < 6:
            flash('❌ La contraseña debe tener al menos 6 caracteres', 'error')
        else:
            current_user.set_password(new_password)
            db.session.commit()
            flash('✅ Contraseña actualizada exitosamente', 'success')
            return redirect(url_for('perfil'))
    
    return render_template('perfil.html')

@app.route('/cuentas')
@login_required
def cuentas():
    """Listar todas las cuentas"""
    estado = request.args.get('estado', '')
    plataforma = request.args.get('plataforma', '')
    
    query = Cuenta.query
    
    if estado:
        query = query.filter_by(estado=estado)
    if plataforma:
        query = query.filter_by(plataforma=plataforma)
    
    cuentas = query.order_by(Cuenta.fecha_compra.desc()).all()
    return render_template('cuentas.html', cuentas=cuentas)

@app.route('/cuenta/nueva', methods=['GET', 'POST'])
@login_required
def nueva_cuenta():
    """Crear nueva cuenta"""
    if request.method == 'POST':
        plataforma = request.form.get('plataforma')
        email = request.form.get('email')
        password = request.form.get('password')
        precio = float(request.form.get('precio', 0))
        fecha_compra = datetime.strptime(request.form.get('fecha_compra'), '%Y-%m-%d').date()
        notas = request.form.get('notas', '')
        
        if not all([plataforma, email, password, precio, fecha_compra]):
            flash('❌ Todos los campos obligatorios deben estar completos', 'error')
            return render_template('nueva_cuenta.html')
        
        nueva_cuenta = Cuenta(
            plataforma=plataforma,
            email=email,
            password=password,
            precio=precio,
            fecha_compra=fecha_compra,
            notas=notas
        )
        
        try:
            db.session.add(nueva_cuenta)
            db.session.commit()
            flash('✅ Cuenta creada exitosamente', 'success')
            return redirect(url_for('cuentas'))
        except Exception as e:
            flash(f'❌ Error al crear cuenta: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('nueva_cuenta.html')

@app.route('/cuenta/<int:id>')
@login_required
def ver_cuenta(id):
    """Ver detalles de una cuenta"""
    cuenta = Cuenta.query.get_or_404(id)
    return render_template('ver_cuenta.html', cuenta=cuenta)

@app.route('/cuenta/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_cuenta(id):
    """Editar una cuenta existente"""
    cuenta = Cuenta.query.get_or_404(id)
    
    if request.method == 'POST':
        cuenta.plataforma = request.form.get('plataforma')
        cuenta.email = request.form.get('email')
        cuenta.password = request.form.get('password')
        cuenta.precio = float(request.form.get('precio', 0))
        cuenta.fecha_compra = datetime.strptime(request.form.get('fecha_compra'), '%Y-%m-%d').date()
        cuenta.estado = request.form.get('estado')
        cuenta.notas = request.form.get('notas', '')
        
        if request.form.get('fecha_venta'):
            cuenta.fecha_venta = datetime.strptime(request.form.get('fecha_venta'), '%Y-%m-%d').date()
        else:
            cuenta.fecha_venta = None
        
        try:
            db.session.commit()
            flash('✅ Cuenta actualizada exitosamente', 'success')
            return redirect(url_for('ver_cuenta', id=cuenta.id))
        except Exception as e:
            flash(f'❌ Error al actualizar cuenta: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('editar_cuenta.html', cuenta=cuenta)

@app.route('/cuenta/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_cuenta(id):
    """Eliminar una cuenta"""
    cuenta = Cuenta.query.get_or_404(id)
    
    try:
        db.session.delete(cuenta)
        db.session.commit()
        flash('✅ Cuenta eliminada exitosamente', 'success')
    except Exception as e:
        flash(f'❌ Error al eliminar cuenta: {str(e)}', 'error')
        db.session.rollback()
    
    return redirect(url_for('cuentas'))

@app.route('/usuarios')
@login_required
def listar_usuarios():
    """Listar usuarios (solo para administradores)"""
    if not current_user.es_admin:
        flash('❌ No tienes permisos para acceder a esta página', 'error')
        return redirect(url_for('index'))
    
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuario/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_usuario():
    """Crear nuevo usuario (solo para administradores)"""
    if not current_user.es_admin:
        flash('❌ No tienes permisos para acceder a esta página', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        es_admin = bool(request.form.get('es_admin'))
        
        if not all([username, email, password]):
            flash('❌ Todos los campos son obligatorios', 'error')
            return render_template('nuevo_usuario.html')
        
        if Usuario.query.filter_by(username=username).first():
            flash('❌ El nombre de usuario ya existe', 'error')
            return render_template('nuevo_usuario.html')
        
        if Usuario.query.filter_by(email=email).first():
            flash('❌ El email ya está registrado', 'error')
            return render_template('nuevo_usuario.html')
        
        try:
            nuevo_usuario = Usuario(
                username=username,
                email=email,
                es_admin=es_admin
            )
            nuevo_usuario.set_password(password)
            
            db.session.add(nuevo_usuario)
            db.session.commit()
            
            tipo_usuario = "Administrador" if es_admin else "Usuario"
            flash(f'✅ Usuario {tipo_usuario} creado exitosamente: {username}', 'success')
            return redirect(url_for('listar_usuarios'))
            
        except Exception as e:
            flash(f'❌ Error al crear usuario: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('nuevo_usuario.html')

@app.route('/usuarios/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_usuario(id):
    """Eliminar usuario (solo para administradores)"""
    if not current_user.es_admin:
        flash('❌ No tienes permisos para realizar esta acción', 'error')
        return redirect(url_for('index'))
    
    if id == current_user.id:
        flash('❌ No puedes eliminar tu propia cuenta', 'error')
        return redirect(url_for('listar_usuarios'))
    
    usuario = Usuario.query.get_or_404(id)
    
    try:
        db.session.delete(usuario)
        db.session.commit()
        flash(f'✅ Usuario {usuario.username} eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'❌ Error al eliminar usuario: {str(e)}', 'error')
        db.session.rollback()
    
    return redirect(url_for('listar_usuarios'))

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
    
    cuentas = query.order_by(Cuenta.fecha_compra.desc()).all()
    return jsonify([cuenta.to_dict() for cuenta in cuentas])

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_interno(error):
    return render_template('500.html'), 500

def crear_usuario_admin():
    """Crear usuario administrador por defecto si no existe"""
    with app.app_context():
        admin = Usuario.query.filter_by(username='admin').first()
        if not admin:
            admin = Usuario(
                username='admin',
                email='admin@gestor.com',
                es_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Usuario administrador creado:")
            print("   Usuario: admin")
            print("   Contraseña: admin123")

# Inicializar la aplicación
with app.app_context():
    db.create_all()
    crear_usuario_admin()

if __name__ == '__main__':
    # Configuración para desarrollo local
    app.run(debug=True, host='0.0.0.0', port=5000)
