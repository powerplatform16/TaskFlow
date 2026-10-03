from django.utils import timezone
from datetime import timedelta
from .models import Category, Task, Note


def populate_demo_data():
    """Populates realistic demo categories, tasks, and notes for initial testing."""
    categories_data = [
        {'name': 'Work & Projects', 'color': 'indigo', 'icon': 'briefcase', 'description': 'Client deliverables, sprints, and team meetings'},
        {'name': 'Personal Life', 'color': 'emerald', 'icon': 'user', 'description': 'Errands, hobbies, and personal goals'},
        {'name': 'Tech & Learning', 'color': 'blue', 'icon': 'code', 'description': 'Django mastery, Python architectures, and cloud deployments'},
        {'name': 'Finance & Taxes', 'color': 'amber', 'icon': 'currency-dollar', 'description': 'Invoicing, receipts, and budgeting'},
    ]

    cat_map = {}
    for cdata in categories_data:
        cat, _ = Category.objects.get_or_create(
            name=cdata['name'],
            defaults={
                'color': cdata['color'],
                'icon': cdata['icon'],
                'description': cdata['description'],
            }
        )
        cat_map[cdata['name']] = cat

    today = timezone.localdate()

    tasks_data = [
        {
            'title': 'Deploy Django Project to PythonAnywhere',
            'description': 'Configure WSGI file, set STATIC_ROOT, run collectstatic, and verify live domain.',
            'category': cat_map.get('Tech & Learning'),
            'priority': 'URGENT',
            'status': 'IN_PROGRESS',
            'due_date': today + timedelta(days=1),
            'estimated_hours': 2.0,
        },
        {
            'title': 'Review SQLite3 Database Migrations',
            'description': 'Ensure all model relationships, on_delete rules, and indexes are properly configured.',
            'category': cat_map.get('Tech & Learning'),
            'priority': 'HIGH',
            'status': 'COMPLETED',
            'due_date': today - timedelta(days=1),
            'estimated_hours': 1.0,
            'completed_at': timezone.now(),
        },
        {
            'title': 'Prepare Q4 Freelance Invoice Summary',
            'description': 'Export billable hours from tracking sheet and format client PDF invoice.',
            'category': cat_map.get('Finance & Taxes'),
            'priority': 'MEDIUM',
            'status': 'PENDING',
            'due_date': today + timedelta(days=3),
            'estimated_hours': 1.5,
        },
        {
            'title': 'Weekly Grocery Shopping & Meal Prep',
            'description': 'Buy fresh vegetables, whole grains, and prep lunch boxes for the work week.',
            'category': cat_map.get('Personal Life'),
            'priority': 'LOW',
            'status': 'PENDING',
            'due_date': today,
            'estimated_hours': 1.0,
        },
        {
            'title': 'Refactor Base Templates with Tailwind CSS',
            'description': 'Implement responsive navbar, dark/light accents, badges, and modal confirmations.',
            'category': cat_map.get('Work & Projects'),
            'priority': 'HIGH',
            'status': 'COMPLETED',
            'due_date': today - timedelta(days=2),
            'estimated_hours': 3.5,
            'completed_at': timezone.now(),
        },
        {
            'title': 'Update Documentation & README',
            'description': 'Document pythonanywhere deployment instructions, local dev steps, and feature list.',
            'category': cat_map.get('Work & Projects'),
            'priority': 'MEDIUM',
            'status': 'IN_PROGRESS',
            'due_date': today + timedelta(days=2),
            'estimated_hours': 1.0,
        },
        {
            'title': 'Renew Domain and SSL Certificate',
            'description': 'Check domain expiration date and ensure auto-renewal is enabled.',
            'category': cat_map.get('Tech & Learning'),
            'priority': 'URGENT',
            'status': 'PENDING',
            'due_date': today - timedelta(days=2),  # intentionally overdue for demo
            'estimated_hours': 0.5,
        },
    ]

    for tdata in tasks_data:
        Task.objects.get_or_create(
            title=tdata['title'],
            defaults=tdata
        )

    notes_data = [
        {
            'title': 'PythonAnywhere Deployment Quick Checklist',
            'content': '1. Upload/git clone code to /home/username/project\n2. Create virtualenv: mkvirtualenv --python=python3.10 myenv\n3. pip install -r requirements.txt\n4. Set static files mappings in Web tab\n5. Edit WSGI configuration file\n6. Reload webapp!',
            'category': cat_map.get('Tech & Learning'),
            'is_pinned': True,
            'theme': 'blue',
        },
        {
            'title': 'Django CBV vs FBV Best Practice Notes',
            'content': 'Use Class-Based Views (ListView, DetailView, CreateView, UpdateView, DeleteView) for standard CRUD. Use FBVs for quick custom actions like toggles, CSV streaming, or webhooks.',
            'category': cat_map.get('Tech & Learning'),
            'is_pinned': True,
            'theme': 'yellow',
        },
        {
            'title': 'Ideas for Future Enhancements',
            'content': '- Add user authentication and multi-user isolation\n- Add email reminders using celery or django-q\n- Add Kanban drag-and-drop board\n- Add attachment uploads (PDFs, images)',
            'category': cat_map.get('Work & Projects'),
            'is_pinned': False,
            'theme': 'emerald',
        },
    ]

    for ndata in notes_data:
        Note.objects.get_or_create(
            title=ndata['title'],
            defaults=ndata
        )
