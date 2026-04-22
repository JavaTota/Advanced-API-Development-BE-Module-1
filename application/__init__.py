from flask import Flask

from .extensions import ma, limiter, cache
from .models import db
from .blueprints.costumers import costumer_bp
from .blueprints.mechanics import mechanic_bp
from .blueprints.service_tickets import service_ticket_bp
from .blueprints.Inventory import inventory_bp


from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.yaml'  # Our API URL (can of course be a local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Service Ticket Management API"
    }
)

def create_app(config_name):
    #initialize app
    app = Flask(__name__)
    #configure app
    app.config.from_object(f'config.{config_name}')
    

    #initialize extensions
    ma.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    #register blueprints
    app.register_blueprint(costumer_bp, url_prefix='/costumers')
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(service_ticket_bp, url_prefix='/service_tickets')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app