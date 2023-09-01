#flask --app main run --debug
from app import app
from flask import render_template
from flask import request
import os
from flask import request
from EditDB import select_all_pokemon,create_connection




@app.route('/', methods=['GET', 'POST'])
def menu_view():
    databasePath = "db\pokemons.db"
    conn = create_connection(databasePath)
    database = select_all_pokemon(conn)
    pesquisa = request.args.get('search')
    

    listaPokemons = []
    if pesquisa:
        pesquisa = pesquisa.lower()
        for p in database:
            if pesquisa in p[1].lower():
                listaPokemons.append(p)
        if len(listaPokemons) ==0:
            listaPokemons = database
    else:
        listaPokemons = database

    return render_template('menu.html',database=listaPokemons)