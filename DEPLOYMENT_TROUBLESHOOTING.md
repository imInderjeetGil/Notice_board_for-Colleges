# Deployment Troubleshooting Guide

## 🚨 Common Issues & Solutions

### Issue 1: psycopg2-binary Build Failure
**Error**: `Failed building wheel for psycopg2-binary`

**Solutions**:

#### Option A: Use Development Requirements (SQLite)
```bash
pip install -r requirements-dev.txt
```
- ✅ **Pros**: No build issues, works immediately
- ❌ **Cons**: SQLite only, not suitable for production

#### Option B: Install PostgreSQL Development Libraries
**Ubuntu/Debian**:
```bash
sudo apt-get install libpq-dev python3-dev
pip install psycopg2-binary
```

**macOS**:
```bash
brew install postgresql
pip install psycopg2-binary
```

**Windows**:
```bash
# Install PostgreSQL from https://www.postgresql.org/download/windows/
pip install psycopg2-binary
```

#### Option C: Use Alternative Database Driver
```bash
# For MySQL
pip install mysqlclient

# For SQLite (development only)
# No additional driver needed
```

### Issue 2: Railway/Render Deployment Issues

#### Railway Specific:
1. **Use requirements-railway.txt**:
   ```bash
   cp requirements-railway.txt requirements.txt
   ```

2. **Set Environment Variables**:
   ```
   DJANGO_SETTINGS_MODULE=notice_board_project.settings_production
   SECRET_KEY=your-secret-key
   DEBUG=False
   ```

3. **Database Configuration**:
   - Railway automatically provides PostgreSQL
   - Use `DATABASE_URL` environment variable

#### Render Specific:
1. **Use requirements-prod.txt**:
   ```bash
   cp requirements-prod.txt requirements.txt
   ```

2. **Build Command**:
   ```bash
   pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
   ```

3. **Start Command**:
   ```bash
   gunicorn notice_board_project.wsgi:application
   ```

### Issue 3: Static Files Not Loading

**Solution**: Add to settings.py
```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# For production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Issue 4: Push Notifications Not Working

**Check**:
1. **VAPID Keys**: Ensure they're set in environment variables
2. **HTTPS**: Push notifications require secure context
3. **Service Worker**: Check browser console for errors
4. **Permissions**: Ensure notifications are allowed

### Issue 5: File Uploads Not Working

**Solution**: Configure media files
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## 🚀 Quick Deployment Commands

### For Development (SQLite):
```bash
pip install -r requirements-dev.txt
python manage.py migrate
python manage.py runserver
```

### For Railway:
```bash
pip install -r requirements-railway.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

### For Render:
```bash
pip install -r requirements-prod.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

## 🔧 Environment Variables Template

```bash
# Django Settings
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (Railway/Render provide this automatically)
DATABASE_URL=postgresql://user:password@host:port/database

# Web Push Settings
VAPID_PUBLIC_KEY=your-vapid-public-key
VAPID_PRIVATE_KEY=your-vapid-private-key
VAPID_ADMIN_EMAIL=your-email@example.com
```

## 📱 Testing After Deployment

1. **Check website loads**: Visit your deployed URL
2. **Test user registration**: Create a superuser
3. **Test notice creation**: Post a notice
4. **Test push notifications**: Subscribe and create notice
5. **Test file uploads**: Upload attachments

## 🆘 Still Having Issues?

1. **Check deployment logs** for specific errors
2. **Test locally first** with development requirements
3. **Use SQLite for initial deployment** (easier)
4. **Gradually add PostgreSQL** once basic deployment works

