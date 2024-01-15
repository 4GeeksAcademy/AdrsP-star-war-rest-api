import os
from flask_admin import Admin
from models import db, User, Planet, Favorites, Character # aca importo los modelos de tabla que se crearon en models.py para renderizarlos con la funcion setup admin
from flask_admin.contrib.sqla import ModelView   

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))       # cada uno de estos modelos se agrega a la interfaz grafica generada, se debe crear 
    admin.add_view(ModelView(Planet, db.session))     # una vista por modelo pero todos se muestran en la navbar y se desplegan uno a uno
    admin.add_view(ModelView(Favorites, db.session))  # automaticamente 
    admin.add_view(ModelView(Character, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))