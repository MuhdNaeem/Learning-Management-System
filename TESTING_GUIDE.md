# Complete Testing Guide - Step by Step

## 🎯 What You Need to Know

### System Overview
Your LMS has:
- **3 Roles**: Student, Instructor, Admin
- **Courses**: Collections of lectures
- **Lectures**: YouTube videos with access control
- **Enrollments**: Links students to courses
- **Notes**: PDFs/files attached to lectures

### How Security Works
1. Users must **login** to get JWT token
2. Students must be **enrolled** in course to access content
3. Videos are on YouTube (set to "Unlisted")
4. Backend controls who gets the embed URL

---

## 🚀 Step-by-Step Testing

### Step 1: Start the Server

The server should be running at: `http://localhost:8000`

If not, run:
```powershell
cd "C:\Users\M NAEEM\Desktop\Learning-Management-System"
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

### Step 2: Open Browsable API

Open browser: `http://localhost:8000/api/`

You'll see a list of available endpoints!

---

## 📝 Test Scenario: Complete Flow

### Test 1: Register an Instructor

1. Go to: `http://localhost:8000/api/users/`
2. Click **"POST"** button (top right)
3. You'll see a form - fill it:
   ```
   Content type: application/json
   
   Raw data:
   {
     "username": "instructor1",
     "email": "instructor@test.com",
     "password": "test123",
     "password_confirm": "test123",
     "role": "instructor"
   }
   ```
4. Click **"POST"** button at bottom
5. **IMPORTANT**: Copy the `access` token from response!
   ```json
   {
     "tokens": {
       "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",  ← COPY THIS!
       "refresh": "..."
     }
   }
   ```

### Test 2: Register a Student

1. Same endpoint: `http://localhost:8000/api/users/`
2. Click **"POST"**
3. Fill form:
   ```json
   {
     "username": "student1",
     "email": "student@test.com",
     "password": "test123",
     "password_confirm": "test123",
     "role": "student"
   }
   ```
4. Click **"POST"**
5. Note the user ID from response (you'll need it later)

### Test 3: Login as Instructor

1. Go to: `http://localhost:8000/api/auth/login/`
2. Click **"POST"**
3. Fill form:
   ```json
   {
     "username": "instructor1",
     "password": "test123"
   }
   ```
4. Click **"POST"**
5. **Copy the `access` token!**

### Test 4: Create a Course

1. Go to: `http://localhost:8000/api/courses/`
2. Click **"POST"**
3. In the form, you'll see:
   - **Content type**: Keep as `application/json`
   - **Raw data** tab: Enter:
     ```json
     {
       "title": "Python Basics",
       "description": "Learn Python from scratch",
       "is_published": false
     }
     ```
   - **Headers** section: Click to expand
     - Add header:
       ```
       Authorization: Bearer <paste_your_instructor_token_here>
       ```
4. Click **"POST"**
5. **Save the course ID** from response (usually `"id": 1`)

### Test 5: Create a Lecture

**First, upload a video to YouTube:**
1. Go to YouTube Studio
2. Upload a test video
3. Set visibility to **"Unlisted"**
4. Copy the video ID from URL:
   - URL: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
   - Video ID: `dQw4w9WgXcQ`

**Then create lecture:**
1. Go to: `http://localhost:8000/api/lectures/`
2. Click **"POST"**
3. Fill form:
   ```json
   {
     "course": 1,
     "title": "Introduction to Python",
     "description": "First lesson",
     "youtube_video_id": "dQw4w9WgXcQ",
     "order": 1,
     "duration_minutes": 30
   }
   ```
4. Add Authorization header with instructor token
5. Click **"POST"**
6. **Save the lecture ID** (usually `"id": 1`)

### Test 6: Publish the Course

1. Go to: `http://localhost:8000/api/courses/1/` (use your course ID)
2. Click **"PATCH"** button
3. Enter:
   ```json
   {
     "is_published": true
   }
   ```
4. Add Authorization header
5. Click **"PATCH"**

### Test 7: Enroll Student

1. Go to: `http://localhost:8000/api/enrollments/`
2. Click **"POST"**
3. Enter:
   ```json
   {
     "user_id": 2,  // Student's user ID (from Test 2)
     "course_id": 1
   }
   ```
4. Add Authorization header with instructor token
5. Click **"POST"**

### Test 8: Login as Student

1. Go to: `http://localhost:8000/api/auth/login/`
2. Login with student credentials:
   ```json
   {
     "username": "student1",
     "password": "test123"
   }
   ```
3. **Copy the student's access token!**

### Test 9: Student Views Courses

1. Go to: `http://localhost:8000/api/courses/`
2. Add Authorization header with student token
3. Click **"GET"**
4. You should see the course you created!

### Test 10: Student Gets Video URL ⭐

1. Go to: `http://localhost:8000/api/lectures/1/get_video_url/`
   (Use your lecture ID)
2. Add Authorization header with student token
3. Click **"GET"**
4. Response will be:
   ```json
   {
     "lecture_id": 1,
     "lecture_title": "Introduction to Python",
     "youtube_video_id": "dQw4w9WgXcQ",
     "embed_url": "https://www.youtube.com/embed/dQw4w9WgXcQ?modestbranding=1&rel=0",
     "watch_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
   }
   ```
5. Copy the `embed_url`
6. Test it: Create an HTML file:
   ```html
   <!DOCTYPE html>
   <html>
   <body>
     <h1>Test Video</h1>
     <iframe 
       src="<paste_embed_url_here>" 
       width="560" 
       height="315" 
       frameborder="0" 
       allowfullscreen>
     </iframe>
   </body>
   </html>
   ```
7. Open in browser - video should play! 🎉

---

## 🔍 Understanding the Browsable API

### How to Use It

1. **GET requests**: Just click "GET" button
2. **POST/PUT/PATCH**: 
   - Click the method button (POST, PUT, etc.)
   - Fill in the form
   - Add headers if needed
   - Click the method button again to submit

### Adding Authorization Header

1. Click the method button (POST, GET, etc.)
2. Scroll down to see "Headers" section
3. Click to expand
4. Add:
   ```
   Authorization: Bearer <your_token>
   ```
5. Make sure there's no extra spaces!

### Understanding Responses

**Success (200 OK):**
- Green response
- Shows data

**Created (201 Created):**
- Green response
- Shows newly created object

**Error (400/401/403):**
- Red response
- Shows error message
- Read the error to understand what went wrong

---

## 🎓 Key Endpoints Summary

| Endpoint | Method | Who Can Use | Purpose |
|----------|--------|-------------|---------|
| `/api/users/` | POST | Anyone | Register |
| `/api/auth/login/` | POST | Anyone | Login |
| `/api/courses/` | GET | Enrolled Students, Instructors | List courses |
| `/api/courses/` | POST | Instructors | Create course |
| `/api/lectures/{id}/get_video_url/` | GET | Enrolled Students | Get video URL |
| `/api/enrollments/` | POST | Instructors | Enroll student |

---

## 🐛 Troubleshooting

### "Authentication credentials not provided"
**Solution**: Add Authorization header:
```
Authorization: Bearer <your_token>
```

### "You do not have permission"
**Solution**: 
- Check your role (instructor needed for some actions)
- Make sure you're using the right token

### "Course not found" when accessing lecture
**Solution**: Make sure student is enrolled in the course

### Video not playing
**Solution**:
- Check YouTube video is "Unlisted" (not Private)
- Verify video ID is correct
- Make sure you're using embed_url in iframe

### Can't see courses as student
**Solution**: 
- Make sure course is published (`is_published: true`)
- Make sure student is enrolled

---

## ✅ Success Checklist

- [ ] Server running on `http://localhost:8000`
- [ ] Can register users
- [ ] Can login and get tokens
- [ ] Instructor can create course
- [ ] Instructor can create lecture
- [ ] Instructor can enroll student
- [ ] Student can see enrolled courses
- [ ] Student can get video embed URL
- [ ] Video plays in iframe

---

**Congratulations! Your LMS is working!** 🎉

Now you understand:
- How authentication works (JWT tokens)
- How enrollment controls access
- How YouTube videos are integrated
- How to use the browsable API

**Next Steps:**
- Build a React frontend
- Add more courses and lectures
- Customize the system for your needs

