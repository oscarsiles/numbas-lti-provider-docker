import numbasltiprovider.settings
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "numbasltiprovider.settings")

from django.core.management import ManagementUtility

ManagementUtility(['manage.py', 'check']).execute()
ManagementUtility(['manage.py', 'migrate']).execute()
ManagementUtility(['manage.py', 'collectstatic','--noinput']).execute()

import django
django.setup()
from django.contrib.auth.models import User

SUPERUSER_USER = os.environ['SUPERUSER_USER']
try:
    superuser = User.objects.get(username=SUPERUSER_USER)
except User.DoesNotExist:
    superuser = User.objects.create_superuser(
        SUPERUSER_USER,
        '{}@{}'.format(os.environ['SUPERUSER_USER'], os.environ['SERVERNAME']),
        os.environ['SUPERUSER_PASSWORD']
    )
if not superuser.is_superuser:
    superuser.is_superuser = True
    superuser.save()
