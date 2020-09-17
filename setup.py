try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'COVID-19 stats in your terminal',
    'author': 'Adams Rosales (https://github.com/arlovesdata)',
    'url': 'https://github.com/adaros92/coronacli',
    'author_email': 'adams.rosales.92@gmail.com',
    'version': '0.1.2',
    'install_requires': ['requests', 'sqlalchemy', 'pandas'],
    'packages': ['coronacli'],
    'package_dir': {'coronacli': 'coronacli/'},
    'scripts': [],
    'name': 'coronacli',
    'python_requires': '>=3.6'
}

setup(**config)
