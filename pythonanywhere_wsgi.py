"""
WSGI Configuration Template for PythonAnywhere
===============================================
When configuring your PythonAnywhere Web Tab:
1. Click on the WSGI configuration file link (e.g., /var/www/yourusername_pythonanywhere_com_wsgi.py)
2. Replace its contents with this template (replace 'yourusername' and project directory name)
3. Save and reload the web app.
"""

import os
import sys

# 1. Add your project directory to the sys.path
path = '/home/yourusername/DjangoProject_AntiGravity'
if path not in sys.path:
    sys.path.insert(0, path)

# 2. Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

# Optional environment variables
os.environ['DJANGO_DEBUG'] = 'False'
# os.environ['DJANGO_SECRET_KEY'] = 'your-production-secret-key-here'

# 3. Import and load Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
