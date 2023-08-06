# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['htranslate']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.65.0,<0.66.0', 'uvicorn>=0.13.4,<0.14.0']

setup_kwargs = {
    'name': 'htranslate',
    'version': '1.0.1',
    'description': 'Translate text into h-binary.',
    'long_description': None,
    'author': 'vcokltfre',
    'author_email': 'vcokltfre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
