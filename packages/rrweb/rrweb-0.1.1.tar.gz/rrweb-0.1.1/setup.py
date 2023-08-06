# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rrweb', 'rrweb.rqUtil']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rrweb',
    'version': '0.1.1',
    'description': 'to web by streamlit',
    'long_description': None,
    'author': 'romepeng',
    'author_email': 'romepeng@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
