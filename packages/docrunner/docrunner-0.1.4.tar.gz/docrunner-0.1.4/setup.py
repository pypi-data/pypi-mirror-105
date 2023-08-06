# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docrunner',
 'docrunner.constants',
 'docrunner.languages',
 'docrunner.models',
 'docrunner.utils']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.1,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['docrunner = docrunner.main:app']}

setup_kwargs = {
    'name': 'docrunner',
    'version': '0.1.4',
    'description': 'A command line tool which allows you to run the code in your markdown files to ensure that readers always have access to working code.',
    'long_description': "## Docrunner\n\nA command line tool which allows you to run the code in your markdown files to ensure that readers always have access to working code.\n\n## What does it do?\n\nDocrunner goes through your markdown file and runs any code in it, providing you safe testing for any markdown documentation. You can specify the path to the markdown file, along with other options, with flags.\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install docrunner.\n\n```powershell\npip install docrunner\n```\n\n## QuickStart\n\n```powershell\npy -m docrunner --help\n```\n\nor\n\n```powershell\ndocrunner\n```\n\n### Language Specific Help\nFor help on a specific language, run:\n```powershell\ndocrunner <language> --help\n```\n\n### Python Example\n\n```powershell\ndocrunner python --markdown-path example/example.md --multi-file\n```\n\nThis command executes all python within your README markdown file and does so by putting each snippet of python from your README into a separate file, and running each file. If you don't want each snippet in a separate python file, just remove the --multi-file option.\n\n\n## Contributing and Local Development\nIf you would like to contribute to `docrunner` please follow these instructions\nto set a local development environment for docrunner on your system\n\n1. Clone this repository\n2. Install `poetry`, a dependency management tool, with `pip` if it is not already installed:\n```powershell\npip install poetry\n```\n3. Install the necessary packages for the project with:\n```powershell\npoetry install\n```\n4. To run the docrunner cli tool in development, run:\n```powershell\npoetry run docrunner --help\n```\n5. You're all set! You can now edit source code within the `docrunner` directory\n6. (Testing CLI Tool) Run the usage example with:\n```powershell\npoetry run docrunner <language> --markdown-path example/example.md\n```\n\nFor larger changes like adding support for another language, please open an issue\n[here](https://github.com/DudeBro249/docrunner/issues)\n\n\n## Supported Languages\n\n- Python\n- Javascript\n- Typescript\n- Dart\n",
    'author': 'DudeBro249',
    'author_email': 'appdevdeploy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DudeBro249/docrunner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
