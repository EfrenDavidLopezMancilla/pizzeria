from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.extensions import db
from app.models import Pizza, Categoria
import os
from werkzeug.utils import secure_filename

pizzas_bp = Blueprint('pizzas', __name__)

UPLOAD_FOLDER = 'app/static/img/pizzas'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@pizzas_bp.route('/')
def listar():
    pizzas = Pizza.query.options(db.joinedload(Pizza.categoria)).order_by(Pizza.nombre).all()
    categorias = Categoria.query.all()
    return render_template('pizzas/listar.html', pizzas=pizzas, categorias=categorias)

@pizzas_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            ingredientes = request.form['ingredientes']
            precio = float(request.form['precio'])
            disponible = 'disponible' in request.form
            categoria_id = request.form['categoria_id'] or None
            
            imagen_url = None
            if 'imagen' in request.files:
                file = request.files['imagen']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    imagen_url = filename

            nueva_pizza = Pizza(
                nombre=nombre,
                descripcion=descripcion,
                ingredientes=ingredientes,
                precio=precio,
                disponible=disponible,
                categoria_id=categoria_id,
                imagen_url=imagen_url
            )
            
            db.session.add(nueva_pizza)
            db.session.commit()
            flash('Pizza creada exitosamente', 'success')
            return redirect(url_for('pizzas.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear pizza: {str(e)}', 'danger')

    categorias = Categoria.query.all()
    return render_template('pizzas/crear.html', categorias=categorias)

@pizzas_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    pizza = Pizza.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            pizza.nombre = request.form['nombre']
            pizza.descripcion = request.form['descripcion']
            pizza.ingredientes = request.form['ingredientes']
            pizza.precio = float(request.form['precio'])
            pizza.disponible = 'disponible' in request.form
            pizza.categoria_id = request.form['categoria_id'] or None
            
            if 'imagen' in request.files:
                file = request.files['imagen']
                if file and allowed_file(file.filename):
                    if pizza.imagen_url:
                        try:
                            os.remove(os.path.join(UPLOAD_FOLDER, pizza.imagen_url))
                        except:
                            pass
                    filename = secure_filename(file.filename)
                    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    pizza.imagen_url = filename
            
            db.session.commit()
            flash('Pizza actualizada exitosamente', 'success')
            return redirect(url_for('pizzas.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar pizza: {str(e)}', 'danger')
    
    categorias = Categoria.query.all()
    return render_template('pizzas/editar.html', pizza=pizza, categorias=categorias)

@pizzas_bp.route('/eliminar/<int:id>')
def eliminar(id):
    try:
        pizza = Pizza.query.get_or_404(id)
        
        if pizza.imagen_url:
            try:
                os.remove(os.path.join(UPLOAD_FOLDER, pizza.imagen_url))
            except:
                pass
        
        db.session.delete(pizza)
        db.session.commit()
        flash('Pizza eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar pizza: {str(e)}', 'danger')
    
    return redirect(url_for('pizzas.listar'))