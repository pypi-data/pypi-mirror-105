import re
from .vegas import importvegas, getplots
from .errortools import *
import os
import inspect
import tarfile
import io

loadargs = {}


def importreg(r, folder='.', filenames=None,
              merge={}, types=[int,float,float],
              sanitycheck=lambda x: True):
    """
    importreg(r, ...) imports all vegas files matching the regular
    expression r and returns a dict containing the results, keyed with
    the groups defined in r.

    optional arguments:

    folder: which folder (or tar file) to search for vegas files
    (default: '.')

    filenames: provide a list of file names to consider. Otherwise all
    files found will be considered (either os.listdir or list(tar))
    (default: None, implying everything)

    merge: given a dict of histograms {'name': n} merges n bins in the
    histogram name (default: {}, i.e. no merging)

    types: functions that convert the groups matched by r into python
    objects. Common examples would be int or float (default: [int,
    float, float] as per McMule filename convention)

    sanitycheck: a function (lambda or named) that, given a vegas
    dict, whether to include the file in the output (return True) or
    to skip (return False) (default: lambda x:True, i.e. include
    everything)
    """

    tar = None
    if not os.path.isdir(folder):
        if os.path.splitext(folder)[1] == '.bz2':
            import bz2
            with bz2.BZ2File(folder, 'r') as b:
                fp = io.BytesIO(b.read())
            tar = tarfile.open(fileobj=fp)
        elif os.path.splitext(folder)[1] == '.gz':
            import gzip
            with gzip.open(folder, 'r') as b:
                fp = io.BytesIO(b.read())
            tar = tarfile.open(fileobj=fp)
        else:
            tar = tarfile.open(folder)

    if filenames is None:
        if tar:
            filenames = [
                i.name
                for i in tar if 'vegas' in i.name
            ]
        else:
            filenames = os.listdir(folder)

    dic = {}
    for filename in filenames:
        m = re.match(r, filename)
        if m:
            if tar:
                v = importvegas(fp=tar.extractfile(filename))
            else:
                v = importvegas(os.path.join(folder, filename))

            if not sanitycheck(v):
                continue

            for p, n in merge.items():
                if n > 0:
                    v[p] = mergebins(v[p], n)

            if len(types) == len(m.groups()):
                k = tuple(f(v) for v,f in zip(m.groups(), types))
            else:
                k = m.groups()
            dic[k] = v

    return dic


def pattern(piece='.*', flavour='.*', obs='', folderp='.*'):
    """
    pattern(...) constructs a regular expression to be used in
    importreg matching the usual McMule file name convention

    optional arguments:
    piece: the which_piece to load (default: everything, i.e. ".*")

    flavour: the flavour to load (default: everything, i.e. ".*")

    obs: the observable to load (the bit after the O) (default: '')

    folderp: a regular expression to match directory structures of a
    tar file (default: everything, i.e. ".*")
    """
    if len(obs) > 0:
        return (
            folderp + piece + '_' + flavour + '_S(\d+)X([\d\.]+)D([\d\.]+).*O'
            + obs + '.vegas'
        )
    else:
        return (
            folderp + piece + '_' + flavour + '_S(\d+)X([\d\.]+)D([\d\.]+).*'
        )


def mergeset(s):
    """
    mergeset statistically merges a set of runs, combining cross
    sections, histograms, and run-time information. The 'chi2a' of the
    output is a list of
     * the chi^2 of the cross section combination
     * a list of the individual chi^2
    """
    if len(s) == 0:
        return {}
    if len(s) == 1:
        return s[0]

    c, v = mergenumbers([i['value'] for i in s],True)
    dic = {
        'time': sum([i['time'] for i in s]),
        'value': v,
        'chi2a': [c, [i['chi2a'] for i in s]]
    }

    for plot in getplots(s):
        p = mergeplots([i[plot] for i in s])
        if p.shape == (0,):
            continue
        dic[plot] = p

    return dic


def mergeseeds(s, key=lambda x: (x[1], x[2])):
    """
    mergeseeds(s, key) statistically merges the random seeds of a set
    of runs. The key is used to group runs in the dict s. Usually,
    this refers to the FKS parameters (in the default notation
    lambda x: (x[1], x[2]) referring to xi_c (x[1]) and \delta (x[2]).

    mergeseeds is using mergesets. This means that it combines cross
    sections, histograms, and run-time information. The 'chi2a' of the
    output is a list of
     * the chi^2 of the cross section combination
     * a list of the individual chi^2
    """
    groups = set(map(key, s.keys()))

    dic = {}
    for group in groups:
        ss = [
            s[k]
            for k in s.keys()
            if key(k) == group
        ]
        dic[group] = mergeset(ss)

    return dic


def addsets(s):
    """
    addsets(s) adds a list of sets (cross section, histograms, and
    run time). The 'chi2a' is a list of constituent 'chi2a's.
    """
    if len(s) == 0:
        return {}

    dic = {
        'time': sum([i['time'] for i in s]),
        'value': plusnumbers([i['value'] for i in s]),
        'chi2a': [i['chi2a'] for i in s]
    }

    for plot in getplots(s):
        dic[plot] = combineNplots(addplots, [i[plot] for i in s])

    return dic


def scaleset(s, v):
    """
    scaleset(s, v) rescales the cross section and distributions of the
    set s. Note that this naturally changes the cross section.
    """
    dic = {
        'time': s['time'],
        'chi2a': s['chi2a'],
        'value': v * s['value']
    }
    for plot in getplots(s):
        dic[plot] = scaleplot(s[plot], 1., v)
    return dic


def scalesets(s, v):
    """
    scalesets(s, v) rescales the cross section and distributions of
    the sets s. Note that this naturally changes the cross section.
    """

    return {
        i: scaleset(s[i], v)
        for i in s.keys()
    }


def multiintersect(lists):
    """
    Given a list of lists, multiintersect find the elements common to
    all sub-lists. This is used to find a list of FKS parameters of a
    given run.
    """
    if len(lists) == 0:
        return []
    inter = set(lists[0])
    for i in lists[1:]:
        inter = inter.intersection(set(i))
    return list(inter)


def mergefks(*sets, **kwargs):
    """
    mergefks(...) performs the FKS merge, i.e. it takes
    random-seed-merged results (usually from sigma) and produces a
    final set, containing cross sections, distributions, and run-time
    information. The chi2a return is a list of the following
     * the chi^2 of the FKS merge
     * a list of chi^2 from previous operations, such as random seed
       merging or the integration.

    Optional argument anyxi (or anything starting with anyxi):
    Sometimes it is necessary to merge xi-dependent runs (such as a
    counter term) and xi-independent runs (such as the one-loop term).
    anyxi is used for this. Example for the radiative muon decay

    mergefks(
        sigma('m2enngR'),       # real corrections
        sigma('m2enngCT'),      # counter term
        anyxi=sigma('m2enngV')  # virtual corrections
    )
    """
    paras = multiintersect([i.keys() for i in sets])

    anyxi = []
    for i in kwargs.keys():
        if 'anyxi' not in i:
            continue
        if len(kwargs[i].keys()) > 1:
            raise KeyError('%s has multiple xis! Only one is allowed' % i)
        anyxi.append(list(kwargs[i].values())[0])

    ans = []
    for para in paras:
        ans.append(addsets([i[para] for i in sets] + anyxi))
    return mergeset(ans)


def callsanitised(func, **kwargs):
    """
    Calls a function func with the arguments from kwargs and the
    defaults specified in the global loadargs. Arguments that are not
    matching are discarded.
    """
    global loadargs
    legal = inspect.getargspec(func).args
    args = {}
    args.update(loadargs)
    args.update(kwargs)
    args = {
        i: args[i]
        for i in args.keys()
        if i in legal
    }
    return func(**args)


def setup(**kwargs):
    """
    setup(**kwargs) sets the default arguments for the sigma(...)
    function. Possible options are

    folder: which folder (or tar file) to search for vegas files
    (default: '.')

    flavour: the flavour to load (default: everything, i.e. ".*")

    obs: the observable to load (the bit after the O) (default: '')

    folderp: a regular expression to match directory structures of a
    tar file (default: everything, i.e. ".*")

    filenames: provide a list of file names to consider. Otherwise all
    files found will be considered (either os.listdir or list(tar))
    (default: None, implying everything)

    merge: given a dict of histograms {'name': n} merges n bins in the
    histogram name (default: {}, i.e. no merging)

    types: functions that convert the groups matched by r into python
    objects. Common examples would be int or float (default: [int,
    float, float] as per McMule filename convention)

    sanitycheck: a function (lambda or named) that, given a vegas
    dict, whether to include the file in the output (return True) or
    to skip (return False) (default: lambda x:True, i.e. include
    everything)
    """
    global loadargs
    loadargs.update(kwargs)


def sigma(piece, **kwargs):
    """
    sigma(piece, **kwargs) loads the which_piece piece and
    statistically combines the random seeds. It returns a dict
    with the tuples of FKS parameters as keys.

    Arguments provided here overwrite the project-default (as set in
    setup) and code-default

    folder: which folder (or tar file) to search for vegas files
    (default: '.')

    flavour: the flavour to load (default: everything, i.e. ".*")

    obs: the observable to load (the bit after the O) (default: '')

    folderp: a regular expression to match directory structures of a
    tar file (default: everything, i.e. ".*")

    filenames: provide a list of file names to consider. Otherwise all
    files found will be considered (either os.listdir or list(tar))
    (default: None, implying everything)

    merge: given a dict of histograms {'name': n} merges n bins in the
    histogram name (default: {}, i.e. no merging)

    types: functions that convert the groups matched by r into python
    objects. Common examples would be int or float (default: [int,
    float, float] as per McMule filename convention)

    sanitycheck: a function (lambda or named) that, given a vegas
    dict, whether to include the file in the output (return True) or
    to skip (return False) (default: lambda x:True, i.e. include
    everything)
    """
    global loadargs
    pat = callsanitised(pattern, piece=piece, **kwargs)
    s = callsanitised(importreg, r=pat, **kwargs)
    return callsanitised(mergeseeds, s=s, **kwargs)
