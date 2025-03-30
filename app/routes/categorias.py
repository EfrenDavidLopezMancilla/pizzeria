from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.extensions import db
from app.models import Categoria, Pizza

categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/')
def listar():
    categorias = Categoria.query.options(db.joinedload(Categoria.pizzas)).order_by(Categoria.nombre).all()
    return render_template('categorias/listar.html', categorias=categorias)

@categorias_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            
            if Categoria.query.filter_by(nombre=nombre).first():
                flash('Esta categoría ya existe', 'danger')
                return redirect(url_for('categorias.crear'))
            
            nueva_categoria = Categoria(nombre=nombre, descripcion=descripcion)
            db.session.add(nueva_categoria)
            db.session.commit()
            flash('Categoría creada exitosamente', 'success')
            return redirect(url_for('categorias.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear categoría: {str(e)}', 'danger')
    
    return render_template('categorias/crear.html')

@categorias_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    categoria = Categoria.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            categoria.nombre = request.form['nombre']
            categoria.descripcion = request.form['descripcion']
            db.session.commit()
            flash('Categoría actualizada exitosamente', 'success')
            return redirect(url_for('categorias.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar categoría: {str(e)}', 'danger')
    
    return render_template('categorias/editar.html', categoria=categoria)

@categorias_bp.route('/eliminar/<int:id>')
def eliminar(id):
    try:
        categoria = Categoria.query.get_or_404(id)
        
        if categoria.pizzas:
            flash('No puedes eliminar esta categoría porque tiene pizzas asociadas', 'danger')
            return redirect(url_for('categorias.listar'))
        
        db.session.delete(categoria)
        db.session.commit()
        flash('Categoría eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar categoría: {str(e)}', 'danger')
    
    return redirect(url_for('categorias.listar'))