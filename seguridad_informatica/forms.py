from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms import StringField, StringField, validators, PasswordField, SelectField,BooleanField, SelectMultipleField
from wtforms.validators import DataRequired
from models import User



class LoginForm(Form):
    username = StringField('Usuario', [validators.DataRequired(message = 'El usurio es requerido')])
    password = PasswordField('Contraseña', [validators.DataRequired(message = 'El usurio es requerido')])
    def validate_username(form, field):
        username = field.data
        user = User.query.filter_by(username = username).first()
        print(username)   
        print(user)   
        
class CreateForm(Form):
    username = StringField('Username', 
                [
                  validators.DataRequired(message = 'Ingrese un usuario'),
                  validators.length(min=5, max=10, message='Ingrese un Usuario valido')
                ])
    password = PasswordField('Password',[validators.DataRequired(message='Ingrese un Password')])
    perfil =SelectField('Perfil', choices=[("Admin", "Administrador"), ("Config", "Operador"), ("Viewer", "Visualizador")])
    checkbox=BooleanField('delete_user', default=False)

    def validate_username_create(form, field):
        username = field.data
        user = User.query.filter_by(username = username).first()
        if user is None:
            raise validators.ValidationError('El Usuario ya se encuentra registrado')

class IngresosForm(Form):
    mes =SelectField('nombre', choices=[("Nulo", ""),("Ene-Mar", "Ene-Mar"), ("Abr-Jun", "Abr-Jun"), ("Jul-Sep", "Jul-Sep"), ("Oct-Dic", "Oct-Dic")])
    year= SelectField('year', choices=[("Nulo", ""),("2019", "2019"),("2020", "2020"),("2021", "2021"),("2022", "2022"),("2023", "2023"),("2024", "2024"),("2025", "2025"),("2026", "2026")])
    checkbox=BooleanField()
    directorio_ingreso=StringField('Ingreso',[validators.DataRequired(message = 'La Direccion de la Carpeta es requerida')])
    archivo_ldap=StringField('Ldap',[validators.DataRequired(message = 'La Dirección del Archivo es requerida')])
    archivo_correo=StringField('Correo',[validators.DataRequired(message = 'La Dirección del Archivo es requerida')])
    
class BajasForm(Form):
    mes =SelectField('nombre', choices=[("Nulo", ""),("Ene-Mar", "Ene-Mar"), ("Abr-Jun", "Abr-Jun"), ("Jul-Sep", "Jul-Sep"), ("Oct-Dic", "Oct-Dic")])
    year= SelectField('year', choices=[("Nulo", ""),("2019", "2019"),("2020", "2020"),("2021", "2021"),("2022", "2022"),("2023", "2023"),("2024", "2024"),("2025", "2025"),("2026", "2026")])
    checkbox=BooleanField()

class DNSForm(Form):
    domain = StringField('Dominio', [validators.DataRequired(message = 'El dominio es requerido')])
    option = SelectField('Option', choices=[("Whois", "Whois"), ("DNSlookup", "DNSlookup"), ("MXlookup", "MXlookup")])