from flask import Flask, render_template, request, Response
from flask.ext.pymongo import PyMongo
from forms import PkForm
from config import config

from . import mod

@mod.route('/')
def index():
    pk_form = PkForm()

    return render_template('index.html',username="Dave",form=pk_form)

@mod.route('/pk', methods=['GET', 'POST'])
def pk():
    pk_form = PkForm()
    if pk_form.validate_on_submit():
        pk1_name = request.form.get('pk1')
        pk2_name = request.form.get('pk2')
        return render_template('pk.html',pk1=pk1_name, pk2=pk2_name)
    return Response("none")

