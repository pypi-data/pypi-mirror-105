# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prettynum']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'prettynum',
    'version': '0.1.0',
    'description': 'Simple number formatting for python',
    'long_description': "# prettynum\n\nSimple number formatting for python inspired by the [scales](https://scales.r-lib.org/index.html) package in R. `prettynum` is lightweight and has not third party library dependencies.\n\n- GitHub: [https://github.com/SamEdwardes/prettynum](https://github.com/SamEdwardes/prettynum)\n- PyPi:  [https://pypi.org/project/prettynum/](https://pypi.org/project/prettynum/)\n\n## Installation\n\n```bash\npip install prettynum\n```\n\n## Usage\n\n```python\n>>> from prettynum import comma, dollar\n>>> comma(1000)\n'1,000'\n>>> comma(1000, 3)\n'1,000.000'\n>>> comma(1000.89, 1)\n'1,000.9'\n>>> dollar(1000)\n'$1,000'\n>>> dollar(1000, 3)\n'$1,000.000'\n>>> dollar(1000.89, 1)\n'$1,000.9'\n```\n",
    'author': 'SamEdwardes',
    'author_email': 'edwardes.s@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SamEdwardes/prettynum',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
