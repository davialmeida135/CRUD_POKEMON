#flask --app main run --debug
from app import app
from flask import render_template
from flask import request
import os
from flask import Flask, flash, request, redirect, url_for
from EditDB import select_all_pokemon,create_connection
from success import success_view



@app.route('/', methods=['GET', 'POST'])
def menu_view():
    database_path = "db\pokemons.db"
    conn = create_connection(database_path)

    database = select_all_pokemon(conn)
    return render_template('menu.html',database=database)


