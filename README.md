# 📋 TaskFlow - Django & Streamlit To-Do Application

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-4.2%2B-green.svg)](https://www.djangoproject.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A modern, full-stack task management application combining the power of **Django REST Framework** for robust backend operations and **Streamlit** for an intuitive, real-time frontend experience.


## ✨ Key Features

### 🔐 **Authentication & Security**
- JWT-based user authentication with secure token management
- Password hashing using Django's built-in security features
- User isolation - access only your own tasks
- Session management with automatic token refresh

### 📝 **Task Management**
- Create, read, update, and delete tasks with ease
- Mark tasks as complete/incomplete with visual feedback
- Rich text support for task descriptions
- Task priority levels (High, Medium, Low)
- Due date tracking with overdue notifications

### 🔍 **Advanced Filtering & Search**
- Real-time search functionality across task titles and descriptions
- Filter by completion status, priority, and due dates
- "Today's Tasks" quick filter for daily focus
- Custom date range filtering

### 📊 **Analytics & Visualization**
- Interactive dashboard with Plotly charts
- Task completion statistics and progress tracking
- Visual breakdown of tasks by priority and status
- Historical performance metrics

### 🚀 **Real-time Features**
- Live updates using Django Channels and WebSockets
- Auto-refresh functionality for seamless collaboration
- Real-time task status synchronization
- Instant notifications for task updates

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Django REST Framework | API endpoints and business logic |
| **Frontend** | Streamlit | Interactive web interface |
| **Database** | SQLite (dev) / PostgreSQL (prod) | Data persistence |
| **Authentication** | JWT (SimpleJWT) | Secure user sessions |
| **Real-time** | Django Channels + Redis | WebSocket connections |
| **Visualization** | Plotly | Interactive charts and graphs |
| **Deployment** | Docker + Docker Compose | Containerized deployment |

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Redis server (for real-time features)
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/taskflow-django-streamlit.git
cd taskflow-django-streamlit
```

### 2. Environment Setup
Create a `.env` file in the project root:
```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Redis (for real-time features)
REDIS_URL=redis://localhost:6379

# JWT Settings
ACCESS_TOKEN_LIFETIME=60
REFRESH_TOKEN_LIFETIME=1440

# API Configuration
API_BASE_URL=http://127.0.0.1:8000
```

### 3. Backend Setup
```bash
# Navigate to backend directory
cd todo_backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start Django server
python manage.py runserver
```

### 4. Frontend Setup
```bash
# Open new terminal and navigate to frontend
cd streamlit_frontend

# Install Streamlit dependencies
pip install -r requirements.txt

# Launch Streamlit app
streamlit run app.py
```

### 5. Access the Application
- **Frontend (Streamlit)**: http://localhost:8501
- **Backend API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/

## 📁 Project Structure

```
TODO_BACKEND/
├── streamlit_frontend/           # Streamlit frontend
│   ├── venv/                     # Virtual environment
│   ├── .env                      # Environment variables
│   ├── app.py                    # Main Streamlit application
│   └── requirements.txt          # Frontend dependencies
├── tasks/                        # Django tasks app
│   ├── __pycache__/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── consumers.py              # WebSocket consumers
│   ├── csrf_exempt_mixin.py
│   ├── models.py                 # Task models
│   ├── serializers.py            # DRF serializers
│   ├── tests.py
│   ├── urls.py                   # Task URLs
│   └── views.py                  # Task views
├── todo_backend/                 # Django project settings
│   ├── __pycache__/
│   ├── __init__.py
│   ├── asgi.py                   # ASGI configuration
│   ├── routing.py                # WebSocket routing
│   ├── settings.py               # Django settings
│   ├── urls.py                   # Main URLs
│   └── wsgi.py                   # WSGI configuration
├── venv/                         # Backend virtual environment
├── .env                          # Environment variables
├── .gitignore                    # Git ignore file
├── manage.py                     # Django management
└── requirements.txt              # Backend dependencies
```

## 🔧 Configuration

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key for security | Required |
| `DEBUG` | Enable debug mode | `False` |
| `DATABASE_URL` | Database connection string | SQLite |
| `REDIS_URL` | Redis server URL | `redis://localhost:6379` |
| `API_BASE_URL` | Backend API base URL | `http://localhost:8000` |

### Database Configuration
```python
# For PostgreSQL in production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'taskflow_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### API Testing
Use tools like Postman or curl to test API endpoints:
```bash
# Register user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

## 📊 API Documentation

### Authentication Endpoints
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Refresh JWT token

### Task Endpoints
- `GET /api/tasks/` - List all tasks
- `POST /api/tasks/` - Create new task
- `GET /api/tasks/{id}/` - Get specific task
- `PUT /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task

## 🎨 Screenshots

### Register
![image](https://github.com/user-attachments/assets/2e14462b-f0ed-4eb9-a16b-6a5568a315c0)

### Login
![Screenshot 2025-07-05 151518](https://github.com/user-attachments/assets/d9fb2d80-a885-4eba-ac0c-ffde299a00ee)


### Task form
![image](https://github.com/user-attachments/assets/e6dab259-b314-4943-964b-4b2936b04c40)


### Task Overview
![Screenshot 2025-07-05 150000](https://github.com/user-attachments/assets/902cf791-5fbd-487d-9a01-2b6fe52f00d5)

## 🔐 Security Features

- **Password Security**: Bcrypt hashing with salt
- **JWT Tokens**: Secure token-based authentication
- **CORS Protection**: Configured for specific origins
- **Input Validation**: Comprehensive data validation
- **Rate Limiting**: API rate limiting to prevent abuse
- **SQL Injection Protection**: Django ORM protection


### Railway
1. Connect GitHub repository
2. Configure environment variables
3. Deploy both backend and frontend services

## 📈 Performance Optimization

- **Database Indexing**: Optimized queries with proper indexes
- **Caching**: Redis caching for frequently accessed data
- **Lazy Loading**: Components loaded on demand
- **Asset Optimization**: Compressed static files
- **Database Connection Pooling**: Efficient database connections

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guide for Python code
- Write comprehensive tests for new features
- Update documentation for API changes
- Use meaningful commit messages

## 📋 Roadmap

### Version 2.0
- [ ] Mobile responsive design
- [ ] Push notifications
- [ ] Task categories and tags
- [ ] File attachments
- [ ] Team collaboration features

### Version 2.1
- [ ] Calendar integration
- [ ] Email reminders
- [ ] Task templates
- [ ] Advanced reporting
- [ ] API rate limiting dashboard

## 🐛 Known Issues

- Real-time updates may have slight delay on slower connections
- Large datasets (>1000 tasks) may impact frontend performance
- WebSocket connections require Redis in production


## 🙏 Acknowledgments

- Django REST Framework team for the excellent API framework
- Streamlit team for the intuitive frontend framework
- Plotly for beautiful visualizations
- Redis for real-time capabilities

---

**Made with ❤️ by [Abhay Tiwari]**

⭐ Star this repository if you find it helpful!
