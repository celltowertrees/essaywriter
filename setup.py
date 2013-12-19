try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
config = {
    'description': 'Twitter Essays',
    'author': 'Kelly Monson',
    'url': 'http://kmonson.com',
    'download_url': ' ',
    'author_email': 'monson.exe@gmail.com',
    'version': '0.1',
    'install_requires': ['nose', 'requests', 'BeautifulSoup4'],
    'packages': ['twitteressays'],
    'scripts': ['bin/app.py'],
    'name': 'twitteressays'
}

setup(**config)