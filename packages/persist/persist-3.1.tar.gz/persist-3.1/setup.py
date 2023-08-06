# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['persist', 'persist._contrib', 'persist._contrib.RADLogic']

package_data = \
{'': ['*']}

install_requires = \
['six>=1.15.0,<2.0.0', 'zope.interface>=5.4.0,<6.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=4.0.1,<5.0.0'],
 'doc': ['Sphinx>=3.5.4,<4.0.0',
         'sphinx-rtd-theme>=0.5.2,<0.6.0',
         'nbsphinx>=0.8.4,<0.9.0',
         'mmf-setup>=0.4.0,<0.5.0'],
 'doc:python_version >= "3.7"': ['ipython>=7.23.1,<8.0.0'],
 'test': ['pytest>=6.2.4,<7.0.0', 'pytest-cov>=2.11.1,<3.0.0'],
 'test:python_version < "3.7"': ['scipy>=1.5.4,<2.0.0', 'h5py'],
 'test:python_version >= "3.7" and python_version < "3.10"': ['scipy>=1.6.3,<2.0.0'],
 'test:python_version >= "3.7" and python_version < "4.0"': ['h5py>=3.2.1,<4.0.0']}

setup_kwargs = {
    'name': 'persist',
    'version': '3.1',
    'description': 'Persistent archival of python objects in an importable format.',
    'long_description': 'Persistent Archival of Python Objects\n=====================================\n\n|Documentation Status| |Language grade: Python| |Tests| |Pypi|\n|pyversions|\\ |Code style: black|\n\nPersistent archival of python objects in an importable format.\n\nThis package provides a method for archiving python objects to disk for\nlong-term persistent storage. The archives are importable python\npackages with large data stored in the\n`npy <https://docs.scipy.org/doc/numpy/neps/npy-format.html>`__ numpy\ndata format, or `HDF5 <http://www.hdfgroup.org/HDF5/>`__ files using the\n`h5py <http://www.h5py.org>`__ package (if it is installed). The\noriginal goal was to overcomes several disadvatages of pickles:\n\n1. Archives are relatively stable to code changes. Unlike pickles,\n   changing the underlying code for a class will not change the ability\n   to read an archive if the API does not change.\n2. In the presence of API changes, the archives can be edited by hand to\n   fix them since they are simply python code. (Note: for reliability,\n   the generated code is highly structured and not so "pretty", but can\n   still be edited or debugged in the case of errors due to API\n   changes.)\n3. Efficient storage of large arrays.\n4. Safe for concurrent access by multiple processes.\n\n**Documentation:** http://persist.readthedocs.org\n\n**Source:** https://alum.mit.edu/www/mforbes/hg/forbes-group/persist\n\n**Issues:** https://alum.mit.edu/www/mforbes/hg/forbes-group/issues\n\n.. |Documentation Status| image:: https://readthedocs.org/projects/persist/badge/?version=latest\n   :target: https://persist.readthedocs.io/en/latest/?badge=latest\n.. |Language grade: Python| image:: https://img.shields.io/lgtm/grade/python/g/forbes-group/persist.svg\n   :target: https://lgtm.com/projects/g/forbes-group/persist/context:python\n.. |Tests| image:: https://github.com/forbes-group/persist/actions/workflows/tests.yml/badge.svg\n   :target: https://github.com/forbes-group/persist/actions/workflows/tests.yml\n.. |Pypi| image:: https://img.shields.io/pypi/v/persist.svg\n   :target: https://pypi.python.org/pypi/persist\n.. |pyversions| image:: https://img.shields.io/pypi/pyversions/persist.svg\n   :target: https://pypi.python.org/pypi/persist\n.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n\nInstalling\n----------\n\nThis package can be installed from\n`PyPI <https://pypi.org/project/persist/>`__:\n\n.. code:: bash\n\n    python3 -m pip install persist\n\nor from source:\n\n.. code:: bash\n\n    python3 -m pip install hg+https://alum.mit.edu/www/mforbes/hg/forbes-group/persist\n\nDataSet Format\n==============\n\n.. toctree::\n   :maxdepth: 1\n   \n   notebooks/DataSet Format\n\nAPI\n===\n\n.. toctree::\n   :maxdepth: 3\n\n   api/persist\n\nDeveloper Notes\n===============\n\n.. toctree::\n   :maxdepth: 1\n\n   notebooks/Pickle\n   notebooks/Dev Notes\n\nRelease Notes\n=============\n\nAs of version 3.1, we release only to PyPI using\n```poetry`` <https://python-poetry.org/>`__. Here is the typical\ndevelopment/release cycle.\n\n-  First make sure you have a development environment with Mercurial,\n   the evolve extension, topics enabled, [Black], [Nox], and\n   [nbconvert].\n\n-  Set your virtual environment and run a shell to work in:\n\n``bash    poetry env use python3.8    poetry shell    poetry install -E doc -E test``\n\n-  Start a development branch, i.e.:\n\n   .. code:: bash\n\n       hg branch 3.2\n\n-  Change version to ``\'3.2.dev0\'`` in ``pyproject.toml`` and commit\n   this changes:\n\n   .. code:: bash\n\n       hg com -m "BRN: Start working on branch 3.2"\n       hg push --new-branch -r . \n\n-  Complete your changes making sure code is well tested etc. While\n   working on specific features, you should always use topics:\n\n   .. code:: bash\n\n       hg topic new-feature\n\n   When you push to Heptapod, the commits in these topics will remain in\n   the draft phase, allowing you to rebase, etc. as needed to clean the\n   history. We have setup automatic pushes to\n   `GitHub <https://github.com/forbes-group/persist>`__ and you can see\n   the status of the tests with the badge: |Github Tests|.\n\n   To run the tests locally, you should be able to just run:\n\n   .. code:: bash\n\n       nox\n\n-  Once everything is working and tested, push it to Heptapod and create\n   Merge Requests:\n\n-  First merge all open topics to the development branch.\n\n-  Then change the revision in ``pyproject.toml`` to ``\'3.2\'``, dropping\n   the ``\'.dev\'``. Push this to Heptapod and create a merge request to\n   merge this to the default branch. Review the changes, and complete\n   the Merge. Unlike previously, **do not close the branch.** Just leave\n   it.\n\n-  Start work on next branch::\n\n   .. code:: bash\n\n       hg up 3.2\n       hg branch 3.3\n\nPyPI\n----\n\nTo release on PyPI:\n\n\\`\\`\\`bash poetry build poetry\n\n::\n\n    hg up 3.2\n    poetry build\n\n    python setup.py sdist bdist_wheel\n    twine upload dist/persist-3.2*\n\nAnaconda Cloud\n--------------\n\nTo release on Anaconda Cloud (replace the filename as appropriate):\n\n::\n\n    conda build meta.yaml\n    anaconda upload --all /data/apps/conda/conda-bld/osx-64/persist-3.0-py37_0.tar.bz2\n\n.. |Github Tests| image:: https://github.com/forbes-group/persist/actions/workflows/tests.yml/badge.svg\n   :target: https://github.com/forbes-group/persist/actions/workflows/tests.yml\n\nIndices and Tables\n==================\n\n* :ref:`genindex`\n* :ref:`modindex`\n* :ref:`search`\n',
    'author': 'Michael McNeil Forbes',
    'author_email': 'michael.forbes+python@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://alum.mit.edu/www/mforbes/hg/forbes-group/persist',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
