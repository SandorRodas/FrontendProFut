from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo
from config import globalConfig, pageConfig, getSessionDefaults

from utils.environment import getEnvironment

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from bson import ObjectId

portal_view = Blueprint('portal_view', __name__, template_folder='templates', static_folder='static')

uri = 'mongodb+srv://root:Zaragoza2023@cluster0.ahvu1c8.mongodb.net/?retryWrites=true&w=majority'


client = MongoClient(uri, server_api=ServerApi('1'))

db = client['PROFUT']
collection= db['INVENTARIO']

@portal_view.route('/portal', methods=['GET','POST'])
def mainView():
    customer, sidebar = getSessionDefaults(session)

    flashMessages = []
    pageConfig['title'] = "PRO FUT"
    pageConfig['description'] = customer
    pageConfig['detail'] = str(getEnvironment('Server')['EnvMode'])
    faq = None

    registers = collection.find()

    print(registers)
    
    return render_template('portal.html', pageConfig=pageConfig, globalconfig=globalConfig, flashMessages=flashMessages, sidebar=sidebar, faq=faq, registers=registers)

@portal_view.route('/portal/login', methods=['GET','POST'])
def catchRedirect():
    data = request.args.get('origin')
    return data

@portal_view.route('/portal/create', methods=['POST'])
def create():

    data = {
        'code': request.form['Code'].split(' ')[0],
        'name': request.form['Name'].split(' ')[0],
        'price': request.form['Price'].split(' ')[0],
        'amount': request.form['Amount'].split(' ')[0]
    }

    result = collection.insert_one(data)
    return redirect(url_for('portal_view.mainView'))

@portal_view.route('/portal/editForm', methods=['POST'])
def edit():

    id = ObjectId(request.form['Id'].split(' ')[0])
    
    collection.update_one({'_id': id}, {'$set': {
        'code': request.form['Code'].split(' ')[0],
        'name': request.form['Name'].split(' ')[0],
        'price': request.form['Price'].split(' ')[0],
        'amount': request.form['Amount'].split(' ')[0]
    }})
    
    return redirect(url_for('portal_view.mainView'))

@portal_view.route('/portal/edit/')
def getEdit():

    id = request.args.get('id')

    if id:
        try:
            # Convierte el ID en un objeto ObjectId de MongoDB
            obj_id = ObjectId(id)

            # Intenta eliminar el documento por su ID
            elemento = collection.find_one({'_id': obj_id})

            if elemento:
                return render_template("partials/editForm.html", register=elemento)
            else:
                return jsonify({"mensaje": "No se encontró el documento con ese ID"}), 404

        except Exception as e:
            return jsonify({"mensaje": "Error al consultar el documento", "error": str(e)}), 500

    return jsonify({"mensaje": "Error al consultar el documento", "error": str(e)}), 500

@portal_view.route('/portal/delete/')
def delete():

    id = request.args.get('id')

    if id:
        try:
            # Convierte el ID en un objeto ObjectId de MongoDB
            obj_id = ObjectId(id)

            # Intenta eliminar el documento por su ID
            result = collection.delete_one({'_id': obj_id})

            if result.deleted_count == 1:
                return redirect(url_for('portal_view.mainView'))
            else:
                return jsonify({"mensaje": "No se encontró el documento con ese ID"}), 404

        except Exception as e:
            return jsonify({"mensaje": "Error al eliminar el documento", "error": str(e)}), 500

    return redirect(url_for('portal_view.mainView'))
    
