# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['examples', 'functimer', 'tests', 'tests.fixtures']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'functimer',
    'version': '1.1.0',
    'description': 'A decorator/wrapper package to time a given function.',
    'long_description': '# functimer\n\nA decorator/wrapper package to time a given function.\n\n[![PyPI version](https://badge.fury.io/py/functimer.svg)](https://badge.fury.io/py/functimer)\n[![Build Status](https://travis-ci.com/EJEmmett/functimer.svg?branch=master)](https://travis-ci.com/EJEmmett/functimer)\n[![codecov](https://codecov.io/gh/EJEmmett/functimer/branch/master/graph/badge.svg?token=L0UMBK8AD4)](https://codecov.io/gh/EJEmmett/functimer)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/EJEmmett/functimer.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/EJEmmett/functimer/context:python)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/857af82e6ff14a68b5bf0866e0b44d30)](https://www.codacy.com/gh/EJEmmett/functimer/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=EJEmmett/functimer&amp;utm_campaign=Badge_Grade)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n---\n## Installation\n- PYPI:\n    ```shell\n        pip install functimer\n    ```\n\n- Manual:\n    ```shell\n        poetry build\n        pip install dist/*.whl\n    ```\n\n\nHow to install [Poetry](https://python-poetry.org/docs/#installation).\n\n## Quick Example\nComprehensive Examples in `examples`\n```py\n    @timed(unit=Unit.second, number=1)\n    def timed_sleep(seconds):\n        sleep(seconds)\n\n    runtime = timed_sleep(1)\n    "1.00 s"\n```\n\n### Tests\nRun `tox` in the root directory of the repo.\n\n### License\nMIT\n',
    'author': 'Edward Emmett',
    'author_email': 'edemms12@gmail.com',
    'maintainer': 'Edward Emmett',
    'maintainer_email': 'edemms12@gmail.com',
    'url': 'https://github.com/EJEmmett/functimer',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
