from .absorber import BlackAbsorber
from .k2_collimator import K2Collimator, K2Crystal
from .geant4_collimator import Geant4Collimator

_all_collimator_types = { BlackAbsorber, K2Collimator, K2Crystal, Geant4Collimator }
