# MicroCoach - Interactive Learning Platform

MicroCoach is a Flask-based web application that provides an interactive learning experience with AI-powered assistance using Google's Gemini API.

## Features

- User authentication and authorization
- Interactive lessons and quizzes
- AI-powered chat assistant
- Progress tracking and achievements
- Responsive design

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Node.js and npm (for frontend assets)
- Supabase account
- Google Cloud account with Gemini API access

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/senuadev/microcoach.git
   cd microcoach
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your Supabase and Google API credentials

5. Initialize the database:
   ```bash
   flask db upgrade
   ```

## Running the Application

### Development

```bash
flask run
```

The application will be available at `http://localhost:5000`

### Production

For production deployment, use a production WSGI server like Gunicorn:

```bash
gunicorn -w 4 'app:create_app()'
```

## Configuration

Configuration is handled through environment variables. See `.env.example` for all available options.

## Project Structure

```
microcoach/
├── app/                    # Application package
│   ├── static/             # Static files (CSS, JS, images)
│   ├── templates/          # Jinja2 templates
│   ├── auth/               # Authentication routes and logic
│   ├── dashboard/          # Dashboard routes and views
│   ├── lessons/            # Lesson management
│   ├── assistant/          # AI assistant integration
│   ├── models/             # Database models
│   ├── __init__.py         # Application factory
│   └── extensions.py       # Flask extensions
├── migrations/             # Database migrations
├── tests/                  # Test suite
├── .env.example            # Example environment variables
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Testing

Run the test suite with:

```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Flask for the web framework
- Supabase for authentication and database
- Google Gemini for AI capabilities
- Bootstrap for responsive design
