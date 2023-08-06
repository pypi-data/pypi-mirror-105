# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['htranslate']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'htranslate',
    'version': '1.0.0',
    'description': 'Translate text into h-binary.',
    'long_description': None,
    'author': 'vcokltfre',
    'author_email': 'vcokltfre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
