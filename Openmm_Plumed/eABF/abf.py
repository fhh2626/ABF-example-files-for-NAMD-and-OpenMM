from simtk.openmm.app import *
from simtk.openmm import *
from simtk.unit import *
from sys import stdout, exit, stderr

platform = Platform.getPlatformByName('CPU')
properties = {'Threads': '2'}

psf = CharmmPsfFile('deca-ala.psf')
pdb = PDBFile('deca-ala.pdb')
params = CharmmParameterSet('top_all22_prot.inp','par_all22_prot.inp')
system = psf.createSystem(
    params,
    nonbondedCutoff=1.2*nanometer,
    switchDistance=1.0*nanometer,
    hydrogenMass=1.008*amu)
from openmmplumed import *
import colvars
system.addForce(PlumedForce(colvars.script))
integrator = LangevinIntegrator(300*kelvin, 1/picosecond, 0.0005*picoseconds)
simulation = Simulation(psf.topology, system, integrator, platform, properties)
simulation.context.setPositions(pdb.positions)
simulation.minimizeEnergy()
simulation.reporters.append(DCDReporter('output/abf.dcd', 1000))
simulation.reporters.append(CheckpointReporter('output/abf.chk', 1000))
simulation.reporters.append(StateDataReporter(
    stdout,
    1000,
    step=True,
    volume=True,
    density=True,
    potentialEnergy=True,
    temperature=True,
    speed=True,
    remainingTime=True,
    totalSteps=20000000))
simulation.step(20000000)
