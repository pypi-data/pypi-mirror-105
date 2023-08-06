# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netcleanser']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'netcleanser',
    'version': '0.1.0',
    'description': 'The library makes parsing and manipulation of URL🌐 and Email address📧 easy.',
    'long_description': None,
    'author': 'Shinichi Takayanagi',
    'author_email': 'shinichi.takayanagi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
