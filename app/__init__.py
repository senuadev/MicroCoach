from flask import Flask, render_template
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
    def landing():
        if 'user' in session:
            return redirect(url_for('dashboard.index'))
        #return redirect(url_for('auth.login'))
        return render_template('landing.html')

    # Add datetime formatter
    @app.template_filter('format_datetime')
    def format_datetime(value, format='%b %d, %Y'):
        if value is None:
            return ''
            
        if isinstance(value, str):
            # Handle different datetime string formats
            try:
                if 'T' in value and '+' in value:
                    # Handle ISO 8601 format with timezone
                    value = datetime.fromisoformat(value.replace('Z', '+00:00'))
                else:
                    # Handle other string formats
                    value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return value  # Return original if parsing fails
                
        if isinstance(value, datetime):
            return value.strftime(format)
            
        return str(value)
        
    return app
