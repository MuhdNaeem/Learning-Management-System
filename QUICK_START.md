# Quick Start Guide - Testing Your LMS

## Step 1: Activate Virtual Environment

```powershell
cd "C:\Users\M NAEEM\Desktop\Learning-Management-System"
.\venv\Scripts\Activate.ps1
```

## Step 2: Run Migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

## Step 3: Create Superuser (Optional but Recommended)

```powershell
python manage.py createsuperuser
```

## Step 4: Start Server

```powershell
python manage.py runserver
```

## Step 5: Open Browsable API

Open your browser and go to:
```
http://localhost:8000/api/
```

## Testing the API

### 1. Register a User
- Go to: `http://localhost:8000/api/users/`
- Click "POST" button
- Fill in the form:
  ```
  username: testuser
  email: test@example.com
  password: test123
  password_confirm: test123
  role: student
  ```
- Click "POST"
- **Save the access token from response!**

### 2. Login
- Go to: `http://localhost:8000/api/auth/login/`
- Click "POST"
- Enter username and password
- **Save the access token!**

### 3. Create Course (as Instructor)
- First register as instructor (role: instructor)
- Login to get instructor token
- Go to: `http://localhost:8000/api/courses/`
- Click "POST"
- In "Raw data" tab, enter:
  ```json
  {
    "title": "Test Course",
    "description": "My first course",
    "is_published": false
  }
  ```
- In "Headers" section, add:
  ```
  Authorization: Bearer <your_instructor_token>
  ```
- Click "POST"

### 4. Create Lecture
- Go to: `http://localhost:8000/api/lectures/`
- Click "POST"
- Enter:
  ```json
  {
    "course": 1,
    "title": "First Lecture",
    "youtube_video_id": "dQw4w9WgXcQ",
    "order": 1
  }
  ```
- Add Authorization header with instructor token
- Click "POST"

### 5. Enroll Student
- Go to: `http://localhost:8000/api/enrollments/`
- Click "POST"
- Enter:
  ```json
  {
    "user_id": 1,
    "course_id": 1
  }
  ```
- Add Authorization header with instructor token
- Click "POST"

### 6. Get Video URL (as Student)
- Login as student to get student token
- Go to: `http://localhost:8000/api/lectures/1/get_video_url/`
- Add Authorization header with student token
- Click "GET"
- You'll get the YouTube embed URL!

## Troubleshooting

### Database Error?
Make sure you've run migrations:
```powershell
python manage.py migrate
```

### Can't Access Endpoints?
Make sure you're logged in and have the Authorization header:
```
Authorization: Bearer <your_token>
```

### Video Not Playing?
- Make sure YouTube video is set to "Unlisted" (not Private)
- Check that video ID is correct
- Verify student is enrolled in the course

---

**Ready to test? Let's start!** 🚀

