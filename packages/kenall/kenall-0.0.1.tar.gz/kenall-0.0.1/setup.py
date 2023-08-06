# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kenall']

package_data = \
{'': ['*']}

install_requires = \
['mojimoji>=0.0.11,<0.0.12']

setup_kwargs = {
    'name': 'kenall',
    'version': '0.0.1',
    'description': '日本郵政が提供している郵便番号ファイル(通称:KEN_ALL.csv)をパースするPython用パッケージ',
    'long_description': None,
    'author': 'Yoshiki Shinagawa',
    'author_email': 's.yoshiki1123@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/s-yoshiki',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
