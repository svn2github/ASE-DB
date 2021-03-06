from ase.calculators.octopus import Octopus
from ase.lattice import bulk

system = bulk('Si', orthorhombic=True)

calc = Octopus(label='silicon',
               Spacing=0.25,
               KPointsGrid=[[4, 4, 4]],
               KPointsUseSymmetries=True,
               Output='dos + density + potential',
               OutputHow='xcrysden',
               DosGamma=0.1)

system.set_calculator(calc)
system.get_potential_energy()
