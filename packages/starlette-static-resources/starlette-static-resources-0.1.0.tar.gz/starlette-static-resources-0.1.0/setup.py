# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starlette_static_resources']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.6.0,<0.7.0', 'starlette>=0.14.2,<0.15.0']

extras_require = \
{':python_version < "3.9"': ['importlib-resources>=5.1.2,<6.0.0']}

setup_kwargs = {
    'name': 'starlette-static-resources',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'david',
    'author_email': 'davidventura27@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
