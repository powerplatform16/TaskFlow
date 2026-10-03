# TaskFlow Hub &mdash; FullStack Django Web Application

A modern, responsive, full-featured Task & Project Management web application built with **Python**, **Django**, and **Tailwind CSS**. Designed following clean architecture principles, Class-Based Views (CBVs), custom Model Managers, and production deployment readiness for **PythonAnywhere.com** and local development.

---

## 🚀 Key Features

- **Full CRUD Capabilities**:
  - **Tasks**: Create, Read, Update, Delete tasks with due date indicators, priorities (`Low`, `Medium`, `High`, `Urgent`), status workflows (`Pending`, `In Progress`, `Completed`, `Archived`), and estimated hour tracking.
  - **Categories / Projects**: Color-coded categorization with dynamic icons, real-time completion progress meters, and filtered task views.
  - **Scratchpad / Quick Notes**: Sticky notes with color themes (`Amber`, `Blue`, `Emerald`, `Purple`, `Rose`, `Slate`), keyword search, and pinning.
- **Interactive Dashboard**:
  - Key Performance Indicators (Total tasks, in-progress count, due today & overdue alerts, completion rate bar).
  - High-priority focus list & quick status toggles directly from cards.
- **Advanced Filtering, Sorting & Search**:
  - Filter by category, priority, status, and search query.
  - Quick-action presets (`Active`, `Due Today`, `Overdue`, `Completed`).
  - Multi-criteria sorting (Due date, Priority, Newest/Oldest).
- **Data Export Utilities**:
  - Instant one-click **CSV** and **JSON** exports.
- **Modern UI & UX**:
  - Styled with **Tailwind CSS** & **FontAwesome**.
  - Built-in **Dark / Light mode** toggler with persistent browser preference.
  - Responsive drawer navigation for mobile, tablet, and desktop screens.
  - Interactive toast notifications with auto-dismissal.
- **Developer Tools**:
  - Pre-built demo data seeder command (`python manage.py seed_data`).
  - Comprehensive automated test suite with 100% pass rate (`python manage.py test`).

---

## 📁 Modern Project Architecture

```text
DjangoProject_AntiGravity/
├── core/                         # Project Configuration & Settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py               # Configured for Local Dev & PythonAnywhere
│   ├── urls.py                   # Root URL Routing
│   └── wsgi.py
├── tasks/                        # Main Application Module
│   ├── migrations/               # Database Schema Migrations
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py      # Demo data management command
│   ├── admin.py                  # Customized Django Admin Panels
│   ├── apps.py
│   ├── forms.py                  # Tailwind Styled ModelForms & Clean Validation
│   ├── models.py                 # Category, Task, Note & Custom QuerySets
│   ├── tests.py                  # Unit and Integration Test Suite
│   ├── urls.py                   # App URL Patterns
│   ├── utils.py                  # Seeder logic and utility functions
│   └── views.py                  # CBVs (ListView, DetailView, etc.) & FBVs
├── templates/                    # Modular Template System
│   ├── base.html                 # Main layout with Tailwind & dark mode
│   ├── includes/
│   │   ├── navbar.html           # Responsive navigation bar
│   │   ├── messages.html         # Flash alert toast component
│   │   └── pagination.html       # Dynamic pagination component
│   └── tasks/
│       ├── dashboard.html        # Interactive analytics dashboard
│       ├── task_list.html        # Task directory with filters & search
│       ├── task_detail.html      # Detailed task view
│       ├── task_form.html        # Create / Edit task form
│       ├── task_confirm_delete.html
│       ├── category_list.html    # Category cards with progress bars
│       ├── category_form.html
│       ├── category_confirm_delete.html
│       ├── note_list.html        # Scratchpad sticky note grid
│       ├── note_form.html
│       └── note_confirm_delete.html
├── static/                       # Static Assets
│   ├── css/
│   │   └── custom.css            # Custom typography & styles
│   └── js/
│       └── main.js               # Theme toggler & alert handlers
├── staticfiles/                  # Collected static files for production
├── manage.py
├── pythonanywhere_wsgi.py        # Ready-to-use PythonAnywhere WSGI file
├── requirements.txt              # Project dependencies
├── .env.example
└── README.md
```

---

## 💻 Local Development Setup

### 1. Clone or Open the Project
Open a terminal in the project directory:
```bash
cd DjangoProject_AntiGravity
```

### 2. Set Up a Python Virtual Environment
**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations
```bash
python manage.py migrate
```

### 5. (Optional) Load Sample Demo Data
To immediately populate realistic categories, tasks, and notes:
```bash
python manage.py seed_data
```

### 6. (Optional) Create Admin Superuser
```bash
python manage.py createsuperuser
```

### 7. Run the Local Development Server
```bash
python manage.py runserver
```
Visit **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser.

---

## 🧪 Running Automated Tests

Run the full test suite verifying models, views, CRUD operations, toggles, and data exports:
```bash
python manage.py test
```

---

## ☁️ PythonAnywhere.com Deployment Guide

Follow these simple steps to deploy your application to PythonAnywhere:

### Step 1: Push or Upload Project
In PythonAnywhere, open a **Bash Console** and clone your repository or upload your files to your home directory:
```bash
cd ~
git clone <your-git-repo-url> DjangoProject_AntiGravity
# Or create directory and upload files
```

### Step 2: Create a Virtual Environment & Install Requirements
In the PythonAnywhere Bash console:
```bash
cd ~/DjangoProject_AntiGravity
mkvirtualenv --python=python3.10 taskflow-env
pip install -r requirements.txt
```

### Step 3: Run Migrations and Collect Static Files
```bash
python manage.py migrate
python manage.py seed_data        # Optional: load sample tasks
python manage.py collectstatic --noinput
```

### Step 4: Configure Web Tab in PythonAnywhere
1. Go to the **Web** tab in PythonAnywhere dashboard.
2. Click **Add a new web app** -> Choose **Manual configuration** -> Select **Python 3.10**.
3. In the **Virtualenv** section:
   - Enter: `/home/yourusername/.virtualenvs/taskflow-env`
4. In the **Static files** section, add mappings:
   - **URL**: `/static/`
   - **Directory**: `/home/yourusername/DjangoProject_AntiGravity/staticfiles`
5. In the **Code** section:
   - **Source code**: `/home/yourusername/DjangoProject_AntiGravity`
   - **Working directory**: `/home/yourusername/DjangoProject_AntiGravity`
6. Click on the **WSGI configuration file** link (e.g. `/var/www/yourusername_pythonanywhere_com_wsgi.py`) and replace its contents with:

```python
import os
import sys

path = '/home/yourusername/DjangoProject_AntiGravity'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
os.environ['DJANGO_DEBUG'] = 'False'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
*(Replace `yourusername` with your actual PythonAnywhere username)*.

### Step 5: Reload Your Web App
Click the green **Reload yourusername.pythonanywhere.com** button. Your site is now live! 🚀
