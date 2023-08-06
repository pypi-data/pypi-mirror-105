# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_mcstatus']

package_data = \
{'': ['*']}

install_requires = \
['mcstatus>=5.2.0,<6.0.0',
 'nonebot-adapter-cqhttp>=2.0.0a13,<3.0.0',
 'nonebot-plugin-apscheduler>=0.1.2,<0.2.0',
 'nonebot2>=2.0.0-alpha.11,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-mcstatus',
    'version': '0.1.0',
    'description': 'Check Minecraft server status',
    'long_description': '# Nonebot Plugin MCStatus\n\n基于 [nonebot2](https://github.com/nonebot/nonebot2) 和 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的 Minecraft 服务器状态查询插件\n\n[![License](https://img.shields.io/github/license/Jigsaw111/nonebot_plugin_mcstatus)](LICENSE)\n![Python Version](https://img.shields.io/badge/python-3.7.3+-blue.svg)\n![NoneBot Version](https://img.shields.io/badge/nonebot-2.0.0a11+-red.svg)\n![Pypi Version](https://img.shields.io/pypi/v/nonebot-plugin-mcstatus.svg)\n\n### 安装\n\n#### 从 PyPI 安装（推荐）\n\n- 使用 nb-cli  \n\n```\nnb plugin install nonebot_plugin_mcstatus\n```\n\n- 使用 poetry\n\n```\npoetry add nonebot_plugin_mcstatus\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_mcstatus\n```\n\n#### 从 GitHub 安装（不推荐）\n\n```\ngit clone https://github.com/Jigsaw111/nonebot_plugin_mcstatus.git\n```\n\n### 使用\n\n### Bug\n\n### To Do\n\n### Changelog\n',
    'author': 'Jigsaw',
    'author_email': 'j1g5aw@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Jigsaw111/nonebot_plugin_puppet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
