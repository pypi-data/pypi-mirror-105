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
    'version': '0.1.1',
    'description': 'French Crypto Tax Return for Humans',
    'long_description': '# Coin2086: French Crypto Tax Return for Humans #\n\nCoin2086 is as Python module that helps French tax residents to fill their\ncrypto-currency tax return ([Formulaire n°2086](https://www.impots.gouv.fr/portail/formulaire/2086/declaration-des-plus-ou-moins-values-de-cessions-dactifs-numeriques)).\n\nFrench tax authorities requires tax residents to provide a lot of information\nfor each crypto-currency sale they performed during the last tax year.\nCoin2086 simply takes your trades as input, and returns a DataFrame with all\nthe information you need to report on [Formulaire n°2086](https://www.impots.gouv.fr/portail/formulaire/2086/declaration-des-plus-ou-moins-values-de-cessions-dactifs-numeriques).\n\nIt\'s that easy !\n\n[Documentation on Read The Docs](https://coin2086.readthedocs.io)\n\n## Installation ##\n\n```sh\npip install coin2086\n```\n\n## Basic Usage ##\n\n```python\n    import pandas as pd\n    import coin2086\n    trades = pd.read_csv(\'trades.csv\')\n    form2086, tax_base = coin2086.compute_taxable_pnls(trades, 2020)\n    expected_tax = 0.3 * tax_base\n    print(f"Taxable base for 2020 crypto-currency sales: {tax_base:.2f}")\n    print(f"Expected tax amount: {expected_tax:.2f}")\n    print("Information that needs to be reported on Formulaire n°2086")\n    print(form2086)\n```\n',
    'author': 'Fabien André',
    'author_email': 'fabien.andre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fandre90/coin2086',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
