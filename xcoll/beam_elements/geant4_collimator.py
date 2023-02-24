import numpy as np
import random
import string

import xobjects as xo
from xtrack import BeamInteraction

from ..scattering_routines.geant4 import Geant4Engine, Geant4Interaction
from .base_collimator import BaseCollimator



def _new_id64(len=16):
    chars = string.ascii_letters + string.digits + '+/'
    return ''.join(random.choice(chars) for i in range(len))


class Geant4Collimator(BaseCollimator, BeamInteraction):
    _xofields = BaseCollimator._xofields | {
        'id':         xo.String,
        'g4engine':   Geant4Engine
    }

    iscollective = True

    def __init__(self, **kwargs):
        kwargs.setdefault('id', _new_id64())
        BaseCollimator.__init__(self, **kwargs)
        # We skip the BeamInteraction initialisation (to avoid issues with setting the length)
        # and manually set the interaction process
        self.interaction_process = Geant4Interaction(element=self)


    def track(self, part):
        BeamInteraction.track(self, part)


    # NEED TO HAVE UPDATE RULES!!! WHEN BeamElement.jaw_F_L etc are updated, this needs to be communicated to Geant4...
    # jaws are currently not set
