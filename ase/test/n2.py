from ase import *

n2 = Atoms('N2', positions=[(0, 0, 0), (0, 0, 1.1)],
           calculator=EMT())
QuasiNewton(n2).run(0.01)
print n2.distance(0, 1), n2.get_potential_energy()
