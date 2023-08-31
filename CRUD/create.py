#flask --app main run --debug
from app import app
from flask import render_template
import os
from pathlib import Path
from flask import flash, request, redirect, url_for
from EditDB import select_all_pokemon,create_pokemon,create_connection,Pokemon
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


#Pagina criar pokemon
@app.route('/create/', methods=['GET', 'POST'])
def create_view():

    #pokemonName, pokemonType ,pokemonId ,pokemon_img,filename, img_status ,name_status, type_status

    ''' Criar conexão com database de pokemons
        Criar array com todos os pokemons da database'''
    
    database_path = "db\pokemons.db"
    conn = create_connection(database_path)

    database = select_all_pokemon(conn) #array de arrays com todos os pokemons da database

    newPokemon = Pokemon(1,'','','https://img.pokemondb.net/artwork/vector/large/unown-question.png')
    newPokemon.id = 1

    invalidPokemon = False
    if len(database) > 0:
        newPokemon.id = database[-1][0] +1 #id do proximo pokemon a ser criado será o id do ultimo pokemon +1

        

    if request.method != 'POST': #primeiro load da pagina
        return render_template('create.html',id_box=newPokemon.id)
    

    filepath = None
    name_status = img_status = type_status =''
    newPokemon.name = request.form.get("pokemon_name")
    newPokemon.type = request.form.get("pokemon_type")
    newPokemon_status = "Não foi possível criar o Pokémon"

    print(newPokemon.name)
    print(newPokemon.type)

    # Check if the post request has the file part
    # UPLOAD DA IMAGEM
    

    file = request.files['file']
    if file.filename == '':
        img_status=("Nenhum arquivo foi selecionado")
        flash('No selected file')
    elif file and allowed_file(file.filename):
        nomearquivo = secure_filename(file.filename)
        filepath = 'uploads/' + nomearquivo
        filepath = url_for('static', filename=filepath)
        print (filepath)
        newPokemon.img = filepath
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], nomearquivo))
        
     # Se não há nome e tipo, o pokemon nao pode ser criado   
    if not newPokemon.name:
        name_status = "Não foi inserido um nome"
        invalidPokemon = True
        print(name_status)
    if not newPokemon.type:
        invalidPokemon = True
        type_status = "Não foi inserido um tipo"
        print(type_status)
    if invalidPokemon:
        return render_template('create.html',img = newPokemon.img,id_box=newPokemon.id,type_box=newPokemon.type,name_box=newPokemon.name,img_status=img_status,type_status=type_status,name_status=name_status,newPokemon_status = newPokemon_status)
    try:
        create_pokemon(conn,(newPokemon.id,newPokemon.name,newPokemon.type,newPokemon.img))
        newPokemon_status = "Pokémon de id {} criado com sucesso!".format(newPokemon.id)
        
    except Exception as e:
        create_pokemon(conn,(newPokemon.id,newPokemon.name,newPokemon.type,newPokemon.img))


    return success_view(newPokemon_status)

        

