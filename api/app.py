"""
Flask application initialization.
"""
from flask import Flask
from flask_cors import CORS
import config

def create_app():
    """Create and configure Flask application."""
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app, resources={
        r"/api/*": {"origins": config.CORS_ORIGINS}
    })
    
    # Register routes
    from .routes import api
    app.register_blueprint(api, url_prefix='/api')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host=config.API_HOST, port=config.API_PORT, debug=True)