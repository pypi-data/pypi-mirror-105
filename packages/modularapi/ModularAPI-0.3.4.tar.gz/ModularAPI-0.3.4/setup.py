# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['modularapi', 'modularapi.templates.default']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.13,<4.0.0',
 'alembic>=1.5.5,<2.0.0',
 'psycopg2-binary>=2.8.6,<3.0.0',
 'pydantic[email,dotenv]>=1.8.1,<2.0.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['ModularAPI = modularapi.cli:cli']}

setup_kwargs = {
    'name': 'modularapi',
    'version': '0.3.4',
    'description': 'A CLI Framework based on FastAPI and Typer using module-based architecture.',
    'long_description': None,
    'author': 'Modular-lab',
    'author_email': 'contact.flapili@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://modular-lab.github.io/Modular-API/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
