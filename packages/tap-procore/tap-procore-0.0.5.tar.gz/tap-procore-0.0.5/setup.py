# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_procore', 'tap_procore.tests']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0', 'singer-sdk>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['tap-procore = tap_procore.tap:cli']}

setup_kwargs = {
    'name': 'tap-procore',
    'version': '0.0.5',
    'description': '`tap-procore` is Singer tap for procore, built with the Singer SDK.',
    'long_description': None,
    'author': 'hotglue',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
