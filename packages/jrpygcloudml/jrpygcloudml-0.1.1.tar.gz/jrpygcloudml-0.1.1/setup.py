# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jrpygcloudml']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19']

setup_kwargs = {
    'name': 'jrpygcloudml',
    'version': '0.1.1',
    'description': 'Jumping Rivers: Google Cloud Machine Learning',
    'long_description': None,
    'author': 'Jamie',
    'author_email': 'jamie@jumpingrivers.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
