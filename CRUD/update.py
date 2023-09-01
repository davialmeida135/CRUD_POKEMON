#flask --app main run --debug
from app import app
from flask import render_template
import os
from flask import flash, request, redirect, url_for
from EditDB import select_all_pokemon,create_connection,Pokemon,select_pokemon_by_id,update_pokemon
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
        return render_template('select_id.html',pokemonList=pokemonList, action = "editado")

    updateId =request.form.get('pokemon_id')
    search = select_pokemon_by_id(conn,updateId)

    if search:
        link = "/update/{}".format(updateId)
        return redirect(link)
    return render_template('select_id.html',pokemonList=pokemonList,action = "editado")


#Página update de cada pokemon
@app.route('/update/<id>/', methods=['GET', 'POST'])
def update_view(id):
    database_path = "db\pokemons.db"
    conn = create_connection(database_path)
    pokemon = select_pokemon_by_id(conn,id)[0]
    pokemon = Pokemon(pokemon[0],pokemon[1],pokemon[2],pokemon[3])

    if request.method != 'POST': #primeiro load da pagina
        return render_template('update.html',id_box=pokemon.id,type_box=pokemon.type,name_box=pokemon.name)
    
    invalidPokemon = False
    filePath = None
    name_status = img_status = type_status =''
    pokemon.name = request.form.get("pokemon_name")
    pokemon.type = request.form.get("pokemon_type")
    pokemon_status = "Não foi possível editar o Pokémon"

    print(pokemon.name)
    print(pokemon.type)

    # Check if the post request has the file part
    # UPLOAD DA IMAGEM
    
    file = request.files['file']
    if file.filename == '':
        img_status=("Nenhum arquivo foi selecionado")
        flash('No selected file')
    elif file and allowed_file(file.filename):
        nomeArquivo = secure_filename(file.filename)
        filePath = 'uploads/' + nomeArquivo
        filePath = url_for('static', filename=filePath)
        print (filePath)
        pokemon.img = filePath
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], nomeArquivo))
        
     # Se não há nome e tipo, o pokemon nao pode ser editado   
    if not pokemon.name:
        name_status = "Não foi inserido um nome"
        invalidPokemon = True
        print(name_status)
    if not pokemon.type:
        invalidPokemon = True
        type_status = "Não foi inserido um tipo"
        print(type_status)
    if invalidPokemon:
        return render_template('update.html',id_box=pokemon.id,type_box=pokemon.type,name_box=pokemon.name,img_status=img_status,type_status=type_status,name_status=name_status,pokemon_status = pokemon_status)
    
    try:
        update_pokemon(conn,pokemon.id,pokemon.name,pokemon.type,pokemon.img)
        pokemon_status = "Pokémon de id {} atualizado com sucesso!".format(pokemon.id)
        
    except :
        print("Foi no except")
        return render_template('update.html',img = pokemon.img,id_box=pokemon.id,type_box=pokemon.type,name_box=pokemon.name,img_status=img_status,type_status=type_status,name_status=name_status,pokemon_status = pokemon_status)
        
    botao = "Editar outro Pokémon"
    botao_url = "/update/"
    return success_view(pokemon_status, botao,botao_url)

