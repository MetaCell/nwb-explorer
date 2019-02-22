
import requests
import os
import logging

CACHE_DEFAULT_DIR = 'nwb_files_cache/'

def get_file_from_url(file_url, fname=None, cache_dir=CACHE_DEFAULT_DIR):
    file_name = cache_dir + (file_url.split('/')[-1] if not fname else fname)
    if not os.path.exists(file_name):
        logging.info('Downloading {} to {}...'.format(file_url, file_name))
        response = requests.get(file_url)
        with open(file_name, 'wb') as f:
            f.write(response.content)
    return file_name