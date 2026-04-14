from flask import Flask

from .extensions import ma
from .models import db
from .blueprints.costumers import costumer_bp

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    

    #initialize extensions
    ma.init_app(app)
    db.init_app(app)

    #register blueprints
    app.register_blueprint(costumer_bp, url_prefix='/costumers')

    return app