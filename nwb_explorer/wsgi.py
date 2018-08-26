"""
WSGI config for pygeppetto_template project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import channels.asgi

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pygeppetto_template.settings")

channel_layer = channels.asgi.get_channel_layer()
application = get_wsgi_application()
