from .loader import multiintersect, addsets, mergeset, scaleset
from scipy import optimize
import scipy.stats
import matplotlib.pyplot as plt
import numpy as np
from .errortools import *
from .colours import alpha_composite


def myfit(data, n):
    """
    myfit(data, n) fits sum_{i=0}^n a_i log(xi_c)^i to the data
    that is given as a plot.

    Input must be a np.array([[xi1, y1, e1], [xi2, y2, e2], ...]).
    """
    xdata = np.log(data[:,0])
    ydata = data[:,1]
    edata = data[:,2]

    fitfunc = lambda p, x: sum(p[i] * x**i for i in range(len(p)))
    errfunc = lambda p, x, y, err: (y - fitfunc(p, x)) / err

    pinit = [1.0] * (n+1)
    out = optimize.leastsq(errfunc, pinit,
                           args=(xdata, ydata, edata), full_output=1)

    coeff = out[0]
    covar = out[1]

    return coeff, covar


def get_val(xs, coeff):
    """
    Given a list of xi values xs and a coeff array from myfit, get_val
    evaluates the fit at the values in xs.
    """
    return [
        sum(np.log(x)**np.arange(0,len(coeff)) * coeff)
        for x in xs
    ]


def get_errorbands(x, coeff, covar, ndata, cf=0.9):
    """
    Given a list of xi values x, the coefficient list coeff and the
    covariance matrix covar from myfit, get_errorbands calculates the
    CF=0.9 errorbands at the values in x.
    """
    if type(x) == np.ndarray:
        return np.array([
            get_errorbands(i, coeff, covar, ndata, cf) for i in x
        ])
    else:
        tval = scipy.stats.t.ppf((cf+1)/2, ndata - len(coeff))
        xvec = np.log(x)**np.arange(0,len(coeff))

        delta = tval*np.sqrt(np.matmul(np.matmul(xvec, covar), xvec))
        centre = sum(xvec * coeff)

        return np.array([x, centre, centre+delta, centre-delta])


def addkeyedsets(sets):
    """
    addkeyedsets(sets) adds a list of keyed sets, i.e. it adds cross
    section, histograms, and run time. The 'chi2a' is a list of
    constituent 'chi2a's.
    """
    paras = multiintersect([i.keys() for i in sets])
    return {
        para: addsets([i[para] for i in sets])
        for para in paras
    }


def mergefkswithplot(sets, scale=1., showfit=[True,True], xlim=[-7, 0]):
    """
    mergefkswithplot(...) performs the FKS merge like mergefks.
    However, it also produces a xi_c plot.

    In contrast mergefks, here phase-space partioned results need to
    be merged first. This is done by grouping those into an array
    first, sorted by number of particles in the final state, i.e. we
    start with the n-particle corrections. Example

    mergefkswithplot([
        [
            sigma('em2emFEE'), sigma('em2emFMM'), sigma('em2emFEM')
        ],
        [
            sigma('em2emREE15'), sigma('em2emREE35'),
            sigma('em2emRMM'),
            sigma('em2emREM')
        ]
    ])

    The FKS merge consists of taking random-seed-merged results
    (usually from sigma) and producing a final set, containing cross
    sections, distributions, and run-time information. The chi2a
    return is a list of the following
     * the chi^2 of the FKS merge
     * a list of chi^2 from previous operations, such as random seed
       merging or the integration.

    mergefks returns the figure of the plot and the result of the FKS
    merge.


    optional arguments
     * scale: a global factor by which the results are re-scaled
         (default: 1.)
     * showfit=[l1, l2]: whether to show the fit lines the overview
         plot (l1) and the zoomed in plot (l2) (default: show all
         fits, i.e. [True, True])
    """
    n = len(sets)
    psets = [addkeyedsets(i) for i in sets]
    ans = mergeset(list(addkeyedsets(psets).values()))

    fig, (ax1,ax2) = plt.subplots(
        2, sharex=True, gridspec_kw={'hspace': 0, 'height_ratios': [3,2]}
    )

    ax2.set_xscale('log')
    ax2.set_xlabel('$\\xi_c$')
    ax1.set_ylabel('$\\sigma^{(%d)}_i$' % (n-1))
    ax2.set_ylabel(
        r'$\tfrac{\sigma^{(%d)}}{\langle\sigma^{(%d)}\rangle}-1$' % (n-1, n-1)
    )
    ax2.ticklabel_format(style='sci',axis='y')
    ax2.yaxis.major.formatter.set_powerlimits([1,1])

    xval = np.exp(np.linspace(xlim[0],xlim[1]))

    totcoeff = np.zeros(n)
    totcovar = np.zeros((n,n))
    pvalues = []
    for pset, ind in zip(psets, range(1,1+len(psets))):
        values = np.array([
            np.insert(scale*pset[xi]['value'], 0, xi[0])
            for xi in sorted(pset.keys())
        ])
        pvalues.append(values)

        coeff, covar = myfit(values, n-1)
        totcoeff += coeff
        totcovar += covar

        if showfit[0]:
            ax1.plot(
                xval, get_val(xval, coeff),
                c='C%d' % ind
            )
        ax1.errorbar(
            values[:,0], values[:,1], values[:,2],
            linestyle='none', marker='.',
            c='C%d' % ind
        )

    norm = scale*ans['value'][0]

    tot = combineNplots(addplots,pvalues)
    tot0 = [1,1/norm,1/norm] * tot - [0,1,0]

    band = get_errorbands(xval, totcoeff, totcovar, len(pvalues[0]))
    if showfit[1]:
        ax2.plot(band[:,0], band[:,1]/norm-1)
        ax2.fill_between(
            band[:,0],
            band[:,2]/norm-1, band[:,3]/norm-1,
            color=alpha_composite('white', 'C0', 0.1)
        )
    ax2.errorbar(
        tot0[:,0], tot0[:,1], tot0[:,2],
        linestyle='none', marker='.',
        c='C0'
    )

    if showfit[0]:
        ax1.plot(band[:,0], band[:,1])
    ax1.errorbar(
        tot[:,0], tot[:,1], tot[:,2],
        linestyle='none', marker='.',
        c='C0'
    )

    # Matplotlib's offset placing routine has a bug. This sorta fixes it
    ax2.yaxis._update_offset_text_position=lambda a,b : 0
    ax2.yaxis.offsetText.set_transform(ax2.transAxes)
    ax2.yaxis.offsetText.set_verticalalignment('top')
    ax2.yaxis.offsetText.set_position((
        0,
        0.98
    ))

    ax1.legend(
        ['$\\sigma^{(%d)}_{n}$' % (n-1)] +
        ['$\\sigma^{(%d)}_{n+%d}$' % (n-1, i) for i in range(1, n)] +
        ['$\\sigma^{(%d)}$' % (n-1)],
        loc='upper right'
    )

    return fig, scaleset(ans,scale)
