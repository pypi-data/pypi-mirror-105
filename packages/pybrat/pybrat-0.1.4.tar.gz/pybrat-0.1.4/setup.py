# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybrat']

package_data = \
{'': ['*'],
 'pybrat': ['.mypy_cache/*',
            '.mypy_cache/3.8/*',
            '.mypy_cache/3.8/_typeshed/*',
            '.mypy_cache/3.8/collections/*',
            '.mypy_cache/3.8/importlib/*',
            '.mypy_cache/3.8/os/*',
            '.mypy_cache/3.8/pybrat/*']}

setup_kwargs = {
    'name': 'pybrat',
    'version': '0.1.4',
    'description': 'Parser for brat rapid annotation tool (Brat)',
    'long_description': None,
    'author': 'Yevgnen Koh',
    'author_email': 'wherejoystarts@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
