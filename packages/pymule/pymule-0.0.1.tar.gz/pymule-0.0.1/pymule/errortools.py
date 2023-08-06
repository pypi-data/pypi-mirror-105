import numpy as np


def chisq(values):
    """
    chisq(values) calculates the chi^2/d.o.f. of the values in this
    list. Accepts either a python list or a np.array. Notation is as
    usual [y, e], s.t. list = [ [y1,e1], [y2, e2], ... ]
    """
    if type(values) == list:
        values = np.array(values)
    weight = sum(1 / values[:,1]**2)
    value = sum(values[:,0] / values[:,1]**2 / weight)
    chi = 1./len(values) * sum(
        ((values[:,0]-value) / values[:,1])**2
    )
    return chi


def mergenumbers(values, quiet=False):
    """
    mergenumbers(values) statistically combines a list of values with
    uncertainties. Accepts either a python list or a np.array.
    Notation is as usual [y, e], s.t. list = [ [y1,e1], [y2, e2], ...].
    Unless requested otherwise with quiet=True, the chi^2/d.o.f. is
    printed.
    """
    if type(values) == list:
        values = np.array(values)

    weight = sum(1 / values[:,1]**2)
    value = sum(values[:,0] / values[:,1]**2 / weight)
    chi = 1./len(values) * sum(
        ((values[:,0]-value) / values[:,1])**2
    )
    ans = np.array([value, np.sqrt(1/weight)])

    if not quiet:
        print(chi)
        return ans
    else:
        return chi, ans


def plusnumbers(*args):
    """
    plusnumbers([y1, e1], [y2, e2], ...) adds the numbers y1 + y2 + ...
    """
    if len(args) == 1:
        lst = np.array(args[0])
    else:
        lst = np.array(args)
    return np.array([
        sum(lst[:,0]),
        np.sqrt(sum(lst[:,1]**2))
    ])


def dividenumbers(a, b):
    """
    dividenumbers(a, b) returns a/b with correct error propagation.
    Input in the usual format (as anything that supports getitem) as
    [y, e]
    """
    return np.array([
        a[0]/b[0],
        np.sqrt((b[1]**2*a[0]**2)/b[0]**4 + a[1]**2/b[0]**2)
    ])


def timesnumbers(a, b):
    """
    times(a, b) returns a*b with correct error propagation.
    Input in the usual format (as anything that supports getitem) as
    [y, e]
    """
    return np.array([
        a[0]*b[0],
        np.sqrt(b[0]**2*a[1]**2 + a[0]**2*b[1]**2)
    ])


def integratehistogram(hist):
    """
    Given a histogram hist, integratehistogram(hist) returns the
    integral over this histogram *without* error estimation.

    Input must be a np.array([[x1, y1, e1], [x2, y2, e2], ...]) with
    equally spaced bins
    """
    ans = 0
    if hist[0,0] == -np.inf:
        ans += hist[0,1]
        hist = hist[1:]
    if hist[-1,0] == +np.inf:
        ans += hist[-1,1]
        hist = hist[:-1]

    ans += np.mean(np.diff(hist[:,0])) * sum(hist[:,1])
    return ans


def mergeplots(ps, returnchi=False):
    """
    mergeplots(ps) statistically combines a list of plots.
    mergeplots(ps, returnchi=True) also returns the bin-wise chisq

    Input must be a np.array([[x1, y1, e1], [x2, y2, e2], ...]).
    """
    if type(ps) == list:
        ps = np.array(ps)

    if len(ps.shape) != 3:
        return np.array([])
    with np.errstate(divide='ignore', invalid='ignore'):
        w = np.sum(1/ps[:,:,2]**2,0)
        out = np.zeros(ps[0].shape)

        out[:,1] = np.sum(ps[:,:,1]/ps[:,:,2]**2 / w, 0)
        out[:,2] = np.sqrt(1/w)

        # if one bin is empty, the zero causes trouble
        out[~np.isfinite(out)] = 0
        out[:,0] = ps[0,:,0]

        chi = 1./(len(ps)-1)*np.sum((ps[:,:,1]-out[:,1])**2/ps[:,:,2]**2,0)
        chi[~np.isfinite(chi)] = 0
        chi = np.column_stack((out[:,0], chi))

    if returnchi:
        return out, chi
    else:
        return out


def combineplots(a, b, yfunc, efunc, tol=1e-8):
    """
    combineplots(a, b, yfunc, efunc, tol=1e-8) combines the plots a
    and b, provided with a function for the values (yfunc) and the
    errors (efunc). Users will not likely call this directly.

    tol is the number of digits the x values have to agree at to
    considered equal.

    Input must be a np.array([[x1, y1, e1], [x2, y2, e2], ...]).
    """
    la = np.round(a[:,0] / tol)
    lb = np.round(b[:,0] / tol)
    newx = np.intersect1d(la, lb)

    maskA = np.in1d(la, newx)
    maskB = np.in1d(lb, newx)

    with np.errstate(divide='ignore', invalid='ignore'):
        x = a[maskA, 0]
        y = yfunc(a[maskA, 1], b[maskB, 1])
        e = efunc(a[maskA, 1], a[maskA, 2], b[maskB, 1], b[maskB, 2])

        y[~np.isfinite(y)] = 0
        e[~np.isfinite(e)] = 0

        out = np.column_stack((x, y, e))
        # if one bin is empty, the zero causes trouble

    return out


def addplots(a, b, sa=1., sb=1.):
    """
    addplots(a, b, sa=1., sb=1.) add the plots a and b, weighted by sa
    and sb, i.e. it returns sa * a + sb * b. For example, use
    addplots(a, b, sb=-1) to calculate a - b.

    Input must be a np.array([[x1, y1, e1], [x2, y2, e2], ...]).
    """
    return combineplots(
        a, b,
        lambda y1, y2: sa*y1 + sb*y2,
        lambda y1, e1, y2, e2: np.sqrt((sa*e1)**2 + (sb*e2)**2)
    )


def divideplots(a, b, offset=0.):
    """
    divideplots(a, b, offset=0.) divides the plots a and b, off-setted
    by offset, i.e. it returns a/b+offset. offset=1. is useful for K
    factors.

    Input must be a np.array([[x1, y1, e1], [x2, y2, e2], ...]).
    """
    return combineplots(
        a, b,
        lambda y1, y2: offset + y1 / y2,
        lambda y1, e1, y2, e2: np.sqrt(e2**2 * y1**2 / y2**4 + e1**2 / y2**2)
    )


def combineNplots(func, plots):
    """
    Given a combination function (such as addplots) and a *list* of
    plots, this returns func(plots[0], func(plots[1], func(plots[2],
    ...))). This is useful to, for example, add a number of plots as
    combineNplots(addplots, plots)
    """
    accum = plots[0]
    for plot in plots[1:]:
        accum = func(accum, plot)
    return accum


def scaleplot(a, sx, sy=None):
    """
    scaleplot(a, s) rescales a plot by s such that the
    integrated plot remains unchanged, i.e. it rescales x and y as
    x -> x / s and y -> y * s
    This is useful to, for example, change units.

    scaleplot(a, sx, sy) rescales the x and y axis independently of
    each other.

    Input must be a np.array([[x1, y1, e1], [x2, y2, e2], ...]).
    """
    if sy is None:
        return np.array((1./sx, sx, sx)) * a
    else:
        return np.array((1./sx, sy, sy)) * a


def mergebins(p, n):
    """
    mergebins(p, n) merges n adjacent bins in the histogram p into one
    larger bin, reducing the uncertainty. Some bins (len(p) % n to be
    exact) may be lost this way.

    Input must be a np.array([[x1, y1, e1], [x2, y2, e2], ...]).
    """
    if p[0,0] == -np.inf:
        return np.concatenate([
            [p[0,:]],
            mergebins(p[1:,:], n)
        ])
    if p[-1,0] == +np.inf:
        return np.concatenate([
            mergebins(p[:-1,:], n),
            [p[-1,:]]
        ])

    # Make sure the length fits
    if len(p) % n:
        short = p[:-(len(p) % n)]
    else:
        short = p[:]
    part = np.split(short, len(short)/n)
    return np.array([
        (
            sum(i[:,0])/n,
            sum(i[:,1])/n,
            np.sqrt(sum(i[:,2]**2))/n
        ) for i in part
    ])


def printnumber(x, prec=0):
    """
    printnumber(x) prints a number with uncertainties to one
    significant digits (as usual, [y, e])
    """
    if x[1] == 0:
        return x[0]

    digits = int(-np.floor(np.log10(x[1]))) + prec

    fmt = '%.' + str(digits) + 'f(%.' + str(prec) + 'f)'
    return fmt % (
        round(x[0], digits),
        10**digits*round(x[1], digits)
    )
