# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csrank',
 'csrank.choicefunction',
 'csrank.core',
 'csrank.dataset_reader',
 'csrank.dataset_reader.choicefunctions',
 'csrank.dataset_reader.discretechoice',
 'csrank.dataset_reader.dyadranking',
 'csrank.dataset_reader.labelranking',
 'csrank.dataset_reader.objectranking',
 'csrank.deprecated',
 'csrank.discretechoice',
 'csrank.dyadranking',
 'csrank.modules',
 'csrank.modules.scoring',
 'csrank.objectranking',
 'csrank.tests']

package_data = \
{'': ['*'], 'csrank.deprecated': ['hotel_dataset/*', 'university_dataset/*']}

install_requires = \
['arviz>=0.10,<0.11.1',
 'numpy>=1.12.1,<2.0.0',
 'pymc3>=3.8,<4.0',
 'scikit-learn>=0.23,<0.24',
 'scipy>=1.2,<2.0',
 'skorch>=0.9,<0.11',
 'torch>=1.8.0,<2.0.0']

extras_require = \
{'data': ['psycopg2-binary>=2.7,<3.0',
          'pandas>=1.1.1,<2.0.0',
          'h5py>=3.0,<4.0',
          'joblib>=0.16.0,<1.0'],
 'docs': ['Sphinx>=3.2.1,<4.0.0',
          'sphinx_rtd_theme>=0.5.0,<0.6.0',
          'sphinxcontrib-bibtex>=1.0.0,<2.0.0',
          'nbsphinx>=0.7.1,<0.8.0',
          'IPython>=7.18.1,<8.0.0'],
 'hypervolume': ['pygmo>=2.7,<3.0']}

setup_kwargs = {
    'name': 'csrank',
    'version': '2.0.0rc2',
    'description': 'Context-sensitive ranking and choice',
    'long_description': '|Coverage| |Binder|\n\n****\nNOTE\n****\n\nThis library has recently been migrated from tensorflow to PyTorch. The 2.0\nversion marks a breaking change. Some of the previous functionality is now\nunavailable and some classes behave differently. You can use the latest 1.x\nrelease if you are looking for the tensorflow based estimators.\n\n*******\nCS-Rank\n*******\n\nCS-Rank is a Python package for context-sensitive ranking and choice\nalgorithms.\n\nWe implement the following new object ranking/choice architectures:\n\n* FATE (First aggregate then evaluate)\n* FETA (First evaluate then aggregate)\n\nIn addition, we also implement these algorithms for choice functions:\n\n* RankNetChoiceFunction\n* GeneralizedLinearModel\n* PairwiseSVMChoiceFunction\n\nThese are the state-of-the-art approaches implemented for the discrete choice\nsetting:\n\n* GeneralizedNestedLogitModel\n* MixedLogitModel\n* NestedLogitModel\n* PairedCombinatorialLogit\n* RankNetDiscreteChoiceFunction\n* PairwiseSVMDiscreteChoiceFunction\n\n\nGetting started\n===============\nAs a simple "Hello World!"-example we will try to learn the Pareto problem:\n\n.. code-block:: python\n\n   import csrank as cs\n   from csrank import ChoiceDatasetGenerator\n   gen = ChoiceDatasetGenerator(dataset_type=\'pareto\',\n                                   n_objects=30,\n                                   n_features=2)\n   X_train, Y_train, X_test, Y_test = gen.get_single_train_test_split()\n\nAll our learning algorithms are implemented using the scikit-learn estimator\nAPI. Fitting our FATENet architecture is as simple as calling the ``fit``\nmethod:\n\n.. code-block:: python\n\n   fate = cs.FATEChoiceFunction()\n   fate.fit(X_train, Y_train)\n\nPredictions can then be obtained using:\n\n.. code-block:: python\n\n   fate.predict(X_test)\n\n\nInstallation\n------------\nThe latest release version of CS-Rank can be installed from Github as follows::\n\n   pip install git+https://github.com/kiudee/cs-ranking.git\n\nAnother option is to clone the repository and install CS-Rank using::\n\n   python setup.py install\n\n\nDependencies\n------------\nCS-Rank depends on PyTorch, skorch, NumPy, SciPy, matplotlib, scikit-learn,\njoblib and tqdm. For data processing and generation you will\nalso need PyGMO, H5Py and pandas.\n\nCiting CS-Rank\n----------------\nYou can cite our `arXiv papers`_::\n\n\n\n  @article{csrank2019,\n    author    = {Karlson Pfannschmidt and\n                 Pritha Gupta and\n                 Eyke H{\\"{u}}llermeier},\n    title     = {Learning Choice Functions: Concepts and Architectures },\n    journal   = {CoRR},\n    volume    = {abs/1901.10860},\n    year      = {2019}\n  }\n\n  @article{csrank2018,\n    author    = {Karlson Pfannschmidt and\n                 Pritha Gupta and\n                 Eyke H{\\"{u}}llermeier},\n    title     = {Deep architectures for learning context-dependent ranking functions},\n    journal   = {CoRR},\n    volume    = {abs/1803.05796},\n    year      = {2018}\n  }\n\nLicense\n--------\n`Apache License, Version 2.0 <https://github.com/kiudee/cs-ranking/blob/master/LICENSE>`_\n\n.. |Binder| image:: https://mybinder.org/badge_logo.svg\n   :target: https://mybinder.org/v2/gh/kiudee/cs-ranking/master?filepath=docs%2Fnotebooks\n\n.. |Coverage| image:: https://codecov.io/gh/kiudee/cs-ranking/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/kiudee/cs-ranking\n\n..\n  |Build Status| image:: https://img.shields.io/github/workflow/status/kiudee/cs-ranking/tests\n  :target: https://github.com/kiudee/cs-ranking/actions\n  :alt: GitHub Workflow Status\n\n\n.. _interactive notebooks: https://mybinder.org/v2/gh/kiudee/cs-ranking/master?filepath=docs%2Fnotebooks\n.. _arXiv papers: https://arxiv.org/search/cs?searchtype=author&query=Pfannschmidt%2C+K\n',
    'author': 'Karlson Pfannschmidt',
    'author_email': 'kiudee@mail.upb.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kiudee/cs-ranking',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
