import numpy as np

import xobjects as xo

from ...beam_elements import K2Collimator, K2Crystal

class K2Engine(xo.HybridClass):

    _xofields = {
        '_capacity':              xo.Int64,
        'random_generator_seed':  xo.Int64,
        # TODO: MetaBeamElement is not subscriptable
#         'collimators':            K2Collimator[:],    # TODO: make this one field for both collimators
#         'crystals':               K2Crystal[:],       #       and crystals
#         'random_state':           xo.Int64,           # TODO: to be implemented; number of randoms already sampled,
#                                                       #       such that this can be taken up again later
    }

    # The engine is a singleton
    def __new__(cls, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
            cls.instance._initialised = False
        return cls.instance


    def __init__(self, **kwargs):
        if(self._initialised):
            return
        self._initialised = True
        self._warning_given = False
        kwargs.setdefault('_capacity', 50000)
        kwargs.setdefault('random_generator_seed', None)  # Allow seed to be set to None to get default:
        if kwargs['random_generator_seed'] is None:
            kwargs['random_generator_seed'] = np.random.randint(1, 10000000)
#         kwargs.setdefault('collimators', [])
#         kwargs.setdefault('crystals', [])
#         kwargs.setdefault('random_freeze_state', -1)
        super().__init__(**kwargs)
        K2Engine.reset()


    @classmethod
    def reset(cls, seed=None):
        if seed is not None:
            cls.instance.random_generator_seed = seed
        try:
            from .pyk2f import pyk2_init
        except ImportError:
            if not cls.instance._warning_given:
                print("Warning: Failed to import pyK2 (did you compile?). " \
                      + "K2collimators will be installed but are not trackable.")
                cls.instance._warning_given = True
        else:
            pyk2_init(n_alloc=cls.instance._capacity, random_generator_seed=cls.instance.random_generator_seed)


    @classmethod
    def add_collimator(cls, collimator):
        if not hasattr(cls, 'instance'):
            cls()   # Instantiate the K2Engine if it doesn't exist yet
        if isinstance(collimator, K2Collimator):
#             if collimator not in self.collimators:
#                 self.collimators += collimator
            pass
        elif isinstance(collimator, K2Crystal):
#             if collimator not in self.crystals:
#                 self.crystals += crystal
            pass
        else:
            raise ValueError("The element to be added to the K2Engine is not a K2Collimator nor a K2Crystal!")


