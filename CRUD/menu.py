#flask --app hello run --debug
from app import app
from flask import render_template
from flask import request
import os
from flask import Flask, flash, request, redirect, url_for
from EditDB import select_all_pokemon,create_connection



@app.route('/', methods=['GET', 'POST'])
def menu_view():
    return render_template('menu.html')
