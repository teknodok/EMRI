from flask import Flask, redirect, url_for
from config import Config
from extensions import login_manager, mail
from auth.routes import auth_bp
from departments.operations.routes import operations_bp
from departments.technology.routes import technology_bp
from departments.quality.routes import quality_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize extensions
    login_manager.init_app(app)
    mail.init_app(app)
    login_manager.login_view = 'auth.login'

    # register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(operations_bp, url_prefix='/operations')
    app.register_blueprint(technology_bp, url_prefix='/technology')
    app.register_blueprint(quality_bp, url_prefix='/quality')

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
