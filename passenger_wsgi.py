import os
import sys

# Add the project directory to the Python path
# INTERP = os.path.expanduser("~/venv/bin/python3")  # Update this path to your Python interpreter
# if sys.executable != INTERP:
#     os.execl(INTERP, INTERP, *sys.argv)

# # Set the application environment
# os.environ.setdefault('FLASK_APP', 'app')
# os.environ.setdefault('FLASK_ENV', 'production')

# Import the application
from app import create_app

# Create the application instance
application = create_app()

if __name__ == "__main__":
    # This block is only for local testing
    application.run()
