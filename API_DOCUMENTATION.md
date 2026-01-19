# LMS API Documentation

## Overview

This Learning Management System (LMS) provides secure access to course content through YouTube videos. All video access is protected by authentication and enrollment checks. Videos should be uploaded as "Unlisted" on YouTube, and the backend controls who can access the embed URLs.

## Base URL

```
http://localhost:8000/api/
```

## Authentication

All endpoints (except registration and login) require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Authentication Endpoints

#### Register User
```http
POST /api/users/
Content-Type: application/json

{
  "username": "student1",
  "email": "student1@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "student"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "username": "student1",
    "email": "student1@example.com",
    "role": "student"
  },
  "tokens": {
    "refresh": "...",
    "access": "..."
  }
}
```

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "student1",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "username": "student1",
    "email": "student1@example.com",
    "role": "student"
  },
  "tokens": {
    "refresh": "...",
    "access": "..."
  }
}
```

#### Refresh Token
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "<refresh_token>"
}
```

## Course Endpoints

### List Courses
```http
GET /api/courses/
Authorization: Bearer <token>
```

**Response:**
- **Students**: Only see published courses they're enrolled in
- **Instructors/Admins**: See all courses

### Get Course Details
```http
GET /api/courses/{id}/
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "title": "Introduction to Python",
  "description": "Learn Python basics",
  "instructor": 2,
  "instructor_name": "Dr. Smith",
  "is_published": true,
  "lecture_count": 5,
  "lectures": [
    {
      "id": 1,
      "title": "Python Basics",
      "description": "...",
      "youtube_video_id": "dQw4w9WgXcQ",
      "order": 1,
      "duration_minutes": 30
    }
  ],
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Create Course (Instructor/Admin only)
```http
POST /api/courses/
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Advanced Python",
  "description": "Advanced Python concepts",
  "is_published": false
}
```

### Update Course (Course Instructor only)
```http
PATCH /api/courses/{id}/
Authorization: Bearer <token>
Content-Type: application/json

{
  "is_published": true
}
```

### Get Course Lectures
```http
GET /api/courses/{id}/lectures/
Authorization: Bearer <token>
```

## Lecture Endpoints

### List Lectures
```http
GET /api/lectures/?course_id=1
Authorization: Bearer <token>
```

**Response:**
- **Students**: Only see lectures from enrolled courses
- **Instructors/Admins**: See all lectures

### Get Lecture Details
```http
GET /api/lectures/{id}/
Authorization: Bearer <token>
```

### Create Lecture (Instructor/Admin only)
```http
POST /api/lectures/
Authorization: Bearer <token>
Content-Type: application/json

{
  "course": 1,
  "title": "Python Variables",
  "description": "Understanding variables in Python",
  "youtube_video_id": "dQw4w9WgXcQ",
  "order": 1,
  "duration_minutes": 25
}
```

### Get Video Embed URL ⭐ CRITICAL ENDPOINT
```http
GET /api/lectures/{id}/get_video_url/
Authorization: Bearer <token>
```

**Query Parameters:**
- `autoplay` (optional): Set to "true" to autoplay video. Default: false
- `controls` (optional): Set to "false" to hide controls. Default: true

**Response:**
```json
{
  "lecture_id": 1,
  "lecture_title": "Python Variables",
  "youtube_video_id": "dQw4w9WgXcQ",
  "embed_url": "https://www.youtube.com/embed/dQw4w9WgXcQ?modestbranding=1&rel=0",
  "watch_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "message": "Use embed_url in an iframe to display the video. Access is controlled by enrollment."
}
```

**Security:**
- ✅ Only enrolled students and course instructors can access
- ✅ Videos should be uploaded as "Unlisted" on YouTube (not searchable)
- ✅ Backend controls who can access the embed URL
- ✅ Use embed_url in an iframe to display videos securely

### Get Lecture Notes
```http
GET /api/lectures/{id}/notes/
Authorization: Bearer <token>
```

## Note Endpoints

### List Notes
```http
GET /api/notes/?lecture_id=1
Authorization: Bearer <token>
```

### Get Note Details
```http
GET /api/notes/{id}/
Authorization: Bearer <token>
```

### Create Note (Instructor/Admin only)
```http
POST /api/notes/
Authorization: Bearer <token>
Content-Type: application/json

{
  "lecture": 1,
  "title": "Python Variables Notes",
  "file_url": "https://drive.google.com/file/d/.../view?usp=sharing",
  "file_type": "pdf"
}
```

**Note:** For Google Drive links, use the sharing link format. For Dropbox, use the direct link format.

### Get Note File URL ⭐ CRITICAL ENDPOINT
```http
GET /api/notes/{id}/get_file_url/
Authorization: Bearer <token>
```

**Response:**
```json
{
  "note_id": 1,
  "note_title": "Python Variables Notes",
  "file_type": "pdf",
  "file_url": "https://drive.google.com/file/d/.../view?usp=sharing",
  "message": "Access is controlled by enrollment. Use this URL to access the file."
}
```

## Enrollment Endpoints

### List Enrollments
```http
GET /api/enrollments/
Authorization: Bearer <token>
```

**Response:**
- **Students**: Only see their own enrollments
- **Instructors/Admins**: See all enrollments

### Create Enrollment (Instructor/Admin only)
```http
POST /api/enrollments/
Authorization: Bearer <token>
Content-Type: application/json

{
  "user_id": 1,  // Optional: defaults to requesting user
  "course_id": 1
}
```

**Note:** Only instructors and admins can create enrollments. They can enroll any user by providing `user_id`, or themselves if omitted.

### Get My Enrollments
```http
GET /api/enrollments/my_enrollments/
Authorization: Bearer <token>
```

### Unenroll
```http
POST /api/enrollments/{id}/unenroll/
Authorization: Bearer <token>
```

## User Endpoints

### Get Current User Profile
```http
GET /api/users/me/
Authorization: Bearer <token>
```

### Update Profile
```http
PATCH /api/users/update_profile/
Authorization: Bearer <token>
Content-Type: application/json

{
  "first_name": "Jane",
  "last_name": "Smith"
}
```

## Permission Rules

| Action | Allowed Roles |
|--------|--------------|
| Create course | Instructor, Admin |
| Upload lecture | Instructor, Admin |
| Enroll student | Instructor, Admin |
| Access lecture video | Enrolled Student, Instructor, Admin |
| Access notes | Enrolled Student, Instructor, Admin |
| View courses | Enrolled Student (published only), Instructor, Admin |

## Security Features

### 1. JWT Authentication
- All endpoints require valid JWT tokens
- Tokens expire after 1 hour (configurable)
- Refresh tokens available for seamless re-authentication

### 2. Enrollment-Based Access
- Students can only access courses they're enrolled in
- Enrollment checks happen at the database level
- Permission classes enforce access control

### 3. YouTube Video Access
- Videos uploaded as "Unlisted" on YouTube (not searchable)
- Backend controls who can access embed URLs through enrollment
- Only enrolled students and instructors can get embed URLs
- Videos are embedded securely using YouTube iframe API

### 4. Role-Based Access Control
- Three roles: Student, Instructor, Admin
- Permissions enforced at view and object levels
- Custom permission classes for fine-grained control

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "error": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "error": "YouTube video ID not found for this lecture."
}
```

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**
   Copy `env.example` to `.env` and fill in your values:
   ```bash
   cp env.example .env
   ```

3. **Upload Videos to YouTube**
   - Upload your videos to YouTube
   - Set videos to "Unlisted" (not Public or Private)
   - Copy the video ID from the YouTube URL (e.g., "dQw4w9WgXcQ" from https://www.youtube.com/watch?v=dQw4w9WgXcQ)
   - Use these video IDs when creating lectures in the LMS

4. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Server**
   ```bash
   python manage.py runserver
   ```

## Testing the API

### Example: Student Flow

1. **Register/Login**
   ```bash
   curl -X POST http://localhost:8000/api/auth/login/ \
     -H "Content-Type: application/json" \
     -d '{"username": "student1", "password": "password123"}'
   ```

2. **Get Courses** (will be empty until enrolled)
   ```bash
   curl http://localhost:8000/api/courses/ \
     -H "Authorization: Bearer <access_token>"
   ```

3. **Instructor enrolls student** (requires instructor token)
   ```bash
   curl -X POST http://localhost:8000/api/enrollments/ \
     -H "Authorization: Bearer <instructor_token>" \
     -H "Content-Type: application/json" \
     -d '{"user_id": 1, "course_id": 1}'
   ```

4. **Get Video Embed URL**
   ```bash
   curl http://localhost:8000/api/lectures/1/get_video_url/ \
     -H "Authorization: Bearer <access_token>"
   ```

5. **Use the embed URL** in an iframe in your frontend:
   ```html
   <iframe src="<embed_url_from_response>" width="560" height="315" frameborder="0" allowfullscreen></iframe>
   ```

## Important Notes

⚠️ **Upload videos as "Unlisted"** - Videos should be set to "Unlisted" on YouTube (not Public or Private)

⚠️ **Backend controls access** - Only enrolled students can get embed URLs

⚠️ **Use embed URLs in iframes** - Frontend should use the embed_url in an iframe to display videos

⚠️ **Enrollment required** - Students must be enrolled before accessing content

⚠️ **File URLs** - Notes can use Google Drive, Dropbox, or any public URL

