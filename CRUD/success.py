#flask --app main run --debug
from app import app
from flask import render_template
import os

@app.route('/success/', methods=['GET', 'POST'])
def success_view(successMessage,botao,botao_url):
    return render_template('success.html',success_message=successMessage,botao=botao,botao_url=botao_url)