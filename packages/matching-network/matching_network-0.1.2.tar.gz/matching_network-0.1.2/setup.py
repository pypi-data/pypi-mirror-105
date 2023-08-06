# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['matching_network']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'quantiphy>=2.13.0,<3.0.0']

entry_points = \
{'console_scripts': ['my-script = matching_network.__main__:cli']}

setup_kwargs = {
    'name': 'matching-network',
    'version': '0.1.2',
    'description': 'Design lumped-parameters matching networks (L-sections)',
    'long_description': '<div align="right" style="text-align:right"><i><a href="https://urbanij.github.io/">Francesco Urbani</a></i></div>\n\n<!-- Index of Jupyter (IPython) Notebooks -->\n\n|Title                                                                                                           |\n|----------------------------------------------------------------------------------------------------------------|\n|<a href="https://github.com/urbanij/matching-network/blob/master/aux/L-section_matching_calculations.ipynb">L-section_matching_calculations</a>|\n|<a href="https://github.com/urbanij/matching-network/blob/master/aux/calculations.ipynb">Calculations</a>                                      |\n|<a href="https://github.com/urbanij/matching-network/blob/master/aux/demo_matching_network.ipynb">Demo</a>                                     |\n\n\n\n---\n\n\n[![Downloads](https://pepy.tech/badge/matching-network)](https://pepy.tech/project/matching-network)\n\n\nInstallation\n============\n\n```sh\npip install matching_network\n```\n\n\nDocumentation\n=============\n\n\n```python\n>>> import matching_network as mn\n>>>\n>>> impedance_you_have         = 90 + 32j # Ω\n>>> impedance_you_want_to_have = 175      # Ω\n>>>\n>>> frequency                  = 900e6    # Hz\n>>>\n>>> mn.L_section_matching(impedance_you_have, impedance_you_want_to_have, frequency).match()\nFrom (90+32j) Ω to 175 Ω\n\nnormalized starting impedance = (90+32j)Ω/175Ω = 0.51429+0.18286j\n\n#solutions: 2\n\nseries-shunt\n    Series Inductor:\n    X = 55.464 Ω ⇔ B = -18.03 mS\n    L = 9.8082 nH  (@ 900 MHz)\n    Shunt Capacitor:\n    X = -180.07 Ω ⇔ B = 5.5533 mS\n    C = 982.04 fF  (@ 900 MHz)\n\nseries-shunt\n    Series Capacitor:\n    X = -119.46 Ω ⇔ B = 8.3707 mS\n    C = 1.4803 pF  (@ 900 MHz)\n    Shunt Inductor:\n    X = 180.07 Ω ⇔ B = -5.5533 mS\n    L = 31.844 nH  (@ 900 MHz)\n\n>>>\n```\n\n\nOr, straight from the CLI:\n```bash\n$ python -c "import matching_network as mn; print(mn.L_section_matching(100, 20+43j, 1e9).match())"\n```\n```\nFrom 100 Ω to (20+43j) Ω\n\nnormalized starting impedance = 100Ω / (20+43j)Ω = 0.88928-1.912j\n\n#solutions: 4\n\nshunt-series\n\tShunt Inductor:\n\tX = 50 Ω ⇔ B = -20 mS\n\tL = 7.9577 nH  (@ 1 GHz)\n\tSeries Inductor:\n\tX = 3 Ω ⇔ B = -333.33 mS\n\tL = 477.46 pH  (@ 1 GHz)\nshunt-series\n\tShunt Capacitor:\n\tX = -50 Ω ⇔ B = 20 mS\n\tC = 3.1831 pF  (@ 1 GHz)\n\tSeries Inductor:\n\tX = 83 Ω ⇔ B = -12.048 mS\n\tL = 13.21 nH  (@ 1 GHz)\nseries-shunt\n\tSeries Inductor:\n\tX = 35.285 Ω ⇔ B = -28.341 mS\n\tL = 5.6157 nH  (@ 1 GHz)\n\tShunt Inductor:\n\tX = 62.571 Ω ⇔ B = -15.982 mS\n\tL = 9.9585 nH  (@ 1 GHz)\nseries-shunt\n\tSeries Capacitor:\n\tX = -35.285 Ω ⇔ B = 28.341 mS\n\tC = 4.5106 pF  (@ 1 GHz)\n\tShunt Inductor:\n\tX = 44.929 Ω ⇔ B = -22.257 mS\n\tL = 7.1507 nH  (@ 1 GHz)\n```\n',
    'author': 'Francesco Urbani',
    'author_email': 'francescourbanidue@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/matching-network/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
