# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jq_test']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jq-test2',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'fikirsiz',
    'author_email': 'hromus@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
