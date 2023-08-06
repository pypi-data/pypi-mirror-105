# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coin2086']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.1,<2.0', 'requests>=2.10,<3.0']

setup_kwargs = {
    'name': 'coin2086',
    'version': '0.1.2',
    'description': 'French Crypto Taxes Made Easy',
    'long_description': '# Coin2086 #\n\n> Crypto Taxes Made Easy ! 📒\n\n[![PyPI Version][pypi-image]][pypi-url]\n[![PyPI Python Version][pypi-version-image]][pypi-url]\n[![PyPI License][pypi-license-image]][pypi-url]\n[![Documentation Status][rtd-image]](https://coin2086.readthedocs.io/en/latest/?badge=latest)\n[![Binder][binder-img]][binder-url]\n\nCoin2086 is a Python module that makes it easy for French tax residents to\nfill their crypto-currency tax return.\n\nTax autorities requires French tax residents to report their profit and losses\n(PnL) on each of their cryto-currency sales of the previous year on\n[Formulaire n°2086][form2086-url].\n\nThe formula to compute your profit and losses, detailed on [Formulaire n°2086][form2086-url],\nrequires you to valuate your *whole* crypto-currency portfolio every time you sell,\nand keep track of the amount of initial investment capital that was sold. This\naccounting is tedious to do by hand.\n\nCoin2086 does all of that automatically for you. It takes your trades as input,\nvaluates your cryptocurrency portfolio, computes your taxable profit and outputs\nthe *exact* information you need to fill on [Formulaire n°2086][form2086-url].\n\nIt\'s that simple !\n\n📖  Documentation: https://coin2086.readthedocs.io/  \n📦  PyPI Package: https://pypi.org/project/coin2086/  \n📝  Example Jupyter Notebook: [Launch on Binder][binder-url]  \n💻  GitHub Project: https://github.com/fandre90/coin2086  \n\n[form2086-url]: https://www.impots.gouv.fr/portail/formulaire/2086/declaration-des-plus-ou-moins-values-de-cessions-dactifs-numeriques\n[binder-img]: https://mybinder.org/badge_logo.svg\n[binder-url]: https://mybinder.org/v2/gh/fandre90/coin2086/HEAD?filepath=notebooks%2FCoin2086%20Example%20Use.ipynb\n[pypi-image]: https://img.shields.io/pypi/v/coin2086\n[pypi-version-image]: https://img.shields.io/pypi/pyversions/coin2086\n[pypi-license-image]: https://img.shields.io/pypi/l/coin2086\n[pypi-url]: https://pypi.org/project/coin2086/\n[rtd-image]: https://readthedocs.org/projects/coin2086/badge/?version=latest\n\n## Installation ##\n\n```sh\npip install coin2086\n```\n\nAlternatively, you may use the [Binder Notebook][binder-url] directly in your browser\n\n## Basic Usage ##\n\n```python\n>>> import pandas as pd\n>>> import coin2086\n>>> trades = pd.read_csv(\'trades.csv\')\n>>> trades\n             datetime trade_side cryptocurrency  quantity     price base_currency      amount        fee\n0 2019-10-19 11:10:00        BUY            BTC      1.00   7149.38           EUR   7149.3800  35.746900\n1 2019-11-14 19:50:00       SELL            BTC      0.50   7844.88           EUR   3922.4400  19.612200\n2 2020-07-28 10:20:00        BUY            BTC      2.00   9262.42           EUR  18524.8400  92.624200\n3 2020-09-01 12:20:00        BUY            ETH      5.00    393.58           EUR   1967.9000   9.839500\n4 2020-09-05 16:50:00       SELL            BTC      1.00   8722.70           EUR   8722.7000  43.613500\n5 2020-09-08 12:40:00       SELL            ETH      5.00    285.07           EUR   1425.3500   7.126750\n6 2020-12-20 09:10:00       SELL            BTC      0.25  19223.90           EUR   4805.9750  24.029875\n7 2021-03-13 23:40:00       SELL            BTC      0.25  50025.17           EUR  12506.2925  62.531463\n\n>>> year = 2020\n>>> form2086, taxable_profit = coin2086.compute_taxable_pnls(trades, year=year)\n>>> print(f"Total taxable profit for year {year}: {taxable_profit:.2f} euros")\nTotal taxable profit for year 2020: 2038.50 euros\n>>> form2086\n     Description  ... Plus-values et moins-values [pnl]\n4  SELL 1.00 BTC  ...                       -371.708792\n5  SELL 5.00 ETH  ...                       -102.332358\n6  SELL 0.25 BTC  ...                       2512.542417\n\n[3 rows x 10 columns]\n```\n\nFor more information, check out the \n[documentation](https://coin2086.readthedocs.io/) or the\n[example notebook][binder-url]\n',
    'author': 'Fabien André',
    'author_email': 'fabien.andre90@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fandre90/coin2086',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
