"""
WSGI config for nwb_explorer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import channels.asgi

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nwb_explorer.settings")

channel_layer = channels.asgi.get_channel_layer()
application = get_wsgi_application()
