FROM jupyterhub/k8s-hub:0.9-c9ee61d
    
COPY --chown=1000:1000 page.html /usr/local/share/jupyterhub/templates/page.html
COPY --chown=1000:1000 spawn_pending.html /usr/local/share/jupyterhub/templates/spawn_pending.html
COPY --chown=1000:1000 jupyter.png /usr/local/share/jupyterhub/static/images/jupyter.png
COPY --chown=1000:1000 favicon.ico /usr/local/share/jupyterhub/static/favicon.ico
COPY --chown=1000:1000 favicon.ico /usr/local/share/jupyterhub/static/images/favicon.ico
COPY --chown=1000:1000 auth.py /usr/local/lib/python3.6/dist-packages/tmpauthenticator/__init__.py
COPY --chown=1000:1000 hot_fix_for_eventsource.js /usr/local/share/jupyterhub/static/hot_fix_for_eventsource.js
CMD ["jupyterhub", "--config", "/srv/jupyterhub_config.py"]