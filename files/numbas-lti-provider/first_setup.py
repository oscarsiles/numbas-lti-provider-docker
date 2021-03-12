import random
import re
import os
import traceback
import urllib.parse
import importlib

def print_notice(s):
    print('\033[92m'+s+'\033[0m\n')

class Command(object):
    hosts_template = """ALLOWED_HOSTS = ['{host}', '127.0.0.1', 'localhost']"""
    postgresql_template = """DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '{POSTGRES_DB}',
        'USER': '{POSTGRES_USER}',
        'PASSWORD': '{POSTGRES_PASSWORD}',
        'HOST': 'db',
    }}
}}"""

    redis_template = """CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL','redis://redis:6379')],
        },
        "ROUTING": "numbasltiprovider.routing.channel_routing",
    },
}"""

    huey_template = """
HUEY = {
    'connection': {
        'host': 'redis',
        'port': 6379,
    },
}"""

    def handle(self):
        self.write_files()

        import numbasltiprovider.settings
        importlib.reload(numbasltiprovider.settings)

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "numbasltiprovider.settings")

        print_notice("Now we'll check that everything works properly")

        self.run_management_command('check')

        self.run_management_command('migrate')

        from django.contrib.auth.models import User;
        User.objects.create_superuser('admin', 'admin@{}'.format(os.environ['SERVERNAME']), os.environ['SUPERUSER_PASSWORD'])

        print_notice("Done!")

        self.run_management_command('collectstatic')
        print_notice("The Numbas LTI provider is now set up. Once you've configured your web server, it'll be ready to use.")

    def write_files(self):
        settings_subs = [
            (r"^DEBUG = (.*?)$", 'False'),
            (r"^SESSION_COOKIE_SECURE = (.*?)$", 'True'),
            (r"^CSRF_COOKIE_SECURE = (.*?)$", 'True'),
            (r"^STATIC_ROOT = '(.*?)'", '/srv/numbas-lti-static/'),
            (r"^MEDIA_ROOT = '(.*?)'", '/srv/numbas-lti-media/'),
            (r"^(ALLOWED_HOSTS = \[.*?\])$", self.hosts_template.format(host=os.environ['SERVERNAME'])),
            (r"^(DATABASES = {.*?^})", self.postgresql_template.format(**os.environ)),
            (r"^(CHANNEL_LAYERS = {.*?^})", self.redis_template),
            (r"^SECRET_KEY = '(.*?)'", ''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50))),
            (r"EMAIL_COMPLETION_RECEIPTS = (.*?)$", 'True'),
            (r"DEFAULT_FROM_EMAIL = '(.*?)'", 'numbas@{}'.format(os.environ['SERVERNAME'])),
        ]
        self.sub_file('numbasltiprovider/settings.py', settings_subs)

    def sub_file(self, fname, subs, confirm_overwrite=True):

        with open(fname+'.dist') as f:
            text = f.read()

        for pattern, value in subs:
            pattern = re.compile(pattern, re.MULTILINE | re.DOTALL)
            text = self.sub(text, pattern, value)

        text += self.huey_template
        print(text)

        with open(fname, 'w') as f:
            f.write(text)

    def sub(self, source, pattern, value):
        def fix(m):
            t = m.group(0)
            start, end = m.span(1)
            ts, te = m.span(0)
            start -= ts
            end -= ts
            return t[:start]+value+t[end:]
        if not pattern.search(source):
            raise Exception("Didn't find {}".format(pattern.pattern))
        return pattern.sub(fix, source)

    def run_management_command(self, *args):
        from django.core.management import ManagementUtility
        args = ['manage.py'] + list(args)
        utility = ManagementUtility(args)
        try:
            utility.execute()
        except SystemExit:
            pass
        print('')

if __name__ == '__main__':
    command = Command()
    try:
        command.handle()
    except Exception as e:
        traceback.print_exc()
        print_notice("The setup script failed. Look at the error message above for a description of why.")
