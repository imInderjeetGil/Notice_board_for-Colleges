# College Digital Notice Board

A modern Django-based digital notice board for colleges with real-time push notifications.

## 🚀 Features

- **Real-time Push Notifications** - Students receive instant alerts for new notices
- **File Attachments** - Teachers can upload multiple files with notices
- **User Authentication** - Secure teacher login system
- **Search & Filtering** - Find notices by department, semester, or keywords
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Modern UI** - Clean Bootstrap-based interface

## 🛠️ Tech Stack

- **Backend**: Django 5.2.6
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite (development) / PostgreSQL (production)
- **Push Notifications**: Web Push API
- **File Storage**: Django FileField

## 📱 Live Demo

[![Deploy to Railway](https://railway.app/button.svg)](https://railway.app/template/your-template-id)

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/notice-board-project.git
   cd notice-board-project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start development server**
   ```bash
   python manage.py runserver
   ```

6. **Open browser**
   ```
   http://localhost:8000
   ```

## 🔧 Configuration

### Environment Variables

Copy `env_example.txt` to `.env` and configure:

```bash
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
VAPID_PUBLIC_KEY=your-vapid-public-key
VAPID_PRIVATE_KEY=your-vapid-private-key
VAPID_ADMIN_EMAIL=your-email@example.com
```

### Push Notifications

1. **Generate VAPID keys** (if needed)
2. **Update settings** with your keys
3. **Test notifications** in browser

## 🚀 Deployment

### Railway (Recommended)

1. **Fork this repository**
2. **Go to** [railway.app](https://railway.app)
3. **Connect GitHub** and select your fork
4. **Add PostgreSQL database**
5. **Set environment variables**
6. **Deploy!**

### Render

1. **Fork this repository**
2. **Go to** [render.com](https://render.com)
3. **Create new Web Service**
4. **Connect GitHub** and select your fork
5. **Add PostgreSQL database**
6. **Set environment variables**
7. **Deploy!**

## 📱 Usage

### For Students
1. **Visit the website**
2. **Click "Subscribe for Notices"**
3. **Allow notifications** when prompted
4. **Receive real-time alerts** for new notices

### For Teachers
1. **Login** with your credentials
2. **Click "Post Notice"**
3. **Fill in notice details**
4. **Upload attachments** (optional)
5. **Publish** - students get notified instantly!

## 🎯 Features in Detail

### Push Notifications
- **Real-time delivery** to subscribed students
- **Cross-device support** (phone, tablet, computer)
- **Automatic subscription management**
- **Error handling** and retry logic

### File Attachments
- **Multiple file uploads** per notice
- **File type validation**
- **Secure file storage**
- **Download links** for students

### Search & Filtering
- **Text search** in titles and descriptions
- **Department filtering** (CSE, EE, ME, CE)
- **Semester filtering** (S1-S8, All)
- **Date-based filtering**

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit changes** (`git commit -m 'Add amazing feature'`)
4. **Push to branch** (`git push origin feature/amazing-feature`)
5. **Open Pull Request**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Django community for the amazing framework
- Bootstrap for the beautiful UI components
- Web Push API for real-time notifications

## 📊 Project Status

![GitHub last commit](https://img.shields.io/github/last-commit/yourusername/notice-board-project)
![GitHub issues](https://img.shields.io/github/issues/yourusername/notice-board-project)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/notice-board-project)
![GitHub stars](https://img.shields.io/github/stars/yourusername/notice-board-project)
