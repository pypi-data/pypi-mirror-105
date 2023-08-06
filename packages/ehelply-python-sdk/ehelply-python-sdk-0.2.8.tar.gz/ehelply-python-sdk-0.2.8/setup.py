# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ehelply_python_sdk',
 'ehelply_python_sdk.services',
 'ehelply_python_sdk.services.access',
 'ehelply_python_sdk.services.meta',
 'ehelply_python_sdk.services.monitor',
 'ehelply_python_sdk.services.notes',
 'ehelply_python_sdk.services.products',
 'ehelply_python_sdk.services.security']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.1.0,<3.0.0',
 'cryptography>=3.4.7,<4.0.0',
 'ehelply-logger>=0.0.8,<0.0.9',
 'httpx>=0.18.1,<0.19.0',
 'isodate>=0.6.0,<0.7.0',
 'passlib>=1.7.4,<2.0.0',
 'pdoc3>=0.9.2,<0.10.0',
 'pyOpenSSL>=20.0.1,<21.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'pytest-asyncio>=0.15.1,<0.16.0',
 'pytest-cov>=2.11.1,<3.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'python-jose>=3.2.0,<4.0.0',
 'python-slugify>=5.0.2,<6.0.0',
 'requests>=2.25.1,<3.0.0',
 'typer>=0.3.2,<0.4.0',
 'wheel>=0.36.2,<0.37.0']

entry_points = \
{'console_scripts': ['ehelply_sdk = ehelply_python_sdk.cli:cli_main']}

setup_kwargs = {
    'name': 'ehelply-python-sdk',
    'version': '0.2.8',
    'description': '',
    'long_description': '# SDK\n\n* Install wipe and upgrade latest packages: `requests@latest python-jose@latest pyjwt@latest passlib@latest cryptography@latest pyopenssl@latest typer@latest python_dateutil@latest python-slugify@latest wheel@latest ehelply-logger@latest pytest-cov@latest pytest-asyncio@latest isodate@latest pydantic@latest pdoc3@latest httpx@latest`',
    'author': 'Shawn Clake',
    'author_email': 'shawn.clake@ehelply.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://ehelply.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
