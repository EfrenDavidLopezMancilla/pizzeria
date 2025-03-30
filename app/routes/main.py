from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/sobre-nosotros')
def sobre_nosotros():
    return render_template('sobre_nosotros.html')