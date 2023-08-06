# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aio_pool']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aio-pool',
    'version': '0.1.0',
    'description': "Extending Python's process pool to support async functions.",
    'long_description': None,
    'author': 'Itay Azolay',
    'author_email': 'itayazolay@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
