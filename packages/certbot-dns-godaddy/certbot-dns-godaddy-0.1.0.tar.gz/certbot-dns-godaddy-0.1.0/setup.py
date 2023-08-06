# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['certbot_dns_godaddy']
install_requires = \
['acme>=0.31.0',
 'certbot>=0.31.0',
 'dns-lexicon>=3.2.3',
 'zope.interface>=5.4.0,<6.0.0']

setup_kwargs = {
    'name': 'certbot-dns-godaddy',
    'version': '0.1.0',
    'description': 'A certbot plugin that implements letsencrypt dns wildcard support for godaddy using lexicon',
    'long_description': '',
    'author': 'Dustyn Gibson',
    'author_email': 'miigotu@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/miigotu/certbot-dns-godaddy',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
