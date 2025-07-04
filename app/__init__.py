from flask import Flask
from .extensions import supabase
from config import Config
from datetime import datetime

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    supabase.init_app(app)

    # Register blueprints
    from .auth.routes import auth_bp
    from .dashboard.routes import dashboard_bp
    from .lessons.routes import lessons_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(lessons_bp)

    # Root route redirect
    from flask import session, redirect, url_for

    @app.route('/')
    def root():
        if 'user' in session:
            return redirect(url_for('dashboard.index'))
        return redirect(url_for('auth.login'))

    # Add datetime formatter
    @app.template_filter('format_datetime')
    def format_datetime(value, format='%b %d, %Y'):
        if isinstance(value, str):
            value = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return value.strftime(format)
        
    return app
