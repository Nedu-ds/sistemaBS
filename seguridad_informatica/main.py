from flask import Flask, render_template, request
from flask import make_response, Response
from flask import session
from flask import flash
from flask import g
from flask_wtf.csrf import CSRFProtect
from flask import url_for
from flask import redirect
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import re




#import xtarfile as tarfile

from config import DevelopmentConfig
from models import db, User
import os,time,random
from ingreso_bajas import *
import forms

import socket
#import dns
import dns.resolver
import whois

import json
import pandas as pd
#import tkinter  as tk
#from tkinter import filedialog
import os



app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()
# app.config['UPLOAD_CORREOS'] = '/mnt/d/Accesos/CORREOS/'
# app.config['UPLOAD_LDAP'] = '/mnt/d/Accesos/LDAP/'
app.config['UPLOAD_CORREOS'] = '/home/seguridad/ssi/accesos/CORREOS/'
app.config['UPLOAD_LDAP'] = '/home/seguridad/ssi/accesos/LDAP/'


@app.errorhandler(404)
def page_nof_found(e):
    return render_template('notfound.html')

@app.before_request
def before_request():
    if 'username' not in session and request.endpoint in ['acceso','index','spam']:
        return redirect (url_for('login'))
    elif 'username' in session and request.endpoint in ['login',]:
        
        return redirect(url_for('index'))

@app.after_request
def after_request(response):
    return response
   

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        print (username)
    custome_cookie = request.cookies.get('custome_cookie','Undefined')
    return render_template('index.html',usuario=username)

@app.route('/node')
def node():
    return render_template('node.html')

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    login_form = forms.LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        username = login_form.username.data
        password = login_form.password.data
        user = User.query.filter_by(username = username).first()
        if user is not None and user.verify_password(password):
            session['username'] = username
            time.sleep(1)
            return redirect(url_for('index'))
        else:
            error_message = 'Usuario o contraseña no validos'
            flash(u'Usuario o contraseña no validos','error')
    
    return render_template('login.html', form = login_form)

@app.route('/create', methods =['GET','POST'])
def create():
    create_form = forms.CreateForm(request.form)
    users=User.query.order_by(User.id).all()
    user_id = request.form.getlist('user_ids') 
    borrar = []
    editar = []
    modificar = []
    perfil = ""
    alerta = ""
    role = ""
    if request.method == 'POST' and create_form.validate():
        user = User(create_form.username.data,
                    create_form.password.data,
                    create_form.perfil.data)
        username = create_form.username.data
        user_check = User.query.filter_by(username = username).first()
        if user_check is not None:
            error_message = 'El nombre de usuario ya existe por favor escriba uno diferente'
            flash(u'El nombre de usuario ya existe por favor escriba uno diferente','error')
        else:
            db.session.add(user)
            db.session.commit()
            success_message = 'Usuario registrado'
            flash(u'Usuario registrado','success')
            alerta="alert alert-success" 
            role="alert"

        users=User.query.order_by(User.id).all()

    elif request.method == 'POST': 
        
        if request.form['Seleccionar'] == 'seleccionar':
            print("Seleccionar  DATOS")
            if len(user_id) !=0:
                for user in user_id:
                    user_id = user.replace('check','')
                    user = User.query.get(user_id)
                    borrar=user.username
                    print(user_id)
                    print(borrar)
                #print(user.username)
                #print(user)
                #print(modificar)
                return render_template('create.html', form = create_form, usuarios=users, borrar=borrar, user_id=user_id)
            else:
                error='Debe seleccionar un usuario'
                flash(error)
                alerta="alert alert-warning"
                role="alert"
                print("Seleccionar")
                return render_template('create.html', form = create_form, usuarios=users, borrar=borrar, alerta=alerta, role=role)
            
        elif request.form['Seleccionar'] == 'eliminar':
            print("eliminar")
            borrar = request.form['borrar']
            user_id = borrar.replace('check','')
          
            if len(borrar) != 0: 
                borrar = request.form['borrar']
                user_id = borrar.replace('check','')
                print(user_id)
                db.session.delete(User.query.get(user_id))
                db.session.commit()
                message= 'Usuario Eliminado'
                flash(message)  
                alerta="alert alert-info"
                role="alert"
                users=User.query.order_by(User.id).all()
                return render_template('create.html', form = create_form, usuarios=users, borrar=borrar, alerta=alerta, role=role)            

            elif borrar == "nulo":
                error= 'Debe seleccionar primero un usuario'
                flash(error)    
                alerta="alert alert-danger"
                role="alert"
                print("Eliminar")
                return render_template('create.html', form = create_form, usuarios=users, borrar=borrar, alerta=alerta, role=role)            

            else:
                error= 'Debe seleccionar primero un usuario'
                flash(error)    
                alerta="alert alert-danger"
                role="alert"
                print("Eliminar")
                return render_template('create.html', form = create_form, usuarios=users, borrar=borrar, alerta=alerta, role=role)            

            
        
        elif request.form['Seleccionar'] == 'editar':
            print("Editar")
            editar = request.form['editar']
            print(editar)
            user_id = editar.replace('check','')
            user = User.query.get(user_id)
            modificar = request.form['modificar']
            perfil = request.form['perfil']
            
            print(perfil)
            user.username = modificar
            user.perfil = perfil
            db.session.commit()
            message= 'Usuario editado con exitosamente'
            flash(message)  
            alerta="alert alert-info"
            role="alert"
            return render_template('create.html', form = create_form, usuarios=users, editar=editar, borrar=borrar, alerta=alerta, role=role)
        


    return render_template('create.html', form = create_form, usuarios=users, borrar=borrar, alerta=alerta, role=role)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/wifi')
def wifi():
    return render_template('wifi.html')

@app.route('/cookie')
def cookie():
    response = make_response (render_template('cookie.html'))
    response.set_cookie('custome_cookie','Acessos')
    return response

@app.route('/spam', methods = ['GET', 'POST'])
def spam():
    spam_form = forms.DNSForm(request.form)
    ip_servers = []
    country_list = []
    mxdata = []
    i = 0
    option = "Whois"
    if request.method == 'POST':
        domain = spam_form.domain.data
        option = spam_form.option.data

        if option == "DNSlookup":
            try:
                ips = socket.getaddrinfo(domain,25)
                if len(ips) > 0:
                    for ip in ips:
                        i +=1
                        ip = str(ip).strip().split(',')
                        ipf = ip[4]
                        ipf = ipf.replace(" ('","")
                        ipf2 = ipf.replace("\'","")
                        if ip != ips[i-1] and i%3 == 0:
                            ip_servers.append(ipf2)
                        whois_df = pd.DataFrame ({'Name_Servers':domain,'IP Addres':ip_servers})
                        
                    return render_template('spam.html', form = spam_form, option=option, tables=[whois_df.to_html(classes='data',index_names=False)])
            except:
                flash(u'No existe el dominio','error')
                return render_template('spam.html', form = spam_form, option=option)

        if option == "MXlookup":
            
            try:
                my_resolver = dns.resolver.Resolver()
                my_resolver.nameservers = ['8.8.8.8']
                result = my_resolver.query(domain,'MX') 
                if len(result) > 0:
                    for mx in result:
                        mx_domain = str(mx)
                        mx_domain = mx_domain.split(" ")
                        mx_domain = mx_domain[1]
                        mxdata.append(mx_domain)
                        ip = socket.getaddrinfo(mx_domain,25)
                        ip = str(ip).strip().split(',')
                        ipf = ip[4]
                        ipf = ipf.replace(" ('","")
                        ipf2 = ipf.replace("\'","")
                        ip_servers.append(ipf2)
                    whois_df = pd.DataFrame ({'Name_Servers':mxdata,'IP Addres':ip_servers})
                return render_template('spam.html', form = spam_form, option=option, tables=[whois_df.to_html(classes='data',index_names=False)])
            except:
                flash(u'No existe un registro MX para el dominio','error')
                return render_template('spam.html', form = spam_form, option=option)
        
        elif option == "Whois":    
            try:
                answer = whois.whois(domain)
                name_servers = answer['name_servers']
                org = answer ['org' ]
                country = answer['country']
                if len(name_servers) > 0:
                    for domain in name_servers:
                        ip = socket.getaddrinfo(domain,25)
                        ip = str(ip).strip().split(',')
                        ipf = ip[4]
                        ipf = ipf.replace(" ('","")
                        ipf2 = ipf.replace("\'","")
                        ip_servers.append(ipf2)
                        country_list.append(country)
                    whois_df = pd.DataFrame ({'Name_Servers':name_servers,'IP Addres':ip_servers,'Country':country_list})
                    return render_template('spam.html', form = spam_form, option=option, tables=[whois_df.to_html(classes='data',index_names=False)])
            except:
                flash(u'No existe informacion del dominnio','error')
                return render_template('spam.html', form = spam_form, option=option)        
             
     
    return render_template('spam.html', form = spam_form, option=option)

  
if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    #app.run(host='10.1.16.221',port=8000)
    app.run(host='127.0.0.1',port=8000)


