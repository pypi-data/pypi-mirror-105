# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unbound_key_control_client_api',
 'unbound_key_control_client_api.models',
 'unbound_key_control_client_api.views']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'unbound-key-control-client-api',
    'version': '0.15.0',
    'description': 'Client API for Unbound Key Control',
    'long_description': None,
    'author': 'Jerod Gawne',
    'author_email': 'jerodgawne@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9.0,<4.0.0',
}


setup(**setup_kwargs)
