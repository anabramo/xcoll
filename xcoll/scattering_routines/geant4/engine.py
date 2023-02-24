import numpy as np
import xobjects as xo

_geant4_warning_given = False

class Geant4Engine(xo.HybridClass):

    _xofields = {
        'random_generator_seed':    xo.Int64,
        'reference_pdg_id':         xo.Int64,
        'reference_kinetic_energy': xo.Float64,
        'relative_energy_cut':      xo.Float64,
        'bdsim_config_file':        xo.String
#         'random_freeze_state':    xo.Int64,  # to be implemented; number of randoms already sampled, such that this can be taken up again later
#         'collimators':            Geant4Collimator[:],  # Does not work, need a pointer of sorts
    }

    def __init__(self, batch_mode=True, **kwargs):
        # Allow seed to be set to None to get default:
        kwargs.setdefault('random_generator_seed', None)
        if kwargs['random_generator_seed'] is None:
            kwargs['random_generator_seed'] = np.random.randint(1, 10000000)
        super().__init__(**kwargs)
        try:
            import collimasim as cs
        except ImportError:
            global _geant4_warning_given
            if not _geant4_warning_given:
                print("Warning: Failed to import collimasim. " \
                      + "Geant4Collimators will be installed but are not trackable.")
                _geant4_warning_given = True
        else:
            unit_GeV = 1e9 # GeV to eV
            self.g4link = cs.XtrackInterface(bdsimConfigFile=self.bdsim_config_file,
                                             referencePdgId=self.reference_pdg_id,
                                             referenceEk=self.reference_kinetic_energy / unit_GeV, # BDSIM expects GeV
                                             relativeEnergyCut=self.relative_energy_cut,
                                             seed=self.random_generator_seed, batchMode=batch_mode)

    def add_collimator(self, name, material, length, ):
        self.g4link.addCollimator(name, material, cdata["length"], apertureLeft=halfgap, apertureRight=halfgap,
                              rotation=cdata["angle"], xOffset=copt["X"], yOffset=copt["Y"],
                              jawTiltLeft=cdata.get("tilt_left", 0.), jawTiltRight=cdata.get("tilt_right", 0.), 
                              side=cdata.get("side", 0))

