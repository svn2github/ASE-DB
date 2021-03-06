from __future__ import print_function
import sys

import numpy as np
from ase import Atoms
from ase.io import write, read, iread
from ase.io.formats import all_formats, get_ioformat
from ase.calculators.singlepoint import SinglePointCalculator

try:
    import matplotlib
except ImportError:
    matplotlib = 0

try:
    from lxml import etree
except ImportError:
    etree = 0
    
a = 5.0
d = 1.9
c = a / 2
atoms = Atoms('AuH',
              positions=[(0, c, c), (d, c, c)],
              cell=(2 * d, a, a),
              pbc=(1, 0, 0))
extra = np.array([2.3, 4.2])
atoms.set_array('extra', extra)
atoms *= (2, 1, 1)

# attach some results to the Atoms. These are serialised by the extxyz writer.
spc = SinglePointCalculator(atoms,
                            energy=-1.0,
                            stress=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
                            forces=-1.0 * atoms.positions)
atoms.set_calculator(spc)
images = [atoms, atoms]


def check(a, format):
    assert abs(a.positions - atoms.positions).max() < 1e-6, (a.positions -
                                                             atoms.positions)
    if format in ['traj', 'cube', 'cfg', 'struct', 'gen', 'extxyz',
                  'db', 'json', 'trj']:
        assert abs(a.cell - atoms.cell).max() < 1e-6
    if format in ['cfg', 'extxyz']:
        assert abs(a.get_array('extra') -
                   atoms.get_array('extra')).max() < 1e-6
    if format in ['extxyz', 'traj', 'trj', 'db', 'json']:
        assert (a.pbc == atoms.pbc).all()
        assert a.get_potential_energy() == atoms.get_potential_energy()
        assert (a.get_stress() == atoms.get_stress()).all()
        assert abs(a.get_forces() - atoms.get_forces()).max() < 1e-12
    
for format in all_formats:
    if format in ['abinit', 'castep-cell', 'dftb', 'eon', 'gaussian']:
        # Someone should do something ...
        continue
        
    if format in ['postgresql', 'trj', 'vti', 'vtu']:
        # Let's not worry about these.
        continue
    
    if sys.version_info[0] == 3 and format in ['bundletrajectory', 'cif']:
        continue

    if not matplotlib and format in ['eps', 'png']:
        continue

    if not etree and format == 'exciting':
        continue
        
    io = get_ioformat(format)
    print('{0:20}{1}{2}{3}{4}'.format(format,
                                      ' R'[bool(io.read)],
                                      ' W'[bool(io.write)],
                                      '+1'[io.single],
                                      'SF'[io.acceptsfd]))
    fname1 = 'io-test.1.' + format
    fname2 = 'io-test.2.' + format
    if io.write:
        write(fname1, atoms, format=format)
        if not io.single:
            write(fname2, images, format=format)

        if io.read:
            for a in [read(fname1, format=format), read(fname1)]:
                check(a, format)
            
            if not io.single:
                if format in ['json', 'db']:
                    aa = read(fname2 + '@id=1') + read(fname2 + '@id=2')
                else:
                    aa = [read(fname2), read(fname2, 0)]
                aa += read(fname2, ':')
                for a in iread(fname2, format=format):
                    aa.append(a)
                assert len(aa) == 6
                for a in aa:
                    check(a, format)
