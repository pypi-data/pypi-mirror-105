# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['housepaint']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'housepaint',
    'version': '0.0.7',
    'description': 'Colour all the output!',
    'long_description': '# housepaint\nDemonstration library for a talk on publishing Python packages\n',
    'author': 'Nicholas Lambourne',
    'author_email': 'nick@ndl.im',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nicklambourne/housepaint',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
