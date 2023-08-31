#flask --app main run --debug
from app import app
from flask import render_template
from flask import request
import os
from flask import Flask, flash, request, redirect, url_for
from EditDB import select_all_pokemon,create_connection

@app.route('/success/', methods=['GET', 'POST'])
def success_view(success_message):
    return render_template('success.html',success_message=success_message)