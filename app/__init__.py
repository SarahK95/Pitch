from flask import Flask
# from config import config_options
from flask_bootstrap import Bootstrap
from config import config_options

app = Flask(__name__)

bootstrap = Bootstrap()

def create_app(config_name):
    # Creating the app configurations
    app.config.from_object(config_options[config_name])
    from .main import main as main_blueprint
    
  
    
    
    return app
