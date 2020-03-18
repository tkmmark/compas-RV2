"""
********************************************************************************
compas_rv2
********************************************************************************

.. currentmodule:: compas_rv2


.. toctree::
    :maxdepth: 1


"""

from __future__ import print_function

import os
import logging


__author__ = ['tom van mele <van.mele@arch.ethz.ch>']
__copyright__ = 'Block Research Group - ETH Zurich'
__license__ = 'MIT License'
__email__ = 'van.mele@arch.ethz.ch'
__version__ = '0.1.0'


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, '../../'))
DATA = os.path.abspath(os.path.join(HOME, 'data'))
DOCS = os.path.abspath(os.path.join(HOME, 'docs'))
TEMP = os.path.abspath(os.path.join(HOME, 'temp'))

# setting up logger
log_path = os.path.join(HERE, 'dev.log')
logging.basicConfig(
    filename=log_path,
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    )

__all__ = ['HOME', 'DATA', 'DOCS', 'TEMP']
