# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ws_rebalancer']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'wealthsimple-trade-python>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['ws-rebalancer = ws_rebalancer.cli:ws_rebalancer']}

setup_kwargs = {
    'name': 'ws-rebalancer',
    'version': '1.0.1',
    'description': 'A CLI tool that helps you rebalance your WealthSimple portfolios.',
    'long_description': "WealthSimple Portfolio Rebalancer\n=\n[![Build Status](https://travis-ci.com/EmilMaric/ws-rebalancer.svg?branch=main)](https://travis-ci.com/EmilMaric/ws-rebalancer)\n[![codecov](https://codecov.io/gh/EmilMaric/ws-rebalancer/branch/main/graph/badge.svg?token=XJ371LIRJB)](https://codecov.io/gh/EmilMaric/ws-rebalancer)\n\nA CLI tool that helps you rebalance your WealthSimple portfolio. The tool takes in a CSV-file that contains the target allocations for your\nportfolio, and prints out a list of buys you should make to bring your portfolio closer to the target allocations you specified.\n\nThe tool will log you in to your WealthSimple account, where it will fetch your current positions & buying power, and will parse the CSV-file you defined to determine how far away each position is from the target allocation. It will then select the positions that are the farthest away from their target positions iteratively, until your buying power is used up.\n\n## Limitations\n- Currently the tool only supports doing buy-only rebalancing, meaning __it won't__ try to simulate any sells in order to rebalance.\n- The tool only works with CAD denominated stocks and assumes your buying power is in CAD. If there is appetite for supporting other currencies then I can try to support that as well.\n- Prices for the stocks are fetched off the WealthSimple Trade API as well, so the quotes may be delayed by 15 minutes.\n\n# Installation\n```\n# To get the latest release\npip install ws-rebalancer\n```\n\n# CSV-file requirements\nTo start, create a CSV file that will contain tickers from assets in your current portfolio, as well as tickers for any new assets you would like to add.\nIn the CSV file, each line will represent a unique asset you own or want to own. On each line, you need to include the correct ticker for the asset and the target allocation for that asset. The format for each line is as follows:\n```\n<stock ticker>, <target allocation>\n```\n\nHere is a sample CSV file:\n```\n# sample-target-allocations.csv\nMSFT, 50%\nAPPL, 30%\nGOOG, 20%\n```\n\nIn other words, I want my sample portfolio to be 50% Microsoft, 30% Apple, and 20% Google.\n\nMake sure that the target allocations add up to 100%. The tool will raise an error and quit if that is not the case. You can also use decimals to represent fractional target allocations. Also don't repeat the same ticker twice. I've tried my best to sanitize the input and raise any errors that I can forsee with the CSV-file, but there may be some things that I didn't catch so please be careful.\n\n# Usage\nTo generate the buys that will rebalance your portfolio as close as possible to the target allocation, run the tool as follows:\n```\n$ ws-rebalancer rebalance -t <target-allocations-CSV-file> --email <WealthSimple-email-login> [--2fa]\n```\n\nUsing our `sample-target-allocations.csv` as above, a sample run could look as follows:\n```\n$ ws-rebalancer rebalance -t sample-target-allocations.csv --email test@gmail.com --2fa\nPassword:\nRepeat for confirmation:\nEnter 2FA code: 12345\n0. non-registered\nPlease input the account you want: 0\nBuy 5X MSFT @ 10.00 - New allocation 40.00%\nBuy 1X APPL @ 20.00 - New allocation 30.00%\nBuy 1X GOOG @ 30.00 - New allocation 30.00%\nRemaining cash $0.00\n```\nNote that in this example, `MSFT` price was $10.00, `APPL` price was $20.00, and `GOOG` price was $30.00, and we had a buying power of $60.00 in this\naccount (although it is not shown). The tool also fetched our current positions and buying power for the specified account and then provided a list of\nbuys we should make in order to try to meet the specified target allocations.\n\n# Finding Issues\nIf you find issues using this tool, please create an Issue using the [Github issue tracker](https://github.com/EmilMaric/ws-rebalancer/issues)\nand I will try to address it as soon as I can.\n\n# Contributing\nIf you would like to contribute, please read the [CONTRIBUTING.md](https://github.com/EmilMaric/ws-rebalancer/blob/main/CONTRIBUTING.md) page\n",
    'author': 'Emil Maric',
    'author_email': 'emil.maric@hotmail.com',
    'maintainer': 'Emil Maric',
    'maintainer_email': 'emil.maric@hotmail.com',
    'url': 'https://github.com/EmilMaric/ws-rebalancer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
