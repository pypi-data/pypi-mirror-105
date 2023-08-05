# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ment']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['m = ment.main:main']}

setup_kwargs = {
    'name': 'ment',
    'version': '0.1.5',
    'description': 'python library to write daily log in markdown quickly and to synthesize daily logs based on category',
    'long_description': '# ment\n## what is this?\nment is a python library to write daily log in markdown quickly and to synthesize daily logs based on category.\n\n## prerequisities\n- vim\n## installation\n```\npip install ment\n```\n## usage\n#### start editting\n```\nm\n```\nThen, starts to edit `~/ment_dir/<todays_date>/diary.md`\n\n#### synthesize by tag\n```\nm --synthe <tag_name>\n```\nThen, it extracts contents followed by "# <tag_name>" from daily logs,\nand outputs `~/ment_dir/synthe/<tag_name>/synthe_<tag_name>.md`.\n\nIf you want to list tags,`m -l`\n\n\n## directory structure\n```\n~/ment_dir/\n├── 2021-03-27\n│\xa0\xa0 └── diary.md\n├── 2021-03-28\n│\xa0\xa0 └── diary.md\n├── 2021-03-29\n│\xa0\xa0 └── diary.md\n├── 2021-03-30\n│\xa0\xa0 └── diary.md\n└── synthe\n    ├── tag1\n    │\xa0\xa0 └── synthe_tag1.md\n    ├── tag2\n    │\xa0\xa0 └── synthe_tag2.md\n    ├── tag3\n    │\xa0\xa0 └── synthe_tag3.md\n    └── weeks.md\n\n```\n',
    'author': 'kawagh',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kawagh/ment',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
