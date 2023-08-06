# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cabrita', 'cabrita.abc', 'cabrita.components', 'cabrita.tests']

package_data = \
{'': ['*']}

install_requires = \
['GitPython',
 'PyYAML',
 'buzio',
 'click',
 'psutil',
 'pydashing',
 'requests',
 'sentry-sdk',
 'sphinx',
 'sphinx-rtd-theme',
 'tabulate',
 'tzlocal']

entry_points = \
{'console_scripts': ['cab = cabrita.run:run', 'cabrita = cabrita.run:run']}

setup_kwargs = {
    'name': 'cabrita',
    'version': '3.0.1',
    'description': 'Create dashboard from docker-compose.yml',
    'long_description': None,
    'author': 'Chris Maillefaud',
    'author_email': 'chris@megalus.com.br',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
