try:
    ip = get_ipython()
    if ip.__class__.__name__ == 'TerminalInteractiveShell':
        ip.magic('pylab')
    elif ip.__class__.__name__ == 'ZMQInteractiveShell':
        ip.magic('pylab notebook')
except NameError:
    pass

def warn():
    import traceback, sys
    sys.stderr.write(
        'pymule warning: some functionality may not be available\n%s\n' % (
            traceback.format_exc()
        )
    )

__all__ = []

try:
    import numpy as np
    __all__ += ['np']

    from .vegas import importvegas, exportvegas
    __all__ += ['importvegas', 'exportvegas']

    from .errortools import mergenumbers, plusnumbers, dividenumbers, timesnumbers,\
                            mergeplots, addplots, divideplots, scaleplot,          \
                            combineplots, combineNplots,                           \
                            integratehistogram, mergebins, printnumber, chisq
    __all__ += [
        'mergenumbers', 'plusnumbers', 'dividenumbers', 'timesnumbers',
        'mergeplots', 'addplots', 'divideplots', 'scaleplot',
        'combineplots', 'combineNplots',
        'integratehistogram', 'mergebins', 'printnumber',
        'chisq'
    ]

    from .loader import importreg, pattern, setup, sigma,                          \
                        mergeset, mergeseeds, mergefks,                            \
                        addsets, scaleset
    __all__ += [
        'importreg', 'pattern', 'setup', 'sigma',
        'mergeset', 'mergeseeds', 'mergefks',
        'addsets', 'scaleset'
    ]

    from .constants import pi, alpha, GF, conv, Mmu, Mel, Mtau
    __all__ += ['pi', 'alpha', 'GF', 'conv', 'Mmu', 'Mel', 'Mtau']

    import matplotlib.pyplot as plt
    __all__ += ['plt']

    from .xicut import mergefkswithplot
    __all__ += ['mergefkswithplot']

    from .plot import errorband, kplot, watermark, updateaxis
    __all__ += ['errorband', 'kplot', 'watermark', 'updateaxis']
    from .mule import mulify
    __all__ += ['mulify']

    from . import colours
    __all__ += ['colours']
except:
    warn()
