import numbasltiprovider.settings
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "numbasltiprovider.settings")

from django.core.management import ManagementUtility

ManagementUtility(['manage.py', 'check']).execute()
ManagementUtility(['manage.py', 'migrate']).execute()
ManagementUtility(['manage.py', 'collectstatic']).execute()

import django
django.setup()
from django.contrib.auth.models import User

User.objects.create_superuser(
    '{}'.format(os.environ['SUPERUSER_USER']),
    '{}@{}'.format(os.environ['SUPERUSER_USER'], os.environ['SERVERNAME']),
    os.environ['SUPERUSER_PASSWORD']
)
