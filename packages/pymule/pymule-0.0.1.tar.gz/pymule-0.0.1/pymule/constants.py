import numpy as np
import os


def read_globaldef(globaldef=''):
    if len(globaldef) == 0:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        globaldef = os.path.abspath(os.path.join(
            dir_path, os.pardir, os.pardir, 'global_def.f95'
        ))

    if not os.path.exists(globaldef):
        raise IOError('No such file or directory %s' % globaldef)

    with open(globaldef) as fp:
        return [
            (n,eval(v))
            for n,v in re.findall(
                'parameter *:: *([A-Z][A-Z\d]*) = ([\dE\.+/-]+)',
                fp.read(),
                re.IGNORECASE
            )
        ]


pi = np.pi


Mmu = 105.658375 # MeV
Mel = 0.510998950 # MeV
Mtau = 1776.86     # MeV
Mproton = 938.272088

alpha = 1./137.035999084
GF = 1.1663787E-11   # MeV^-2

conv = 3.893793655569159807686738742e8  # MeV^2 mu barn
