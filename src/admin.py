import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
# Asegúrate de que `User` y otros modelos estén importados
from models import db, User


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='Star Wars Admin', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    # Agrega tus otros modelos aquí si es necesario
    # admin.add_view(ModelView(OtherModel, db.session))
