# 🎓 Faculty Activity Management Portal

A modern web-based Faculty Activity Management Portal developed using **Django** for the Department of Information Technology. The portal enables faculty members to submit, manage, edit, and generate reports for their monthly academic and professional activities.

---

## 🌐 Live Demo

https://faculty-activity-management-portal.onrender.com

## 📌 Features

### 🔐 Authentication
- Secure Login System
- One-time User Registration
- Logout Functionality
- Session-based Authentication

### 📋 Activity Management
- Add Faculty Activities
- Edit Existing Activities
- Delete Activities
- Upload Multiple PDF Proofs
- View Uploaded Attachments

### 👨‍🏫 Faculty Management
- Shared Faculty List
- Add New Faculty Members
- Automatic Faculty ID Generation

### 📚 Activity Management
- Shared Activity List
- Add New Activities

### 📊 Dashboard
- Total Faculty Members
- Total Activity Submissions
- Monthly Activity Count
- Reports Generated
- Recent Submissions

### 📄 Reports
- Generate Monthly PDF Reports
- Department Logo Included
- Categorized Activity Report
- Professional Report Layout
- Automatic Page Numbers

### 🔍 Search Activities
- Filter by Month
- Filter by Date Range
- Download Attachments
- Edit Activities
- Delete Activities

### 📎 File Upload
- Multiple PDF Upload
- 10 MB File Size Validation
- Secure Attachment Storage

---

# 🛠 Technologies Used

### Backend
- Python
- Django 6
- SQLite

### Frontend
- HTML5
- CSS3
- JavaScript
- jQuery
- AJAX

### Libraries
- ReportLab
- Select2
- DataTables
- SweetAlert2
- WhiteNoise

### Deployment
- GitHub
- Render

---

# 📂 Project Structure

```
FacultyMonthlyActivities/
│
├── activities/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── migrations/
│   └── management/
│
├── facultyactivities/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── static/
│
├── templates/
│
├── media/
│
├── manage.py
│
├── requirements.txt
│
└── README.md
```

---

# 🚀 Installation

## 1. Clone Repository

```bash
git clone https://github.com/chai12tanya12-afk/faculty-activity-management-portal.git
```

---

## 2. Move into Project

```bash
cd faculty-activity-management-portal
```

---

## 3. Create Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 4. Install Requirements

```bash
pip install -r requirements.txt
```

---

## 5. Apply Migrations

```bash
python manage.py migrate
```

---

## 6. Import Faculty Members

```bash
python manage.py import_faculty
```

---

## 7. Import Activities

```bash
python manage.py import_activities
```

---

## 8. Run Development Server

```bash
python manage.py runserver
```

---

Open

```
http://127.0.0.1:8000
```

---

# 🌐 Production Deployment

The project is deployment-ready.

For deployment:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py import_faculty
python manage.py import_activities
python manage.py collectstatic --noinput
```

---

# 👤 Login

On first launch:

- Register a user account.
- Login using the created credentials.

Subsequent users can log in using the existing credentials.

---

# 📄 Reports

The portal automatically generates:

- Monthly Faculty Activity Reports
- Department Header
- Faculty Details
- Description
- Entry Date
- Pagination
- Downloadable PDF

---

# 📸 Screenshots

You may add screenshots here.

Example:

```
screenshots/
    login.png
    dashboard.png
    activity_form.png
    reports.png
    activities.png
```

---

# 📦 Requirements

Main Packages

- Django
- ReportLab
- WhiteNoise
- django-widget-tweaks
- jQuery
- DataTables
- SweetAlert2

See **requirements.txt** for complete dependencies.

---

# 👨‍💻 Developer

**K. Chaitanya**

B.Tech – Information Technology

Vishnu Institute of Technology, Bhimavaram

---

# 📄 License

This project was developed for academic purposes.

---

# ⭐ Acknowledgement

Developed as part of the Faculty Activity Management System for the Department of Information Technology to simplify faculty activity submission, report generation, and activity management.
