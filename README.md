# TaskFlow - Modern Task Management Application

<div align="center">

![TaskFlow Logo](https://via.placeholder.com/150x150/6366f1/ffffff?text=TaskFlow)

**A professional, full-stack task management application built with Next.js and FastAPI**

[![Next.js](https://img.shields.io/badge/Next.js-16.1-black?style=flat-square&logo=next.js)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-19.2-61dafb?style=flat-square&logo=react)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue?style=flat-square&logo=typescript)](https://www.typescriptlang.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

[Features](#features) • [Demo](#demo) • [Installation](#installation) • [API Documentation](#api-documentation) • [Contributing](#contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Screenshots](#screenshots)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## 🌟 Overview

TaskFlow is a modern, full-stack task management application designed to help users organize their daily tasks efficiently. Built with cutting-edge technologies, it features a beautiful, responsive UI with smooth animations, real-time updates, and a robust backend API.

### Why TaskFlow?

- **Modern UI/UX**: Professional design with smooth animations and micro-interactions
- **Fully Responsive**: Works seamlessly on mobile, tablet, and desktop devices
- **Secure Authentication**: JWT-based authentication with refresh tokens
- **Real-time Updates**: Optimistic UI updates for instant feedback
- **Accessible**: WCAG AA compliant with keyboard navigation support
- **Type-Safe**: Full TypeScript implementation for better developer experience

---

## ✨ Features

### 🎨 User Interface
- **Professional Dashboard** with real-time statistics
- **Sidebar Navigation** with icons and smooth transitions
- **Stats Cards** showing Total Tasks, Completed, Pending, and Completion Rate
- **Filter Tabs** to organize tasks (All, Active, Completed)
- **Toast Notifications** for user feedback
- **Dark Mode Ready** (coming soon)

### 📝 Task Management
- **Create Tasks** with title and description
- **Edit Tasks** with pre-populated forms
- **Delete Tasks** with confirmation modal
- **Toggle Completion** with smooth animations
- **Filter Tasks** by status
- **Search Tasks** (coming soon)

### 🔐 Authentication & Security
- **User Registration** with email and password
- **Secure Login** with JWT tokens
- **Token Refresh** mechanism for extended sessions
- **Protected Routes** with automatic redirects
- **Password Validation** with strength indicators

### 📱 Responsive Design
- **Mobile-First** approach
- **Touch-Friendly** controls (44x44px minimum)
- **Collapsible Sidebar** on mobile devices
- **Adaptive Layouts** for all screen sizes

### ♿ Accessibility
- **WCAG AA Compliant** color contrast
- **Keyboard Navigation** support
- **Screen Reader Friendly** with ARIA labels
- **Focus Management** in modals and dropdowns

---

## 📸 Screenshots

### Dashboard
![Dashboard](https://via.placeholder.com/800x450/6366f1/ffffff?text=Dashboard+Screenshot)
*Main dashboard with stats cards and task list*

### Task Management
![Task Management](https://via.placeholder.com/800x450/6366f1/ffffff?text=Task+Management)
*Create and manage tasks with filters*

### Mobile View
![Mobile View](https://via.placeholder.com/400x700/6366f1/ffffff?text=Mobile+View)
*Responsive design on mobile devices*

### Authentication
![Authentication](https://via.placeholder.com/800x450/6366f1/ffffff?text=Authentication)
*Professional sign-in page with gradient background*

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: [Next.js 16.1](https://nextjs.org/) (App Router)
- **UI Library**: [React 19.2](https://reactjs.org/)
- **Language**: [TypeScript 5.x](https://www.typescriptlang.org/)
- **Styling**: [Tailwind CSS 4.x](https://tailwindcss.com/)
- **Icons**: [Lucide React](https://lucide.dev/)
- **UI Components**: [Headless UI](https://headlessui.com/)
- **HTTP Client**: [Axios](https://axios-http.com/)
- **Font Optimization**: [next/font/google](https://nextjs.org/docs/app/building-your-application/optimizing/fonts)

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Language**: Python 3.10+
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) / [SQLModel](https://sqlmodel.tiangolo.com/)
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: [bcrypt](https://github.com/pyca/bcrypt/)
- **Validation**: [Pydantic](https://pydantic-docs.helpmanual.io/)

### Development Tools
- **Build Tool**: [Turbopack](https://turbo.build/pack)
- **Linting**: ESLint
- **Formatting**: Prettier
- **Version Control**: Git

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** 18.x or higher ([Download](https://nodejs.org/))
- **npm** or **yarn** package manager
- **Python** 3.10 or higher ([Download](https://www.python.org/))
- **PostgreSQL** 14.x or higher ([Download](https://www.postgresql.org/download/))
- **Git** ([Download](https://git-scm.com/))

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/taskflow.git
cd taskflow
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Setup PostgreSQL Database

```bash
# Create database
createdb taskflow_db

# Or using psql:
psql -U postgres
CREATE DATABASE taskflow_db;
\q
```

#### Configure Backend Environment

Create a `.env` file in the `backend/` directory:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost:5432/taskflow_db

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# Server Configuration
HOST=0.0.0.0
PORT=8001
```

**⚠️ Important**: Change `SECRET_KEY` to a secure random string in production!

Generate a secure secret key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### Run Database Migrations

```bash
# Initialize database tables
python -m app.db.init_db

# Or if using Alembic:
alembic upgrade head
```

### 3. Frontend Setup

#### Install Node Dependencies

```bash
cd ../frontend

# Install dependencies
npm install
# or
yarn install
```

#### Configure Frontend Environment

Create a `.env.local` file in the `frontend/` directory:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8001

# Optional: Analytics, etc.
# NEXT_PUBLIC_GA_ID=your-google-analytics-id
```

---

## ⚙️ Configuration

### Backend Configuration Options

Edit `backend/.env` to customize:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://...` |
| `SECRET_KEY` | JWT secret key | *Required* |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime | `15` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token lifetime | `7` |
| `ALLOWED_ORIGINS` | CORS allowed origins | `http://localhost:3000` |

### Frontend Configuration Options

Edit `frontend/.env.local` to customize:

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8001` |

---

## 🏃 Running the Application

### Development Mode

#### Start Backend Server

```bash
cd backend

# Activate virtual environment (if not already activated)
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Start FastAPI server with hot reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

Backend will be available at: **http://localhost:8001**

API Documentation: **http://localhost:8001/docs** (Swagger UI)

#### Start Frontend Server

```bash
cd frontend

# Start Next.js development server
npm run dev
# or
yarn dev
```

Frontend will be available at: **http://localhost:3000**

### Production Mode

#### Build Backend

```bash
cd backend

# Install production dependencies only
pip install -r requirements.txt --no-dev

# Run with production server (Gunicorn)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001
```

#### Build Frontend

```bash
cd frontend

# Build for production
npm run build

# Start production server
npm start
```

### Using Docker (Optional)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in detached mode
docker-compose up -d

# Stop containers
docker-compose down
```

---

## 📚 API Documentation

### Base URL

```
http://localhost:8001/api
```

### Authentication Endpoints

#### Register User

```http
POST /api/auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "John Doe"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

#### Login

```http
POST /api/auth/signin
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

#### Refresh Token

```http
POST /api/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Task Endpoints

All task endpoints require authentication. Include the access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

#### Get All Tasks

```http
GET /api/tasks
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Complete project documentation",
    "description": "Write comprehensive README",
    "completed": false,
    "user_id": 1,
    "created_at": "2026-01-25T10:00:00Z",
    "updated_at": "2026-01-25T10:00:00Z"
  }
]
```

#### Create Task

```http
POST /api/tasks
Content-Type: application/json

{
  "title": "New task",
  "description": "Task description (optional)"
}
```

#### Update Task

```http
PUT /api/tasks/{task_id}
Content-Type: application/json

{
  "title": "Updated task title",
  "description": "Updated description"
}
```

#### Delete Task

```http
DELETE /api/tasks/{task_id}
```

#### Toggle Task Completion

```http
PATCH /api/tasks/{task_id}/toggle
```

### Interactive API Documentation

Visit **http://localhost:8001/docs** for interactive Swagger UI documentation with the ability to test endpoints directly.

---

## 📁 Project Structure

```
taskflow/
├── frontend/                    # Next.js frontend application
│   ├── app/                    # Next.js App Router
│   │   ├── (auth)/            # Authentication pages
│   │   │   ├── signin/
│   │   │   └── signup/
│   │   ├── dashboard/         # Protected dashboard
│   │   ├── layout.tsx         # Root layout
│   │   └── globals.css        # Global styles
│   ├── components/            # React components
│   │   ├── layout/           # Layout components (Sidebar, Navbar)
│   │   ├── dashboard/        # Dashboard components (StatsCard)
│   │   ├── tasks/            # Task components
│   │   ├── auth/             # Auth components
│   │   └── ui/               # Reusable UI components
│   ├── contexts/             # React contexts
│   ├── lib/                  # Utilities and helpers
│   │   ├── api/             # API client
│   │   ├── hooks/           # Custom React hooks
│   │   └── utils/           # Utility functions
│   ├── types/               # TypeScript type definitions
│   ├── public/              # Static assets
│   ├── .env.local           # Environment variables (not in git)
│   ├── package.json         # Dependencies
│   └── tsconfig.json        # TypeScript config
│
├── backend/                    # FastAPI backend application
│   ├── app/
│   │   ├── api/              # API routes
│   │   │   ├── auth.py      # Authentication endpoints
│   │   │   └── tasks.py     # Task endpoints
│   │   ├── core/             # Core functionality
│   │   │   ├── config.py    # Configuration
│   │   │   └── security.py  # Security utilities
│   │   ├── db/               # Database
│   │   │   ├── base.py      # Database base
│   │   │   └── session.py   # Database session
│   │   ├── models/           # SQLAlchemy models
│   │   │   ├── user.py      # User model
│   │   │   └── task.py      # Task model
│   │   ├── schemas/          # Pydantic schemas
│   │   └── main.py           # FastAPI app entry point
│   ├── tests/                # Backend tests
│   ├── .env                  # Environment variables (not in git)
│   ├── requirements.txt      # Python dependencies
│   └── alembic.ini          # Database migrations config
│
├── .gitignore               # Git ignore rules
├── README.md                # This file
├── LICENSE                  # MIT License
└── docker-compose.yml       # Docker configuration (optional)
```

---

## 🤝 Contributing

We welcome contributions to TaskFlow! Here's how you can help:

### Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/yourusername/taskflow.git
   ```
3. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
4. **Make your changes**
5. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
6. **Push to your branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Contribution Guidelines

- **Code Style**: Follow existing code style and conventions
- **TypeScript**: Use strict TypeScript types
- **Comments**: Add comments for complex logic
- **Testing**: Add tests for new features
- **Documentation**: Update README if needed
- **Commits**: Write clear, descriptive commit messages

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Environment details (OS, browser, versions)

### Feature Requests

We love new ideas! Create an issue with:
- Clear description of the feature
- Use cases and benefits
- Possible implementation approach

---

## 🧪 Testing

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run tests with coverage
npm run test:coverage

# Run tests in watch mode
npm run test:watch
```

### Backend Tests

```bash
cd backend

# Run tests
pytest

# Run tests with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py
```

---

## 🚢 Deployment

### Frontend Deployment (Vercel)

1. Push your code to GitHub
2. Import project in [Vercel](https://vercel.com)
3. Set environment variables:
   - `NEXT_PUBLIC_API_URL`
4. Deploy

### Backend Deployment (Railway/Render)

1. Push your code to GitHub
2. Create new project in [Railway](https://railway.app) or [Render](https://render.com)
3. Set environment variables (all from `.env`)
4. Deploy

### Docker Deployment

```bash
# Build images
docker-compose build

# Run containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

---

## 🔒 Security Best Practices

### Environment Variables
- ✅ **Never commit** `.env` files to Git
- ✅ Use different secrets for development and production
- ✅ Rotate secrets regularly
- ✅ Use strong, random secret keys

### Authentication
- ✅ Use HTTPS in production
- ✅ Implement rate limiting
- ✅ Use secure password hashing (bcrypt)
- ✅ Implement token refresh mechanism
- ✅ Set appropriate token expiration times

### Database
- ✅ Use parameterized queries (SQLAlchemy handles this)
- ✅ Implement proper user isolation
- ✅ Regular backups
- ✅ Use connection pooling

### API Security
- ✅ Validate all inputs
- ✅ Implement CORS properly
- ✅ Use rate limiting
- ✅ Sanitize error messages (don't expose internals)

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 TaskFlow Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- [Next.js](https://nextjs.org/) - The React Framework
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework
- [Lucide](https://lucide.dev/) - Beautiful icon library
- [Headless UI](https://headlessui.com/) - Unstyled, accessible UI components

---

## 📞 Support

- **Documentation**: [Read the docs](https://github.com/yourusername/taskflow/wiki)
- **Issues**: [Report a bug](https://github.com/yourusername/taskflow/issues)
- **Discussions**: [Join the discussion](https://github.com/yourusername/taskflow/discussions)
- **Email**: support@taskflow.com

---

## 🗺️ Roadmap

- [ ] Dark mode support
- [ ] Task priorities (High, Medium, Low)
- [ ] Due dates and reminders
- [ ] Task categories/tags
- [ ] Search and advanced filtering
- [ ] Drag-and-drop task reordering
- [ ] Task sharing and collaboration
- [ ] Mobile app (React Native)
- [ ] Desktop app (Electron)
- [ ] Email notifications
- [ ] Task comments
- [ ] File attachments
- [ ] Statistics and analytics dashboard

---

<div align="center">

**Made with ❤️ Muhammad Muneeb Khan**

[⬆ Back to Top](#taskflow---modern-task-management-application)

</div>
