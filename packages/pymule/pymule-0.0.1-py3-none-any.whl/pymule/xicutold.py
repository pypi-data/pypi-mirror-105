from loader import multiintersect, addsets, mergeset
from scipy import optimize
import scipy.stats
import matplotlib.pyplot as plt
import numpy as np
from errortools import *


def myfit(data, n):
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
    return [
        sum(np.log(x)**np.arange(0,len(coeff)) * coeff)
        for x in xs
    ]


def get_errorbands(x, coeff, covar, cf=0.9):
    if type(x) == np.ndarray:
        return np.array([
            get_errorbands(i, coeff, covar, cf) for i in x
        ])
    else:
        tval = scipy.stats.t.ppf((cf+1)/2, len(coeff))
        xvec = np.log(x)**np.arange(0,len(coeff))

        delta = tval*np.sqrt(np.matmul(np.matmul(xvec, covar), xvec))
        centre = sum(xvec * coeff)

        return np.array([x, centre, centre+delta, centre-delta])


def get_errormap(coeff, covar):
    n = len(coeff)
    tval = scipy.stats.t.ppf((cf+1)/2, len(coeff))

    dxvec = [0] + [(i+1)*np.log(x)**i for i in range(n-1)]
    xvec = np.log(x)**np.arange(n)
    sqrt = np.matmul(np.matmul(xvec, covar), xvec)
    dsqrt = (
        np.matmul(np.matmul(dxvec, covar), xvec)
        + np.matmul(np.matmul(xvec, covar), dxvec)
    )
    ddelta = dsqrt/np.sqrt(sqrt)/2/x


def addkeyedsets(sets):
    paras = multiintersect([i.keys() for i in sets])
    return {
        para: addsets([i[para] for i in sets])
        for para in paras
    }


def mergefkswithplot(sets, split=False, scale=1., showfit=[True,True]):
    n = len(sets)
    psets = [addkeyedsets(i) for i in sets]
    ans = mergeset(addkeyedsets(psets).values())

    if split:
        fig1, ax1 = plt.subplots()
        fig2, ax2 = plt.subplots()
        fig = [fig1,fig2]
    else:
        fig, (ax1, ax2) = plt.subplots(1, 2)

    ax1.set_xscale('log')
    ax2.set_xscale('log')
    ax1.set_xlabel('$\\xi_c$')
    ax2.set_xlabel('$\\xi_c$')
    ax1.set_ylabel('$\\sigma^{(%d)}_i$' % (n-1))
    ax2.set_ylabel(
        r'$\tfrac{\sigma^{(%d)}}{\langle\sigma^{(%d)}\rangle}-1$' % (n-1, n-1)
    )
    ax2.ticklabel_format(style='sci',axis='y')
    ax2.yaxis.major.formatter.set_powerlimits([1,1])

    xval = np.exp(np.linspace(-7,0))

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

    band = get_errorbands(xval, totcoeff, totcovar)
    if showfit[1]:
        ax2.plot(band[:,0], band[:,1]/norm-1)
        ax2.fill_between(
            band[:,0],
            band[:,2]/norm-1, band[:,3]/norm-1,
            alpha=0.1, color='C0'
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

    ax1.legend(
        ['$\\sigma^{(%d)}_{n}$' % (n-1)] +
        ['$\\sigma^{(%d)}_{n+%d}$' % (i, n-1) for i in range(1, n)] +
        ['$\\sigma^{(%d)}$' % (n-1)],
        loc='upper right'
    )
    ax2.legend(
        ['$\\sigma^{(%d)}$' % (n-1)],
        loc='upper right'
    )

    return fig, ans
