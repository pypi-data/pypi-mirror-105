craterpy |RtdBadge|_ |PyPiBadge|_ |CodecovBadge|_ |ZenodoBadge|_
================================================================================================
.. |ZenodoBadge| image:: https://zenodo.org/badge/88457986.svg
.. _ZenodoBadge: https://zenodo.org/badge/latestdoi/88457986

.. |RtdBadge| image:: http://readthedocs.org/projects/craterpy/badge/?version=latest
.. _RtdBadge: http://craterpy.readthedocs.io/en/latest/?badge=latest

.. |PyPiBadge| image:: https://badge.fury.io/py/craterpy.svg
.. _PyPiBadge: https://badge.fury.io/py/craterpy

.. |CodecovBadge| image:: https://codecov.io/gh/cjtu/craterpy/branch/trunk/graph/badge.svg?token=9K567x0YUJ
.. _CodecovBadge: https://codecov.io/gh/cjtu/craterpy

Overview
--------
Welcome to craterpy (formerly *ACERIM*), your one-stop shop to crater data science in Python!

This package is in the alpha stage of development. You can direct any questions to Christian at cj.taiudovicic@gmail.com. Bug reports and feature requests can be opened as issues at the `issues`_ board on GitHub.

You can use craterpy to:

  - work with tables of crater data in Python (using pandas)
  - load and manipulate image data in Python (using rasterio)
  - extract, mask, filter, and compute stats on craters located in your images
  - plot crater data in python!

Craterpy currently only supports simple cylindrical images and requires you to provide a table of crater locations and sizes (e.g. it isn't a crater detection program). See the example below!

Example
-------
Craterpy in action::

    import pandas as pd
    from craterpy import dataset, stats
    df = pd.DataFrame({'Name': ["Orientale", "Langrenus", "Compton"],
                       'Lat': [-19.9, -8.86, 55.9],
                       'Lon': [-94.7, 61.0, 104.0],
                       'Rad': [147.0, 66.0, 82.3]})
    moon = dataset.CraterpyDataset("moon.tif")
    stat_df = cs.ejecta_stats(df, moon, 4, ['mean', 'median', 'std'], plot=True)


.. image:: https://raw.githubusercontent.com/cjtu/craterpy/trunk/craterpy/data/_images/readme_crater_ejecta.png

::

  stats_df.head()

.. image:: https://raw.githubusercontent.com/cjtu/craterpy/trunk/craterpy/data/_images/readme_stat_df.png


New users should start with the IPython notebook `tutorial`_ for typical usage with examples.

**Note**: This package currently **only accepts image data in simple-cylindrical (Plate Caree) projection**. If your data is in another projection, please reproject it to simple-cylindrical before importing it with craterpy. If you would like add reprojection functionality to craterpy, consider `Contributing`_.

.. _`tutorial`: https://gist.github.com/cjtu/560f121049b342aa0b2bf70e038358b7


Requires
--------
Craterpy requires python >3.7 and is tested on Ubuntu and OS X. If you would like to use craterpy on Windows, we recommend getting the Windows Subsystem for Linux (`WSL`_) and installing it from the bash shell.

.. _`WSL`: https://docs.microsoft.com/en-us/windows/wsl/install-win10

It's core dependencies are:

- rasterio
- pandas
- numpy
- matplotlib

Installation
------------

The most reliable way to get craterpy is by installing `git <https://git-scm.com>`_ and `poetry <https://python-poetry.org/docs/>`_ to clone and install the package.

You can clone and install craterpy with the following steps::

    # Clone this repository
    $ cd ~
    $ git clone https://github.com/cjtu/craterpy.git

    # Enter the repository
    $ cd craterpy

    # Configure poetry
    poetry config virtualenvs.create true --local
    poetry config virtualenvs.in-project true --local

    # Install craterpy with poetry
    $ poetry install

    # Check installation
    poetry version

    # Either open a Jupyter server
    $ poetry run jupyter notebook

    # Or activate the venv from your Python editor of choice
    # The venv is path is ~/craterpy/.venv/bin/python

Installing from pip
-------------------

Craterpy is also listed on `PYPI <https://pypi.org/project/craterpy/>`_ and can be installed with `pip <https://packaging.python.org/tutorials/installing-packages/>`_::

    pip install craterpy
    python -c "import craterpy; print(craterpy.__version__)"

Installing into a conda environment
-----------------------------------

You can similarly install craterpy into a `conda environment`_ using pip::

    # Create conda environment
    conda create -n craterpy python=3.7

    # Activate the environment
    conda activate craterpy

    # Install dependencies (optional, but may fix dependency issues on some platforms)
    conda install -c conda-forge rasterio pandas, numpy, matplotlib

    # Install craterpy
    pip install craterpy

    # Test installation
    python -c "import craterpy; print(craterpy.__version__)"

Trouble installing craterpy? Let us know on the `issues`_ board.

Now that you have craterpy installed, head over to the `tutorial`_ to get started!

.. _`conda environment`: https://conda.io/docs/using/envs

Installing from a fork
^^^^^^^^^^^^^^^^^^^^^^

1. Fork this project from `craterpy on GitHub`_.
2. Clone your fork locally
3. Navigate to the craterpy root directory and install with::

    python setup.py install

**Warning**: This installs the newest craterpy updates which may not be production stable. Installing from pip automatically pulls the previous stable release.

.. _`craterpy on GitHub`: https://github.com/cjtu/craterpy

Documentation
-------------

API documentation is available at `readthedocs <https://readthedocs.org/projects/craterpy/>`_.


Contributing
------------
There are two major ways you can help improve craterpy:

Bug Reporting and Feature Requests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You can report bugs or request new features on the `issues`_ board. If you are reporting a bug, please give a detailed description about how it came up and what your build environment is (e.g. with ``conda list``).

.. _`issues`: https://github.com/cjtu/craterpy/issues

Becoming a contributor
^^^^^^^^^^^^^^^^^^^^^^
craterpy is seeking new contributors! If you are interested in open source and want to join a supportive learning environment - or if you want to extend craterpy to suit your own crater analysis - consider contributing to the project! See `CONTRIBUTING.rst`_ for details on how to get started.

.. _`CONTRIBUTING.rst`: https://github.com/cjtu/craterpy/blob/master/CONTRIBUTING.rst

Development Environment
"""""""""""""""""""""""
The development environment is specified in `.environment.yml`. It can be built automatically in a new conda environment in a few simple steps:

1. Fork `craterpy on GitHub`_.

2. Clone your fork, then cd into your local craterpy repository.

3. Install the dependencies using poetry (steps above).

4. Run a jupyter notebook with::

    poetry run jupyter notebook

5. Test your changes::

    poetry run pytest craterpy

6. Apply code formatting with black::

    poetry run black craterpy

7. Run pylint to check your code style::

    poetry run pylint craterpy

8. Hack away!

Read more about testing, contributing and style in `CONTRIBUTING.rst`_.


Citing craterpy
---------------

For convenience, this project uses the `MIT Licence <https://github.com/cjtu/craterpy/blob/master/LICENSE.txt>`_ for warranty-free ease of use and distribution. The author simply asks that you cite the project when using it in published research. The `citable DOI <https://zenodo.org/badge/latestdoi/88457986>`_ can be found at Zenodo by clicking the badge below.

.. image:: https://zenodo.org/badge/88457986.svg
    :target: https://zenodo.org/badge/latestdoi/88457986

To read more about citable code, check out `Zenodo <http://help.zenodo.org/features>`_.


Contact
-------
If you have comments/question/concerns or just want to get in touch, you can email Christian at cj.taiudovicic@gmail.com or follow `@TaiUdovicic <https://twitter.com/TaiUdovicic>`_ on Twitter.


License
-------

Copyright (c) 2021- Christian Tai Udovicic. Released under the MIT license. This software comes with no warranties. See `LICENSE <https://github.com/cjtu/craterpy/blob/master/LICENSE.txt>`_ for details.


Contributors
------------
Craterpy was developed with the aid of `these wonderful people <https://github.com/cjtu/craterpy/graphs/contributors>`_!
