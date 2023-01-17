import numpy as np

import xobjects as xo
import xtrack as xt

from ..general import _pkg_root

class BlackAbsorber(xt.BeamElement):
    _xofields = {
        'inactive_front': xo.Float64,
        'active_length': xo.Float64,
        'inactive_back': xo.Float64,
        'jaw_L': xo.Float64,
        'jaw_R': xo.Float64,
        'jaw_U': xo.Float64,
        'jaw_D': xo.Float64,
        'dx': xo.Float64,
        'dy': xo.Float64,
        'dpx': xo.Float64,
        'dpy': xo.Float64,
        'cos_z': xo.Float64,
        'sin_z': xo.Float64,
    }

    isthick = True
    behaves_like_drift = True

    def __init__(self, angle=0, **kwargs):
        super().__init__(**kwargs)

    @property
    def angle(self):
        return np.arctan2(self.sin_z, self.cos_z) * (180.0 / np.pi)
    
    @angle.setter
    def angle(self, angle):
        anglerad = angle / 180 * np.pi
        self.cos_z = np.cos(anglerad)
        self.sin_z = np.sin(anglerad)

    @property
    def length(self):
        return (self.inactive_front + self.active_length + self.inactive_back)

