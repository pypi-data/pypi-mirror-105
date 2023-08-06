# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['housepaint']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'housepaint',
    'version': '0.0.4',
    'description': 'Colour all the output!',
    'long_description': '# housepaint\n\n<p align="center">\n    <img src="https://github.com/nicklambourne/housepaint/raw/master/docs/img/logo.png" width="250px"/>\n</p>\n\n## What is it?\n`housepaint` is a demonstration library for a talk on publishing Python packages. A silly little thing with limited \nutility, it allows you to recolor an entire function\'s worth of text with beautiful, simple decorators.\n\n## Requirements\n`housepaint` requires Python >= 3.6.\n\nAs of version 0.0.1 it has no dependencies outside the Python standard library, except for `pytest in dev`.\n\n## Installation\n\nVia `poetry`:\n```bash\npoetry add housepaint\n```\n\nVia `pip`:\n```bash\npip install housepaint\n```\n\n## Usage\n\n```python\nfrom housepaint import BG, FG, paint, Style\n\n\n@paint(foreground=FG.GREEN, background=BG.BLACK, styles=Style.BOLD)\ndef success_example() -> None:\n    print("This")\n    print("Should")\n    print("All")\n    print("Be")\n    print("Green")\n\nsuccess_example()\n```\n\nWill result in all of the print output of the function `success_example` being in bold, green font on a black background.\n\n![example of housepaint at work](https://github.com/nicklambourne/housepaint/raw/master/docs/img/example.png)\n\n### Limitations\nThis library relies on ANSI escape codes to recolour text. If your printed text has ANSI codes there\'s a good chance it \nwon\'t work out well for you.\n\n## Can I use this in my project?\nYes, please do! The code is all open source and BSD-3-Clause licensed.\n',
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
