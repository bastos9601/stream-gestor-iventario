#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestor de Cuentas de Streaming - Aplicación Web
Sistema web para gestionar inventario de cuentas de streaming desde cualquier dispositivo
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuración para Render
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'tu-clave-secreta-aqui')

# Configuración de base de datos para PostgreSQL en Render
database_url = os.getenv('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///gestor_cuentas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_timeout': 20,
    'pool_recycle': 300,
    'max_overflow': 0
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
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    es_admin = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    
    # Relación con cuentas
    cuentas = db.relationship('Cuenta', backref='usuario', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Modelo de Cuenta (actualizado)
class Cuenta(db.Model):
    """Modelo de la base de datos para las cuentas"""
    id = db.Column(db.Integer, primary_key=True)
    plataforma = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    fecha_compra = db.Column(db.Date, nullable=False)
    notas = db.Column(db.Text)
    estado = db.Column(db.String(20), default='Disponible')
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_venta = db.Column(db.DateTime)
    nombre_comprador = db.Column(db.String(100))
    whatsapp_comprador = db.Column(db.String(20))
    fecha_vencimiento = db.Column(db.Date)
    
    # Nuevo campo para asociar cuentas con usuarios
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    
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
            'usuario_id': self.usuario_id
        }

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        usuario = Usuario.query.filter_by(username=username, activo=True).first()
        
        if usuario and usuario.check_password(password):
            login_user(usuario)
            flash(f'¡Bienvenido, {usuario.username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
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
        
        usuarios_stats = None
        ultimas_cuentas = Cuenta.query.filter_by(usuario_id=current_user.id).order_by(Cuenta.fecha_creacion.desc()).limit(5).all()
    
    # Cuentas por plataforma (solo del usuario actual o todas si es admin)
    if current_user.es_admin:
        plataformas = db.session.query(
            Cuenta.plataforma, 
            db.func.count(Cuenta.id).label('cantidad')
        ).filter_by(estado='Disponible').group_by(Cuenta.plataforma).all()
    else:
        plataformas = db.session.query(
            Cuenta.plataforma, 
            db.func.count(Cuenta.id).label('cantidad')
        ).filter_by(usuario_id=current_user.id, estado='Disponible').group_by(Cuenta.plataforma).all()
    
    return render_template('index.html',
                         total_cuentas=total_cuentas,
                         cuentas_disponibles=cuentas_disponibles,
                         cuentas_vendidas=cuentas_vendidas,
                         plataformas=plataformas,
                         ultimas_cuentas=ultimas_cuentas,
                         usuarios_stats=usuarios_stats,
                         valor_inventario_admin=valor_inventario_admin if current_user.es_admin else 0,
                         valor_inventario_usuario=valor_inventario_usuario if not current_user.es_admin else 0)

@app.route('/cuentas')
@login_required
def cuentas():
    """Lista de cuentas"""
    plataforma = request.args.get('plataforma', '')
    
    if current_user.es_admin:
        # Administrador ve todas las cuentas
        query = Cuenta.query
        if plataforma:
            query = query.filter_by(plataforma=plataforma)
    else:
        # Usuario normal solo ve sus propias cuentas
        query = Cuenta.query.filter_by(usuario_id=current_user.id)
        if plataforma:
            query = query.filter_by(plataforma=plataforma)
    
    cuentas = query.order_by(Cuenta.fecha_creacion.desc()).all()
    plataformas_disponibles = db.session.query(Cuenta.plataforma).distinct().all()
    
    return render_template('cuentas.html', cuentas=cuentas, plataformas=plataformas_disponibles)

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
        
        # Verificar que el email no esté duplicado para este usuario
        cuenta_existente = Cuenta.query.filter_by(
            email=email, 
            usuario_id=current_user.id
        ).first()
        
        if cuenta_existente:
            flash('Ya existe una cuenta con este email para tu usuario', 'error')
            return render_template('nueva_cuenta.html')
        
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
        
        # Verificar que el email no esté duplicado para este usuario (excluyendo la cuenta actual)
        cuenta_existente = Cuenta.query.filter(
            Cuenta.email == email,
            Cuenta.usuario_id == current_user.id,
            Cuenta.id != id
        ).first()
        
        if cuenta_existente:
            flash('Ya existe otra cuenta con este email para tu usuario', 'error')
            return render_template('editar_cuenta.html', cuenta=cuenta)
        
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
        return redirect(url_for('cuentas'))
    except Exception as e:
        flash(f'❌ Error al eliminar cuenta: {str(e)}', 'error')
        db.session.rollback()
        return redirect(url_for('ver_cuenta', id=cuenta.id))

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
    if not current_user.es_admin:
        flash('No tienes permisos para realizar esta acción', 'error')
        return redirect(url_for('index'))
    
    usuario = Usuario.query.get_or_404(id)
    
    # No permitir eliminar el propio usuario
    if usuario.id == current_user.id:
        flash('No puedes eliminar tu propio usuario', 'error')
        return redirect(url_for('usuarios'))
    
    # Verificar si el usuario tiene cuentas
    if usuario.cuentas:
        flash('No se puede eliminar un usuario que tiene cuentas asociadas', 'error')
        return redirect(url_for('usuarios'))
    
    db.session.delete(usuario)
    db.session.commit()
    
    flash('Usuario eliminado correctamente', 'success')
    return redirect(url_for('usuarios'))

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
    # Configuración para producción (Render)
    with app.app_context():
        db.create_all()
        crear_admin_inicial()
