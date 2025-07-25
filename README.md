# Game Store Application

An online gaming store application built with Django and PostgreSQL.

## Features

- Game management system
- User authentication and authorization
- Shopping cart functionality
- Subscription system
- Admin panel with analytics
- RESTful API

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the example environment file and configure it:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Create a PostgreSQL database:
```bash
createdb game_store_db
```

6. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

7. Create a superuser:
```bash
python manage.py createsuperuser
```

8. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

- Games: `/api/games/`
- Categories: `/api/categories/`
- Platforms: `/api/platforms/`
- Featured Games: `/api/games/featured/`
- Recommended Games: `/api/games/recommended/`

## Authentication

The API uses JWT authentication. Obtain a token by:

1. Registering a new user:
```bash
POST /api/users/register/
```

2. Logging in:
```bash
POST /api/token/
```

3. Refreshing token:
```bash
POST /api/token/refresh/
```

## Project Structure

```
game_store/
├── games/          # Game management app
├── users/          # User management app
├── admin_panel/    # Custom admin panel
├── game_store/     # Project settings
├── static/         # Static files
├── media/          # Media files
├── templates/      # Template files
└── .env            # Environment variables
```

## Project Structure
```
game_store/
├── games/          # Game management app
├── users/          # User management app
├── admin_panel/    # Custom admin panel
└── game_store/     # Project settings
```
