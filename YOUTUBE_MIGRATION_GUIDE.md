# YouTube Integration - Migration Guide

## Overview

The LMS has been updated to use YouTube videos instead of AWS S3. This change makes the system more cost-effective while maintaining security through enrollment-based access control.

## What Changed

### 1. Model Changes

**Lecture Model:**
- ❌ Removed: `video_key` (CharField for S3 object key)
- ✅ Added: `youtube_video_id` (CharField for YouTube video ID)

**Note Model:**
- ❌ Removed: `file_key` (CharField for S3 object key)
- ✅ Added: `file_url` (URLField for direct file URLs)

### 2. Removed Dependencies
- ❌ `boto3` - No longer needed

### 3. New Service
- ✅ `core/services.py` - YouTubeService for generating embed URLs

### 4. Updated Endpoints
- `GET /api/lectures/{id}/get_video_url/` - Now returns YouTube embed URL
- `GET /api/notes/{id}/get_file_url/` - Now returns direct file URL

## Migration Steps

### Step 1: Create and Run Migrations

```bash
# Create migrations for model changes
python manage.py makemigrations courses

# Review the migration file (it will rename video_key to youtube_video_id)
# You may need to create a data migration if you have existing data

# Run migrations
python manage.py migrate
```

### Step 2: Data Migration (If You Have Existing Lectures)

If you have existing lectures with `video_key` values, you'll need to:

1. **Extract YouTube video IDs from existing data:**
   - If your `video_key` values are already YouTube IDs, the migration will handle it
   - If they're S3 keys, you'll need to manually update them

2. **Create a data migration** (optional, if needed):
   ```python
   # courses/migrations/XXXX_data_migration.py
   from django.db import migrations
   
   def migrate_video_keys_to_youtube_ids(apps, schema_editor):
       Lecture = apps.get_model('courses', 'Lecture')
       for lecture in Lecture.objects.all():
           # If video_key is already a YouTube ID, it will be migrated automatically
           # If it's an S3 key, you'll need to manually update it
           # Example: lecture.youtube_video_id = extract_youtube_id(lecture.video_key)
           pass
   
   class Migration(migrations.Migration):
       dependencies = [
           ('courses', 'XXXX_rename_video_key_to_youtube_video_id'),
       ]
       
       operations = [
           migrations.RunPython(migrate_video_keys_to_youtube_ids),
       ]
   ```

### Step 3: Update Existing Lectures

For each existing lecture, you need to:

1. **Get the YouTube video ID:**
   - If video is already on YouTube: Extract ID from URL
     - `https://www.youtube.com/watch?v=dQw4w9WgXcQ` → `dQw4w9WgXcQ`
     - `https://youtu.be/dQw4w9WgXcQ` → `dQw4w9WgXcQ`
   
2. **Update via Django admin or API:**
   ```python
   # Via Django shell
   from courses.models import Lecture
   lecture = Lecture.objects.get(id=1)
   lecture.youtube_video_id = "dQw4w9WgXcQ"  # Your YouTube video ID
   lecture.save()
   ```

### Step 4: Upload Videos to YouTube (If Not Already Done)

1. **Upload videos to YouTube:**
   - Go to YouTube Studio
   - Upload your video
   - **Important:** Set visibility to **"Unlisted"** (not Public or Private)
   - Copy the video ID from the URL

2. **Why "Unlisted"?**
   - Videos won't appear in YouTube search results
   - Only people with the link can access them
   - Backend controls who gets the link through enrollment

### Step 5: Update Notes (File URLs)

For notes, update `file_key` to `file_url`:

**Option 1: Google Drive**
- Upload PDF to Google Drive
- Right-click → Get link → Set to "Anyone with the link"
- Use the sharing URL as `file_url`

**Option 2: Dropbox**
- Upload PDF to Dropbox
- Get sharing link
- Replace `?dl=0` with `?dl=1` for direct download
- Use as `file_url`

**Option 3: Any Public URL**
- Upload to any file hosting service
- Use the direct URL as `file_url`

## API Changes

### Creating a Lecture (Before)
```json
{
  "course": 1,
  "title": "Python Basics",
  "video_key": "courses/python/intro.mp4",
  "order": 1
}
```

### Creating a Lecture (After)
```json
{
  "course": 1,
  "title": "Python Basics",
  "youtube_video_id": "dQw4w9WgXcQ",
  "order": 1
}
```

### Getting Video URL Response (Before)
```json
{
  "video_url": "https://s3.amazonaws.com/...",
  "expires_in": 600
}
```

### Getting Video URL Response (After)
```json
{
  "youtube_video_id": "dQw4w9WgXcQ",
  "embed_url": "https://www.youtube.com/embed/dQw4w9WgXcQ?modestbranding=1&rel=0",
  "watch_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

## Frontend Changes

### Before (S3 Signed URL)
```javascript
// Direct video playback
<video src={videoUrl} controls />
```

### After (YouTube Embed)
```javascript
// YouTube iframe embed
<iframe 
  src={embedUrl} 
  width="560" 
  height="315" 
  frameborder="0" 
  allowfullscreen
/>
```

## Benefits of YouTube Integration

✅ **Cost-effective** - No AWS S3 storage costs
✅ **Free hosting** - YouTube handles video storage and CDN
✅ **Better performance** - YouTube's global CDN
✅ **Easy upload** - Upload directly to YouTube
✅ **Still secure** - Backend controls access through enrollment

## Security Considerations

1. **Video Privacy:**
   - Always upload videos as "Unlisted"
   - Never set to "Public" (searchable)
   - "Private" won't work (only owner can view)

2. **Access Control:**
   - Backend still controls who can access embed URLs
   - Only enrolled students can get embed URLs
   - Enrollment checks happen before URL generation

3. **Link Sharing:**
   - If someone shares the YouTube watch URL, they can access it
   - But they need to know the video ID
   - Unlisted videos don't appear in search
   - Consider this when evaluating security needs

## Troubleshooting

### Issue: Migration fails
**Solution:** Make sure you've backed up your database. The migration renames fields, so existing data should be preserved.

### Issue: YouTube video not playing
**Solution:** 
- Check that video is set to "Unlisted" (not Private)
- Verify the video ID is correct
- Check that the embed URL is being used in an iframe

### Issue: File URLs not working
**Solution:**
- For Google Drive: Make sure sharing is set to "Anyone with the link"
- For Dropbox: Use direct download links (`?dl=1`)
- Test the URL in a browser first

## Next Steps

1. ✅ Run migrations
2. ✅ Update existing lectures with YouTube video IDs
3. ✅ Upload new videos to YouTube as "Unlisted"
4. ✅ Update frontend to use YouTube iframe embeds
5. ✅ Test video playback and access control

---

**Note:** This migration removes AWS S3 dependency, making the system more cost-effective while maintaining security through enrollment-based access control.

