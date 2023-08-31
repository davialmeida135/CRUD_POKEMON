#flask --app main run --debug
from app import app
from flask import render_template
import os
from pathlib import Path
from flask import flash, request, redirect, url_for
from EditDB import select_all_pokemon,create_pokemon,create_connection,Pokemon,select_pokemon_by_id,update_pokemon
from werkzeug.utils import secure_filename
from success import success_view


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'secret_key'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#Pagina update pokemon
@app.route('/update/', methods=['GET', 'POST'])
def update_menu():

    database_path = "db\pokemons.db"
    conn = create_connection(database_path)
    pokemonList = select_all_pokemon(conn)

    if request.method != 'POST': #primeiro load da pagina
        return render_template('update_menu.html',pokemonList=pokemonList)

    updateId =request.form.get('pokemon_id')
    search = select_pokemon_by_id(conn,updateId)

    if search:
        link = "/update/{}".format(updateId)
        return redirect(link)
    return render_template('update_menu.html',pokemonList=pokemonList)

@app.route('/update/<id>/', methods=['GET', 'POST'])
def update_view(id):
    return id