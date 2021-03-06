# -*- coding: utf-8 -*-

import numpy as np

from ase.utils.sjeos import EquationOfStateSJEOS

try:
    # ase.utils.eosase2 requires scipy
    import scipy
    from ase.utils.eosase2 import EquationOfStateASE2

    class EquationOfState:
        """Fit equation of state for bulk systems.

        The following equation is used::

           sjeos (default)
               A third order inverse polynomial fit 10.1103/PhysRevB.67.026103

                               2      3        -1/3
           E(V) = c + c t + c t  + c t ,  t = V
                   0   1     2      3

           taylor
               A third order Taylor series expansion about the minimum volume

           murnaghan
               PRB 28, 5480 (1983)

           birch
               Intermetallic compounds: Principles and Practice,
               Vol I: Principles. pages 195-210

           birchmurnaghan
               PRB 70, 224107

           pouriertarantola
               PRB 70, 224107

           vinet
               PRB 70, 224107

           antonschmidt
               Intermetallics 11, 23-32 (2003)

           p3
               A third order polynomial fit

        Use::

           eos = EquationOfState(volumes, energies, eos='sjeos')
           v0, e0, B = eos.fit()
           eos.plot()

        """
        def __init__(self, volumes, energies, eos='sjeos'):
            if eos == 'sjeos':
                eosclass = EquationOfStateSJEOS
            else:
                eosclass = EquationOfStateASE2  # old ASE2 implementation
            self._impl = eosclass(volumes, energies, eos)

        def fit(self):
            return self._impl.fit()

        def plot(self, filename=None, show=None):
            return self._impl.plot(filename, show)

except ImportError:
    # ase.utils.sjeos requires only numpy
    EquationOfState = EquationOfStateSJEOS
    
    
if __name__ == '__main__':
    import pickle
    import sys
    v, e = pickle.load(sys.stdin)
    eos = EquationOfState(v, e)
    eos.plot()
