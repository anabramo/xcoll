import numpy as np
import xobjects as xo

from .engine import Geant4Engine

class Geant4Interaction(xo.HybridClass):
    _xofields = {
        'element_id':    xo.String,
        'g4link':        xo.String,
    }


    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def interact(self, particles):
        g4link = self.element.g4link
        g4link.clearData() # Clear the old data - bunch particles and hits

        # This temp delta is necessary because for primary particles, the coordinates are
        # modified in place. But for the longitudinal plane there are 3 coordinates that must
        # be updated, so pass a copy of the delta for the update in place and trigger the
        # correct update of the 3 coordinates later
        delta_temp = particles._delta.copy()

        # Using a list allows to package the required coordinates without copying
        coordinates = [particles.x, particles.y, particles.px, particles.py,
                       particles.zeta, delta_temp, particles.s,
                       particles.particle_id, particles.state,
                       particles.at_element, particles.at_turn]

        g4link.addParticles(coordinates)
        # The collimators must be defined already in the g4manager
        g4link.selectCollimator(self.element.id)

        g4link.collimate() # Performs the physical interaction simulation

        # Modifies the primary coordinates in place and returns a list of arrays for the
        # coordinates of the secondary particles.
        products = g4link.collimateReturn(coordinates)

        # Force the update using the private member _delta
        # as the update_delta method only updates the delta for active particles
        particles._delta[:len(delta_temp)] = delta_temp
        particles.update_delta(delta_temp)

        return products
