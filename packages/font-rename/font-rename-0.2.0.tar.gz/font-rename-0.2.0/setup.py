# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['font_rename']
install_requires = \
['cchardet>=2.1.7,<3.0.0', 'fonttools>=4.16.0,<5.0.0']

entry_points = \
{'console_scripts': ['font-rename = font_rename:main']}

setup_kwargs = {
    'name': 'font-rename',
    'version': '0.2.0',
    'description': 'Renames fonts to their internal name and unpacks .ttc/.otc files.',
    'long_description': '# font-rename\n\nRenames fonts to their internal name and unpacks .ttc/.otc files.\n\n```bash\npip install font-rename\nfont-rename insert/directory/file/path/here\n```\n\n## Changelog\n\n### v0.2.0\n\n- Add the option to remove unparsable fonts [#11](https://github.com/whtsky/font-rename/pull/11)\n- Add `.otc` support [#9](https://github.com/whtsky/font-rename/pull/9)\n- Fix invalid .ttc handling [#9](https://github.com/whtsky/font-rename/pull/9)\n\n### v0.1.0\n\n- Initial Release',
    'author': 'Wu Haotian',
    'author_email': 'whtsky@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whtsky/font-rename/',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
