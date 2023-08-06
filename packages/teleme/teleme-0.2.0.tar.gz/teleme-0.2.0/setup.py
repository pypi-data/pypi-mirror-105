# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['teleme']

package_data = \
{'': ['*']}

install_requires = \
['hiyori>=0.2,<0.3']

extras_require = \
{':python_version <= "3.7"': ['importlib-metadata>=4.0.1,<5.0.0']}

setup_kwargs = {
    'name': 'teleme',
    'version': '0.2.0',
    'description': 'An async, super simple Telegram Bot framework.',
    'long_description': 'Teleme\n======\nTeleme(pronounced `tell-me`)  is an async, super simple Telegram Bot framework.\n\nUnder Development\n-----------------\nWhilst the code has been used for years privately, since I just released the code,\nthere may have been some bugs that have left undiscovered. I have decided to set\nthe status of this project as Beta.\n\nLicense\n-------\n\n    Copyright 2020 Kaede Hoshikawa\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n    http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n',
    'author': 'Kaede Hoshikawa',
    'author_email': 'futursolo@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/futursolo/teleme',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
