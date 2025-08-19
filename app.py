#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestor de Cuentas de Streaming - Aplicación Web
Sistema web para gestionar inventario de cuentas de streaming desde cualquier dispositivo
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)

# Configuración para Render
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tu_clave_secreta_aqui_2024')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///cuentas_streaming.db')
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

@app.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    """Página de perfil del usuario para cambiar contraseña"""
    if request.method == 'POST':
        contraseña_actual = request.form.get('contraseña_actual')
        nueva_contraseña = request.form.get('nueva_contraseña')
        confirmar_contraseña = request.form.get('confirmar_contraseña')
        
        # Validar que la contraseña actual sea correcta
        if not current_user.check_password(contraseña_actual):
            flash('❌ La contraseña actual es incorrecta', 'error')
            return render_template('perfil.html')
        
        # Validar que las nuevas contraseñas coincidan
        if nueva_contraseña != confirmar_contraseña:
            flash('❌ Las nuevas contraseñas no coinciden', 'error')
            return render_template('perfil.html')
        
        # Validar longitud mínima de contraseña
        if len(nueva_contraseña) < 6:
            flash('❌ La nueva contraseña debe tener al menos 6 caracteres', 'error')
            return render_template('perfil.html')
        
        try:
            # Cambiar la contraseña
            current_user.set_password(nueva_contraseña)
            db.session.commit()
            flash('✅ Contraseña cambiada exitosamente', 'success')
            return redirect(url_for('perfil'))
        except Exception as e:
            flash(f'❌ Error al cambiar la contraseña: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('perfil.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    """Página principal con dashboard"""
    # Obtener estadísticas
    total_cuentas = Cuenta.query.count()
    cuentas_disponibles = Cuenta.query.filter_by(estado='disponible').count()
    cuentas_vendidas = Cuenta.query.filter_by(estado='vendida').count()
    valor_total = db.session.query(db.func.sum(Cuenta.precio)).filter_by(estado='disponible').scalar() or 0
    
    # Cuentas por plataforma
    plataformas = db.session.query(
        Cuenta.plataforma, 
        db.func.count(Cuenta.id).label('cantidad')
    ).filter_by(estado='disponible').group_by(Cuenta.plataforma).all()
    
    # Últimas cuentas agregadas
    ultimas_cuentas = Cuenta.query.order_by(Cuenta.created_at.desc()).limit(5).all()
    
    return render_template('index.html',
                         total_cuentas=total_cuentas,
                         cuentas_disponibles=cuentas_disponibles,
                         cuentas_vendidas=cuentas_vendidas,
                         valor_total=valor_total,
                         plataformas=plataformas,
                         ultimas_cuentas=ultimas_cuentas)

@app.route('/cuentas')
@login_required
def listar_cuentas():
    """Listar todas las cuentas"""
    estado = request.args.get('estado', '')
    plataforma = request.args.get('plataforma', '')
    
    query = Cuenta.query
    
    if estado:
        query = query.filter_by(estado=estado)
    if plataforma:
        query = query.filter_by(plataforma=plataforma)
    
    cuentas = query.order_by(Cuenta.fecha_compra.desc()).all()
    plataformas_disponibles = db.session.query(Cuenta.plataforma).distinct().all()
    
    return render_template('cuentas.html', 
                         cuentas=cuentas, 
                         plataformas=plataformas_disponibles,
                         filtro_estado=estado,
                         filtro_plataforma=plataforma)

@app.route('/cuentas/nueva', methods=['GET', 'POST'])
@login_required
def nueva_cuenta():
    """Agregar nueva cuenta"""
    if request.method == 'POST':
        try:
            plataforma = request.form['plataforma']
            email = request.form['email']
            password = request.form['password']
            precio = float(request.form['precio'])
            fecha_compra = datetime.strptime(request.form['fecha_compra'], '%Y-%m-%d').date()
            notas = request.form.get('notas', '')
            
            nueva_cuenta = Cuenta(
                plataforma=plataforma,
                email=email,
                password=password,
                precio=precio,
                fecha_compra=fecha_compra,
                notas=notas
            )
            
            db.session.add(nueva_cuenta)
            db.session.commit()
            
            flash('✅ Cuenta agregada exitosamente', 'success')
            return redirect(url_for('listar_cuentas'))
            
        except Exception as e:
            flash(f'❌ Error al agregar cuenta: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('nueva_cuenta.html')

@app.route('/cuentas/<int:id>')
@login_required
def ver_cuenta(id):
    """Ver detalles de una cuenta específica"""
    cuenta = Cuenta.query.get_or_404(id)
    return render_template('ver_cuenta.html', cuenta=cuenta)

@app.route('/cuentas/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_cuenta(id):
    """Editar una cuenta existente (solo para administradores)"""
    if not current_user.es_admin:
        flash('❌ Solo los administradores pueden editar cuentas', 'error')
        return redirect(url_for('ver_cuenta', id=id))
    
    cuenta = Cuenta.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            cuenta.plataforma = request.form['plataforma']
            cuenta.email = request.form['email']
            cuenta.password = request.form['password']
            cuenta.precio = float(request.form['precio'])
            cuenta.fecha_compra = datetime.strptime(request.form['fecha_compra'], '%Y-%m-%d').date()
            cuenta.notas = request.form.get('notas', '')
            
            db.session.commit()
            flash('✅ Cuenta actualizada exitosamente', 'success')
            return redirect(url_for('ver_cuenta', id=cuenta.id))
            
        except Exception as e:
            flash(f'❌ Error al actualizar cuenta: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('editar_cuenta.html', cuenta=cuenta)

@app.route('/cuentas/<int:id>/vender', methods=['POST'])
@login_required
def vender_cuenta(id):
    """Marcar una cuenta como vendida (solo para administradores)"""
    if not current_user.es_admin:
        flash('❌ Solo los administradores pueden vender cuentas', 'error')
        return redirect(url_for('ver_cuenta', id=id))
    
    cuenta = Cuenta.query.get_or_404(id)
    
    if cuenta.estado == 'disponible':
        cuenta.estado = 'vendida'
        cuenta.fecha_venta = datetime.now().date()
        db.session.commit()
        flash('💰 Cuenta vendida exitosamente', 'success')
    else:
        flash('❌ La cuenta ya no está disponible', 'error')
    
    return redirect(url_for('ver_cuenta', id=cuenta.id))

@app.route('/cuentas/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_cuenta(id):
    """Eliminar una cuenta (solo para administradores)"""
    if not current_user.es_admin:
        flash('❌ Solo los administradores pueden eliminar cuentas', 'error')
        return redirect(url_for('ver_cuenta', id=id))
    
    cuenta = Cuenta.query.get_or_404(id)
    
    try:
        db.session.delete(cuenta)
        db.session.commit()
        flash('🗑️ Cuenta eliminada exitosamente', 'success')
        return redirect(url_for('listar_cuentas'))
    except Exception as e:
        flash(f'❌ Error al eliminar cuenta: {str(e)}', 'error')
        db.session.rollback()
        return redirect(url_for('ver_cuenta', id=cuenta.id))

@app.route('/api/estadisticas')
@login_required
def api_estadisticas():
    """API para obtener estadísticas en formato JSON"""
    total_cuentas = Cuenta.query.count()
    cuentas_disponibles = Cuenta.query.filter_by(estado='disponible').count()
    cuentas_vendidas = Cuenta.query.filter_by(estado='vendida').count()
    valor_total = db.session.query(db.func.sum(Cuenta.precio)).filter_by(estado='disponible').scalar() or 0
    
    plataformas = db.session.query(
        Cuenta.plataforma, 
        db.func.count(Cuenta.id).label('cantidad')
    ).filter_by(estado='disponible').group_by(Cuenta.plataforma).all()
    
    return jsonify({
        'total': total_cuentas,
        'disponibles': cuentas_disponibles,
        'vendidas': cuentas_vendidas,
        'valor_total': valor_total,
        'plataformas': [{'plataforma': p.plataforma, 'cantidad': p.cantidad} for p in plataformas]
    })

@app.route('/usuarios')
@login_required
def listar_usuarios():
    """Listar todos los usuarios (solo para administradores)"""
    if not current_user.es_admin:
        flash('❌ No tienes permisos para acceder a esta página', 'error')
        return redirect(url_for('index'))
    
    usuarios = Usuario.query.order_by(Usuario.fecha_registro.desc()).all()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuarios/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_usuario():
    """Crear nuevo usuario (solo para administradores)"""
    if not current_user.es_admin:
        flash('❌ No tienes permisos para acceder a esta página', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            es_admin = 'es_admin' in request.form
            
            # Verificar si el usuario ya existe
            if Usuario.query.filter_by(username=username).first():
                flash('❌ El nombre de usuario ya existe', 'error')
                return render_template('nuevo_usuario.html')
            
            if Usuario.query.filter_by(email=email).first():
                flash('❌ El email ya está registrado', 'error')
                return render_template('nuevo_usuario.html')
            
            # Crear nuevo usuario
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        crear_usuario_admin()
    
    # Configuración para desarrollo
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    # Configuración para producción (Render)
    with app.app_context():
        db.create_all()
        crear_usuario_admin()
