# Configuration Guide

This document outlines the configuration required for the Learning Management System.

## Environment Variables

Create a `.env` file in the root directory with the following variables:

### Required Settings

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (Development - SQLite)
# For SQLite, leave DATABASE_ENGINE as sqlite3 or comment it out
DATABASE_ENGINE=sqlite3

# Database Configuration (PostgreSQL - Production)
# Uncomment and configure for PostgreSQL
# DATABASE_ENGINE=postgresql
# DB_NAME=lms_db
# DB_USER=postgres
# DB_PASSWORD=your-database-password
# DB_HOST=localhost
# DB_PORT=5432

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CORS_ALLOW_ALL_ORIGINS=False
```

### Production Settings (Optional - for production deployment)

```env
# Production Security Settings
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## Database Setup

### For Development (SQLite - Default)
No additional setup required. SQLite will be used automatically.

### For Production (PostgreSQL)
1. Install PostgreSQL on your server
2. Create a database named `lms_db` (or your preferred name)
3. Update the `.env` file with your PostgreSQL credentials
4. Set `DATABASE_ENGINE=postgresql` in your `.env` file

## Initial Setup Steps

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create and configure `.env` file:**
   - Copy the configuration above
   - Generate a secure SECRET_KEY (you can use Django's `get_random_secret_key()`)

3. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
- `POST /api/auth/login/` - Login and get JWT tokens
- `POST /api/auth/token/` - Get JWT token pair
- `POST /api/auth/token/refresh/` - Refresh access token
- `POST /api/auth/token/verify/` - Verify token

### Users
- `POST /api/users/` - Register new user
- `GET /api/users/me/` - Get current user profile
- `PUT /api/users/update_profile/` - Update current user profile

### Courses
- `GET /api/courses/` - List all courses (filtered by enrollment for students)
- `POST /api/courses/` - Create course (instructors only)
- `GET /api/courses/{id}/` - Get course details
- `GET /api/courses/{id}/lectures/` - Get course lectures

### Lectures
- `GET /api/lectures/` - List lectures
- `GET /api/lectures/{id}/` - Get lecture details
- `GET /api/lectures/{id}/get_video_url/` - Get signed video URL (placeholder)
- `GET /api/lectures/{id}/notes/` - Get lecture notes

### Enrollments
- `GET /api/enrollments/` - List enrollments
- `POST /api/enrollments/` - Enroll in a course
- `GET /api/enrollments/my_enrollments/` - Get current user's enrollments
- `POST /api/enrollments/{id}/unenroll/` - Unenroll from a course

## Next Steps

1. **AWS S3 Setup** (for video storage):
   - Create an S3 bucket
   - Set up CloudFront distribution
   - Configure AWS credentials
   - Implement signed URL generation in views

2. **Frontend Integration**:
   - Set up React frontend
   - Configure API base URL
   - Implement JWT token storage

3. **Testing**:
   - Write unit tests
   - Write integration tests
   - Test API endpoints
