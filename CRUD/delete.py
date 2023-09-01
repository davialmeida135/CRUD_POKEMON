#flask --app main run --debug
from app import app
from flask import render_template
import os
from flask import  request, redirect, url_for
from EditDB import select_all_pokemon,create_connection,Pokemon,select_pokemon_by_id,delete_pokemon
from success import success_view

#Pagina de selecionar o id do pokemon pra deletar
@app.route('/delete/', methods=['GET', 'POST'])
def delete_menu():

    database_path = "db\pokemons.db"
    conn = create_connection(database_path)
    pokemonList = select_all_pokemon(conn)

    if request.method != 'POST': #primeiro load da pagina
        return render_template('select_id.html',pokemonList=pokemonList,action = "deletado")

    deleteId = request.form.get('pokemon_id')
    search = select_pokemon_by_id(conn,deleteId)
    

    if search:
        link = "/delete/{}".format(deleteId)
        return redirect(link)
    return render_template('select_id.html',pokemonList=pokemonList,action = "deletado")

@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete_view(id):

    database_path = "db\pokemons.db"
    conn = create_connection(database_path)
    pokemon = select_pokemon_by_id(conn,id)[0]
    pokemon = Pokemon(pokemon[0],pokemon[1],pokemon[2],pokemon[3])
    pokemon_status = "Pokemon não pode ser deletado"

    if request.method != 'POST': #primeiro load da pagina
        return render_template('delete.html',id_box=pokemon.id,name_box=pokemon.name)
    
    print(pokemon)
    #Tenta deletar o pokemon
    try:
        delete_pokemon(conn,pokemon.id)
        pokemon_status = "Pokémon de id {} deletado com sucesso!".format(pokemon.id)
        
    except :
        print("Foi no except")
        return delete_menu()
        
    #Se o delete deu certo:
    botao = "Deletar outro Pokémon"
    botao_url = "/delete/"
    return success_view(pokemon_status, botao,botao_url)