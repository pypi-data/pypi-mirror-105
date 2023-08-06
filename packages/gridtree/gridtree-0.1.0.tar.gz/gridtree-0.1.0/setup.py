# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gridtree']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gridtree',
    'version': '0.1.0',
    'description': 'Generalized quadtree.',
    'long_description': '# gridtree\nGeneralized quadtree.\n\n\n# Installation\n```\npip install gridtree\n```\n\n# Usage\n\nTODO: expand\n\n```python\npoints : Collection[tuple[NormalizedFloat, ...]] # between 0 and 1 inclusive\n\ntree = GTree(max_leaf_size=2)(points)\ntree_as_list = GTreeList(max_leaf_size=2)(points)\ntree_as_list = GTreeList.gtree_to_list(tree)\n```\n\n# Examples\n\nTODO\n\n',
    'author': 'uigctaw',
    'author_email': 'uigctaw@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
