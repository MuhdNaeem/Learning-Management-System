# Learning Management System - Project Standards & Design

## Project Overview

**Client:** Online tutor who teaches courses to different students

**Current Problem:**
- Lectures uploaded to YouTube as private videos
- Links shared with enrolled students
- **No security** - links are shareable, students can share with others

**Solution Goal:**
- Build a Learning Management System (LMS)
- Backend: Django REST Framework
- Frontend: React (to be implemented later)
- Scale: 300-400 students initially
- Budget: Limited
- Learning-focused project

**Time Commitment:** 5 hours per day

---

## System Architecture

### High-Level Design

```
React Frontend
   |
   |  (JWT Auth)
   v
Django REST Framework (API)
   |
   |-- PostgreSQL (data)
   |
   |-- Object Storage (videos, notes)
```

### Design Pattern

**Approach:** Monolithic Backend + Modular Apps

**Why:**
- 300–400 students is easily handled by this setup
- Easier to develop, debug, and learn
- Django REST Framework is perfect for this use case

### Django Apps Structure

```
lms_backend/
│
├── accounts/        # users, roles, auth
├── courses/         # courses, lectures, notes
├── enrollments/     # student-course relation
├── payments/        # optional (future)
├── permissions/     # custom DRF permissions
└── core/            # shared utilities
```

**Note:** This follows a Domain-Driven style, not framework-driven.

---

## Security Model

### Key Principle

**Students never get a public video URL.**

### Access Flow

1. Student logs in
2. Student requests a lecture
3. Backend checks:
   - Is the user authenticated?
   - Is the user enrolled in this course?
4. If yes → backend returns temporary access to the video

### Video Access Strategy (Low Budget)

**Option 1 (RECOMMENDED - Best for learning + budget):**

**Private videos in cloud storage + signed URLs**

**Flow:**
```
Student → API → Permission Check → Signed URL (expires in 5–10 min)
```

**Benefits:**
- Even if student shares URL → it expires
- Each request is validated by your backend
- This is how real platforms work (Udemy-like)

---

## Video Hosting Platform

### ❌ Avoid

- YouTube (private/unlisted = insecure)
- Vimeo paid plans (expensive)

### ✅ Recommended (Ranked)

#### 🥇 AWS S3 + CloudFront (Student Tier Friendly)

**Why this is perfect:**
- You already know AWS
- Industry-standard
- Extremely cheap at small scale
- Teaches real-world skills

**Setup:**
- S3 bucket (private)
- CloudFront distribution
- Signed URLs via Django

**Cost (approx):**
- Storage: ~$0.023/GB
- Bandwidth: minimal for 300 students

#### 🥈 Backblaze B2 + Cloudflare

- Even cheaper than AWS
- Slightly more setup complexity
- Good alternative if budget is very tight

### Notes & PDFs

- Store in same object storage
- PDFs can also be served via signed URLs

---

## Core Data Model

### User
```
User
- id
- name
- email
- role (student | instructor | admin)
```

### Course
```
Course
- id
- title
- description
- instructor
- is_published
```

### Lecture
```
Lecture
- id
- course
- title
- video_key (S3 object key)
- order
```

### Notes
```
Note
- id
- lecture
- file_key
```

### Enrollment
```
Enrollment
- user
- course
- enrolled_at
- is_active
```

**Note:** This is simple, normalized, and production-ready.

---

## Development Roadmap

### Week 1 Tasks (5 hours/day)

*[To be detailed in upcoming prompts]*

---

## Implementation Notes

- This document serves as the standard reference for the LMS project
- All implementation decisions should align with this design
- Security is a top priority - no public video URLs
- Budget-conscious solutions preferred
- Learning-focused approach
