# Complete LMS User Guide - Everything You Need to Know

## 📚 Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Explained](#architecture-explained)
3. [How Authentication Works](#how-authentication-works)
4. [How Enrollment Works](#how-enrollment-works)
5. [How Video Access Works](#how-video-access-works)
6. [Step-by-Step Usage Guide](#step-by-step-usage-guide)
7. [Testing with Browsable API](#testing-with-browsable-api)

---

## 🎯 System Overview

### What is This LMS?
A Learning Management System that:
- ✅ Manages courses, lectures, and students
- ✅ Controls access through enrollment
- ✅ Uses YouTube for free video hosting
- ✅ Secures content with JWT authentication
- ✅ Prevents unauthorized access

### Key Concepts

**Roles:**
- **Student**: Can view enrolled courses and watch videos
- **Instructor**: Can create courses, upload lectures, enroll students
- **Admin**: Can do everything (like instructor + manage users)

**Core Entities:**
1. **Course**: A collection of lectures (e.g., "Python Basics")
2. **Lecture**: A single video lesson in a course
3. **Enrollment**: Links a student to a course (required for access)
4. **Note**: PDFs or files attached to lectures

---

## 🏗️ Architecture Explained

### How the System Works

```
┌─────────────┐
│   Student   │
│  (Browser)  │
└──────┬──────┘
       │
       │ 1. Login → Get JWT Token
       ▼
┌─────────────────────────────────┐
│      Django Backend API         │
│  ┌──────────────────────────┐  │
│  │  Authentication Layer     │  │
│  │  (JWT Token Validation)  │  │
│  └──────────────────────────┘  │
│  ┌──────────────────────────┐  │
│  │  Permission Layer        │  │
│  │  (Check Enrollment)      │  │
│  └──────────────────────────┘  │
│  ┌──────────────────────────┐  │
│  │  Business Logic          │  │
│  │  (Generate YouTube URL)  │  │
│  └──────────────────────────┘  │
└──────┬──────────────────────────┘
       │
       │ 2. Return YouTube Embed URL
       ▼
┌─────────────┐
│  YouTube    │
│  (Unlisted) │
└─────────────┘
```

### File Structure Explained

```
Learning-Management-System/
│
├── accounts/              # User management
│   ├── models.py         # User model (Student/Instructor/Admin)
│   ├── views.py          # User registration, login, profile
│   └── serializers.py    # Data formatting for API
│
├── courses/              # Course management
│   ├── models.py        # Course, Lecture, Note models
│   ├── views.py         # CRUD operations + video URL endpoint
│   └── serializers.py   # Data formatting
│
├── enrollments/          # Enrollment management
│   ├── models.py       # Enrollment model (links User to Course)
│   ├── views.py        # Create/list enrollments
│   └── serializers.py  # Data formatting
│
├── permissions/         # Access control
│   └── permissions.py  # Custom permission classes
│
├── core/                # Shared utilities
│   └── services.py     # YouTube service (generates embed URLs)
│
└── config/              # Django configuration
    ├── settings/       # Settings files
    └── urls.py         # URL routing
```

---

## 🔐 How Authentication Works

### JWT (JSON Web Token) Explained

**What is JWT?**
- A secure way to identify users
- Token contains user info (ID, role, etc.)
- Expires after 1 hour (configurable)

**Flow:**
```
1. User logs in → Gets access_token + refresh_token
2. User includes token in every request: Authorization: Bearer <token>
3. Backend validates token → Allows/denies access
4. Token expires → Use refresh_token to get new access_token
```

### Authentication Endpoints

**1. Register (Create Account)**
```
POST /api/users/
Body: {
  "username": "student1",
  "email": "student1@example.com",
  "password": "password123",
  "password_confirm": "password123",
  "role": "student"
}
Response: { user data + tokens }
```

**2. Login**
```
POST /api/auth/login/
Body: {
  "username": "student1",
  "password": "password123"
}
Response: { user data + tokens }
```

**3. Refresh Token (Get New Access Token)**
```
POST /api/auth/token/refresh/
Body: {
  "refresh": "<refresh_token>"
}
Response: { "access": "<new_access_token>" }
```

---

## 👥 How Enrollment Works

### Why Enrollment?
- Students can ONLY access courses they're enrolled in
- Enrollment = Permission to view course content
- Only instructors/admins can create enrollments

### Enrollment Flow

```
1. Instructor creates course
2. Instructor enrolls student(s) in course
3. Student can now see course in their list
4. Student can access lectures and videos
```

### Enrollment Endpoints

**Create Enrollment (Instructor/Admin only)**
```
POST /api/enrollments/
Headers: Authorization: Bearer <instructor_token>
Body: {
  "user_id": 1,        // Student ID (optional, defaults to yourself)
  "course_id": 1       // Course ID
}
```

**List My Enrollments**
```
GET /api/enrollments/my_enrollments/
Headers: Authorization: Bearer <token>
Response: [ List of enrolled courses ]
```

---

## 🎥 How Video Access Works

### YouTube Integration Explained

**Why YouTube?**
- ✅ Free hosting (no AWS S3 costs)
- ✅ Global CDN (fast delivery)
- ✅ Easy upload process

**How Security Works:**
1. Videos uploaded as "Unlisted" (not searchable)
2. Backend checks enrollment before giving embed URL
3. Only enrolled students get the embed URL
4. Frontend displays video in iframe

### Video Access Flow

```
1. Student requests video URL
   GET /api/lectures/1/get_video_url/
   
2. Backend checks:
   - Is user authenticated? ✅
   - Is user enrolled in course? ✅
   
3. Backend generates YouTube embed URL
   Response: {
     "embed_url": "https://www.youtube.com/embed/VIDEO_ID"
   }
   
4. Frontend displays in iframe
   <iframe src="embed_url" />
```

### Video Endpoints

**Get Video Embed URL**
```
GET /api/lectures/{lecture_id}/get_video_url/
Headers: Authorization: Bearer <token>
Response: {
  "embed_url": "https://www.youtube.com/embed/...",
  "watch_url": "https://www.youtube.com/watch?v=...",
  "youtube_video_id": "dQw4w9WgXcQ"
}
```

---

## 📝 Step-by-Step Usage Guide

### Scenario: Complete Course Creation Flow

#### Step 1: Create Users

**Create Instructor:**
```json
POST /api/users/
{
  "username": "instructor1",
  "email": "instructor@example.com",
  "password": "instructor123",
  "password_confirm": "instructor123",
  "role": "instructor"
}
```

**Create Student:**
```json
POST /api/users/
{
  "username": "student1",
  "email": "student@example.com",
  "password": "student123",
  "password_confirm": "student123",
  "role": "student"
}
```

#### Step 2: Login as Instructor

```json
POST /api/auth/login/
{
  "username": "instructor1",
  "password": "instructor123"
}
```

**Save the `access` token!**

#### Step 3: Upload Video to YouTube

1. Go to YouTube Studio
2. Click "Create" → "Upload video"
3. Upload your video
4. Set visibility to **"Unlisted"**
5. Copy video ID from URL:
   - URL: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
   - Video ID: `dQw4w9WgXcQ`

#### Step 4: Create Course

```json
POST /api/courses/
Headers: Authorization: Bearer <instructor_token>
{
  "title": "Python Basics",
  "description": "Learn Python from scratch",
  "is_published": false
}
```

**Save the course ID from response!**

#### Step 5: Create Lecture

```json
POST /api/lectures/
Headers: Authorization: Bearer <instructor_token>
{
  "course": 1,
  "title": "Introduction to Python",
  "description": "First lesson",
  "youtube_video_id": "dQw4w9WgXcQ",
  "order": 1,
  "duration_minutes": 30
}
```

#### Step 6: Publish Course

```json
PATCH /api/courses/1/
Headers: Authorization: Bearer <instructor_token>
{
  "is_published": true
}
```

#### Step 7: Enroll Student

```json
POST /api/enrollments/
Headers: Authorization: Bearer <instructor_token>
{
  "user_id": 2,  // Student ID
  "course_id": 1
}
```

#### Step 8: Student Accesses Video

**Student logs in:**
```json
POST /api/auth/login/
{
  "username": "student1",
  "password": "student123"
}
```

**Student gets video URL:**
```json
GET /api/lectures/1/get_video_url/
Headers: Authorization: Bearer <student_token>
```

**Response:**
```json
{
  "embed_url": "https://www.youtube.com/embed/dQw4w9WgXcQ?modestbranding=1&rel=0",
  "watch_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

---

## 🧪 Testing with Browsable API

### What is Browsable API?
- Django REST Framework's built-in web interface
- Test APIs directly in browser (no Postman needed!)
- Available at: `http://localhost:8000/api/`

### How to Use Browsable API

1. **Start Server:**
   ```bash
   python manage.py runserver
   ```

2. **Open Browser:**
   Go to: `http://localhost:8000/api/`

3. **You'll see:**
   - List of available endpoints
   - Can click to explore each endpoint
   - Can test POST/PUT/DELETE directly

### Step-by-Step Testing Guide

#### Test 1: Register User

1. Go to: `http://localhost:8000/api/users/`
2. Click "POST" button
3. Fill in form:
   ```
   username: student1
   email: student1@test.com
   password: test123
   password_confirm: test123
   role: student
   ```
4. Click "POST"
5. See response with tokens!

#### Test 2: Login

1. Go to: `http://localhost:8000/api/auth/login/`
2. Click "POST"
3. Fill in:
   ```
   username: student1
   password: test123
   ```
4. Click "POST"
5. Copy the `access` token!

#### Test 3: Create Course (as Instructor)

1. First, register as instructor:
   - Go to `/api/users/`
   - Create user with `role: instructor`
   - Login to get instructor token

2. Go to: `http://localhost:8000/api/courses/`
3. Click "POST"
4. In "Raw data" tab, enter:
   ```json
   {
     "title": "My First Course",
     "description": "Test course",
     "is_published": false
   }
   ```
5. In "Headers" section, add:
   ```
   Authorization: Bearer <instructor_token>
   ```
6. Click "POST"
7. See created course!

#### Test 4: Get Video URL

1. First create a lecture with YouTube video ID
2. Go to: `http://localhost:8000/api/lectures/1/get_video_url/`
3. Add header: `Authorization: Bearer <token>`
4. Click "GET"
5. See embed URL!

---

## 🔍 Understanding API Responses

### Common Response Formats

**Success (200 OK):**
```json
{
  "id": 1,
  "title": "Course Title",
  ...
}
```

**Created (201 Created):**
```json
{
  "id": 1,
  "title": "New Course",
  ...
}
```

**Error (400 Bad Request):**
```json
{
  "error": "Invalid data",
  "field_name": ["Error message"]
}
```

**Unauthorized (401):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Forbidden (403):**
```json
{
  "error": "You do not have permission to perform this action."
}
```

---

## 🎓 Quick Reference

### Most Common Operations

**1. Register & Login:**
```
POST /api/users/ → Register
POST /api/auth/login/ → Login (get token)
```

**2. Create Course (Instructor):**
```
POST /api/courses/ → Create course
POST /api/lectures/ → Add lecture
```

**3. Enroll Student (Instructor):**
```
POST /api/enrollments/ → Enroll student
```

**4. Access Content (Student):**
```
GET /api/courses/ → List enrolled courses
GET /api/lectures/{id}/get_video_url/ → Get video URL
```

---

## 🚨 Common Issues & Solutions

### Issue: "Authentication credentials not provided"
**Solution:** Add header: `Authorization: Bearer <token>`

### Issue: "You do not have permission"
**Solution:** Check your role (instructor/admin needed for some actions)

### Issue: "Course not found" when accessing lecture
**Solution:** Make sure student is enrolled in the course

### Issue: Video not playing
**Solution:** 
- Check YouTube video is "Unlisted" (not Private)
- Verify video ID is correct
- Make sure you're using embed_url in iframe

---

## 📚 Next Steps

1. ✅ Run migrations
2. ✅ Create test users
3. ✅ Upload test video to YouTube
4. ✅ Create test course
5. ✅ Test enrollment
6. ✅ Test video access

**Ready to test? Let's start the server!** 🚀

