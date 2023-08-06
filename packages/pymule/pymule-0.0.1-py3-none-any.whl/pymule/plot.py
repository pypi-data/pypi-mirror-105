import matplotlib.pyplot as plt
import matplotlib.collections
import matplotlib.patches
import matplotlib.lines
import numpy as np
from matplotlib import rc
from .colours import *
from .errortools import *
from . import mpl_axes_aligner
from .mule import mulify
import re


rc('text', usetex=True)
rc('text.latex', preamble='\n'.join([
    '\\usepackage{amsmath}',
    '\\usepackage{upgreek}',
    '\\newcommand{\\Einv}{E\\hspace*{-6pt}/}',
    '\\newcommand{\\D}{\\mathrm{d}}',
    '\\providecommand{\mathdefault}[1][]{}'
]))

#Taken from http://greg-ashton.physics.monash.edu/setting-nice-axes-labels-in-matplotlib.html
def update_label(old_label, exponent_text):
    if exponent_text == '': return old_label

    exp = '10^{%d} \\times' % -int(re.findall('10\^{([-\\d]*)}', exponent_text)[0])
    if old_label[0] == '$':
        return '$' + exp + old_label[1:]
    else:
        return '$' + exp + '$' + old_label
    return old_label# + ' ' + exponent_text

def format_label_string_with_exponent(ax, axis='both'):
    """ Format the label string with the exponent from the ScalarFormatter """
    ax.ticklabel_format(axis=axis, style='sci')

    axes_instances = []
    if axis in ['x', 'both']:
        axes_instances.append(ax.xaxis)
    if axis in ['y', 'both']:
        axes_instances.append(ax.yaxis)

    ax.stale = True
    plt.draw()
    for ax in axes_instances:
        ax.major.formatter._useMathText = True
        plt.draw() # Update the text
        exponent_text = ax.get_offset_text().get_text()
        label = ax.get_label().get_text()
        ax.offsetText.set_visible(False)
        ax.set_label_text(update_label(label, exponent_text))
        ax.stale = True


def updateaxis(ax, fig=None, n=3):
    if fig == None: fig = gcf()
    fig.canvas.draw()
    ax.yaxis.get_major_formatter().set_powerlimits((-n,n))
    format_label_string_with_exponent(ax, axis='y')


def setup_pgf():
    """
    setupf_pgf() ensures that Matplotlib exports PGF compatible
    plots.
    """
    plt.rcParams.update({
        'pgf.texsystem': 'pdflatex',
        'pgf.preamble': [
            '\\usepackage{amsmath}',
            '\\usepackage{upgreek}',
            '\\newcommand{\\Einv}{E\\hspace*{-6pt}/}',
            '\\newcommand{\\D}{\\mathrm{d}}'
            '\\newcommand{\\rm}{\\mathrm}'
        ],
        'font.family': 'serif',
        'text.usetex': True,
        'pgf.rcfonts': False
    })


def watermark(fig, txt='PRELIMINARY', fontsize=60, rotation=20):
    """
    watermark(fig, ...) writes 'PRELIMINARY' as a watermark over the
    figure fig.
    """
    axs = fig.axes
    corners = matplotlib.transforms.Bbox.union(
        [i.get_position() for i in axs]
    ).corners()
    center = np.average(corners, axis=0)
    fig.text(
        center[0], center[1],
        txt,
        fontsize=fontsize, rotation=rotation,
        ha='center', va='center', alpha=0.1
    )


def errorband(p, ax=None, col='default', underflow=False, overflow=False, linestyle='solid'):
    """
    errorband(p, ...) plots an errorband of a compatible histogram p.

    Input must be a np.array([[x1, y1, e1], [x2, y2, e2], ...]).

    optional arguments:
    ax: the axes object to plot. If not specified gca() is used,
    potentially creating a new axes

    col: a matplotlib colour specification. Per default matplotlib
    decides using the order specified in pymule.colours

    underflow, overflow: whether and how big to plot under- and
    overflow bins. Either logical or numbers indicating the how much
    bigger the under- and overflow bins shall be (default: False)
    """
    if ax is None:
        ax = plt.gca()

    p = p.copy()

    delta = p[2,0] - p[1,0]

    if p[0,0] == -np.inf:
        if underflow is False:
            p = p[1:]
        else:
            s = 2 if type(underflow) == bool else underflow
            p[0,0] = p[1,0] - (s+0.5) * delta
    if p[-1,0] == +np.inf:
        if overflow is False:
            p = p[:-1]
        else:
            s = 2 if type(overflow) == bool else overflow
            p[-1,0] = p[-2,0] + (s+0.5) * delta

    if col == 'default':
        artist = ax.step(p[:,0], p[:,1], where='mid', linestyle=linestyle)
        col = artist[0].get_color()
    else:
        artist = ax.step(p[:,0], p[:,1], col, where='mid', linestyle=linestyle)

    if linestyle == 'solid':
        ax.fill_between(
            p[:,0],
            p[:,1]+p[:,2]/2, p[:,1]-p[:,2]/2,
            step='mid',
            facecolor=col, edgecolor=col
        )
    return artist


def twopanel(labelx='',
             upleft=[], labupleft='', colupleft=defcol,
             downleft=[], labdownleft='', coldownleft=defcol,
             upright=[], labupright='', colupright=defcol,
             downright=[], labdownright='', coldownright=defcol,
             upalign=[], downalign=[]):
    """
    towpanel(...) creates two panel plot, accommodating at most four
    axes (upper left, upper right, lower left, and lower right). The x
    axis is naturally shared.

    Arguments:
    labelx: label for the x axis (default: "")

    upleft: data plotted in the upper-left axes, either np.array
    (single plot) or list of plots (default: nothing shown)

    labupleft: label for the upper-left y axis (default: "")

    colupleft: colour for upper-left data. Must at least as long as
    upleft (default: default colour scheme pymule.colours.defcol)

    downleft, labdownleft, coldownleft: similar for lower-left axes

    upright, labupright, colupright: similar for upper-right axes

    downright, labdownright, coldownright: similar for lower-right axes

    upalign, downalign: Values that should be aligned on the left and
    right y axis in the upper or lower panel.

    If some dataset is missing, nothing is shown for that axes and the
    axes is not created.

    Returns the figure created as well as a list of axes created.
    """

    if type(upleft) == np.ndarray:
        upleft = [upleft]
    if type(upright) == np.ndarray:
        upright = [upright]
    if type(downleft) == np.ndarray:
        downleft = [downleft]
    if type(downright) == np.ndarray:
        downright = [downright]

    fig, axs = plt.subplots(
        2, sharex=True, gridspec_kw={'hspace': 0}
    )
    axs = list(axs)
    if type(labelx) == str:
        axs[1].set_xlabel(labelx)
    else:
        axs[1].set_xlabel(**labelx)

    if type(labupleft) == str:
        axs[0].set_ylabel(labupleft)
    else:
        axs[0].set_ylabel(**labupleft)
    for i, c in zip(upleft, colupleft):
        if type(i) == dict:
            errorband(ax=axs[0], col=c, **i)
        else:
            errorband(i, ax=axs[0], col=c)

    if len(upright) > 0:
        ax2 = axs[0].twinx()
        axs.append(ax2)
        if labupright is not None:
            if type(labupright) == str:
                ax2.set_ylabel(labupright)
            else:
                ax2.set_ylabel(**labupright)
        for i, c in zip(upright, colupright):
            if type(i) == dict:
                errorband(ax=ax2, col=c, **i)
            else:
                errorband(i, ax=ax2, col=c)
        if len(upalign) == 2:
            mpl_axes_aligner.yaxes(
                axs[0], ax2,
                upalign[0], upalign[1]
            )

    if type(labdownleft) == str:
        axs[1].set_ylabel(labdownleft)
    else:
        axs[1].set_ylabel(**labdownleft)
    for i, c in zip(downleft, coldownleft):
        if type(i) == dict:
            errorband(ax=axs[1], col=c, **i)
        else:
            errorband(i, ax=axs[1], col=c)

    if len(downright) > 0:
        ax3 = axs[1].twinx()
        axs.append(ax3)
        if labdownright is not None:
            if type(labdownright) == str:
                ax3.set_ylabel(labdownright)
            else:
                ax3.set_ylabel(**labdownright)
        for i, c in zip(downright, coldownright):
            if type(i) == dict:
                errorband(ax=ax3, col=c, **i)
            else:
                errorband(i, ax=ax3, col=c)
        if len(downalign) == 2:
            mpl_axes_aligner.yaxes(
                axs[1], ax3,
                downalign[0], downalign[1]
            )

    return fig, axs


def threepanel(labelx='',
             upleft=[], labupleft='', colupleft=defcol,
             middleleft=[], labmiddleleft='', colmiddleleft=defcol,
             downleft=[], labdownleft='', coldownleft=defcol):
    if type(upleft) == np.ndarray:
        upleft = [upleft]
    if type(middleleft) == np.ndarray:
        middleleft = [middleleft]
    if type(downleft) == np.ndarray:
        downleft = [downleft]
    fig, axs = plt.subplots(
        3, sharex=True, gridspec_kw={'hspace': 0}
    )

    axs = list(axs)

    if type(labelx) == str:
        axs[2].set_xlabel(labelx)
    else:
        axs[2].set_xlabel(**labelx)

    if type(labupleft) == str:
        axs[0].set_ylabel(labupleft)
    else:
        axs[0].set_ylabel(**labupleft)
    for i, c in zip(upleft, colupleft):
        if type(i) == dict:
            errorband(ax=axs[0], col=c, **i)
        else:
            errorband(i, ax=axs[0], col=c)

    if type(labmiddleleft) == str:
        axs[1].set_ylabel(labmiddleleft)
    else:
        axs[1].set_ylabel(**labmiddleleft)
    for i, c in zip(middleleft, colmiddleleft):
        if type(i) == dict:
            errorband(ax=axs[0], col=c, **i)
        else:
            errorband(i, ax=axs[1], col=c)

    if type(labdownleft) == str:
        axs[2].set_ylabel(labdownleft)
    else:
        axs[2].set_ylabel(**labdownleft)
    for i, c in zip(downleft, coldownleft):
        if type(i) == dict:
            errorband(ax=axs[2], col=c, **i)
        else:
            errorband(i, ax=axs[2], col=c)

    return fig, axs


def kplot(sigma, labelx='$x_e$', labelsigma=None,
          labelknlo='$\\delta K^{(1)}$', labelknnlo='$\\delta K^{(2)}$',
          legend={'lo': r'$\rm LO$', 'nlo': r'$\rm NLO$', 'nnlo': r'$\rm NNLO$'},
          legendopts={'what': 'l', 'loc': 'upper right'},
          linestyle2=':',
          show=[0,-1], showk=[1,2], nomule=False):
    """
    kplot(sigma, ...) produces a K factor plot in line with McMule's
    design, i.e.  a two-panel plot showing in the upper panel the
    cross sections and in the lower panel the K factor defined as

        K^{(i)} = d\sigma^{(i)} / d\sigma^{(i-1)}

    The data to plot sigma is given as a dict with keys "lo", "nlo",
    and possibly "nnlo". kplot *only* takes the corrections at a loop
    order, not the full distribution!

    All labels support LaTeX inline maths

    optional arguments:
    labelx: the label for the x axis

    labelsigma: the label for the upper y axis

    labelknlo (labelknnlo): the labels for the K factors (default (per
    design guidelines $K^{(1)}$ and $K^{(2)}$)

    show, showk: a list which cross sections and K factors to show (if
    available), 0 indicates the LO cross section, 1 the NLO etc. -1
    indicates the last given cross section

    legend: a dict with the legend for "lo", "nlo", "nnlo". The keys
    "nlo2" and "nnlo2" are optional and will be drawn dashed in the
    lower panel.

    legendopts: a kwargs dict of options to be passed to legend(..) as
    well as the "what"-key indicating whether the legend such be
    placed in the lower panel (l, default), upper panel (u), or as a
    figlegend (fig). Notable is the "loc"-key that places the legend
    inside the object specified by "what". Possible values are (cf.
    legend)

        'upper right'
        'upper left'
        'lower left'
        'lower right'
        'right'
        'center left'
        'center right'
        'lower center'
        'upper center'
        'center'

    nomule: if set to True, no mule will be printed

    Returns the figure as well as all axis created
    """


    legend = legend.copy()
    legendopts = legendopts.copy()
    if labelsigma is None:
        labelsigma = r'$\D\sigma$'

    kwargs = {
        'labelx': labelx,
        'labupleft': labelsigma,
        'downalign': [0,0]
    }
    if type(labelknlo) == dict:
        kwargs['labdownleft'] = labelknlo
    else:
        kwargs['labdownleft'] = {
            'ylabel': labelknlo,
            'color': orderscheme['nlo']
        }
    if type(labelknlo) == dict:
        kwargs['labdownright'] = labelknnlo
    else:
        kwargs['labdownright'] = {
            'ylabel': labelknnlo,
            'color': orderscheme['nnlo']
        }

    if type(sigma) != dict:
        raise ValueError('kplot takes dicts!')
    if 'lo' not in sigma:
        raise KeyError('kplot: no leading order')
    if 'nlo' not in sigma:
        raise KeyError('kplot: no next-to-leading order')
    if 'nnlo' in sigma:
        orders = ['lo', 'nlo', 'nnlo']
        xsec = {
            'lo': sigma['lo'],
            'nlo': addplots(sigma['lo'], sigma['nlo']),
            'nnlo': addplots(
                sigma['lo'],
                addplots(sigma['nlo'], sigma['nnlo'])
            )
        }
    else:
        try:
            show.remove(2)
        except ValueError:
            pass
        try:
            showk.remove(2)
        except ValueError:
            pass
        orders = ['lo', 'nlo']
        xsec = {
            'lo': sigma['lo'],
            'nlo': addplots(sigma['lo'], sigma['nlo'])
        }

    if 1 in showk:
        kwargs['downleft'] = divideplots(sigma['nlo'], xsec['lo'])
        kwargs['coldownleft'] = [orderscheme['nlo']]
        if 'nlo2' in sigma:
            kwargs['downleft'] = [
                kwargs['downleft'],
                {'p': divideplots(sigma['nlo2'], xsec['lo']), 'linestyle': linestyle2}
            ]
            kwargs['coldownleft'] *= 2
    if 2 in showk:
        kwargs['downright'] = divideplots(sigma['nnlo'], xsec['nlo'])
        kwargs['coldownright'] = [orderscheme['nnlo']]
        if 'nnlo2' in sigma:
            if 'nlo2' in sigma:
                nlo2 = sigma['nlo2']
            else:
                nlo2 = sigma['nlo']
            kwargs['downright'] = [
                kwargs['downright'],
                {'p': divideplots(sigma['nnlo2'], addplots(nlo2, xsec['lo'])), 'linestyle': linestyle2}
            ]
            kwargs['coldownright'] *= 2

    kwargs['upleft'] = [
        xsec[orders[i]] for i in show
    ]
    kwargs['colupleft'] = [
        orderscheme[orders[i]] for i in show
    ]

    fig, axs = twopanel(**kwargs)
    if 1 in showk:
        axs[1].tick_params(labelcolor=orderscheme['nlo'], axis='y')
    if 2 in showk and 'nnlo' in sigma:
        axs[2].tick_params(labelcolor=orderscheme['nnlo'], axis='y')

    axs[1].axhline(0, color='black', linewidth=0.4, zorder=1)
    plegend = [
        (
            matplotlib.lines.Line2D([0], [0], color=orderscheme[i]),
            legend[i]
        )
        for i in sorted(list(set(orders[i] for i in show+showk)))
        if i in legend
    ]

    if 'nlo2' in sigma and 'nlo2' in legend:
        plegend.append((
            matplotlib.lines.Line2D([0], [0], color=orderscheme['nlo'], linestyle=linestyle2),
            legend['nlo2']
        ))
    if 'nnlo2' in sigma and 'nnlo2' in legend:
        plegend.append((
            matplotlib.lines.Line2D([0], [0], color=orderscheme['nnlo'], linestyle=linestyle2),
            legend['nnlo2']
        ))

    plegend = list(zip(*plegend))


    what = {
        'fig': fig, 'u': axs[0], 'l': axs[1]
    }[legendopts.pop('what', 'u')]
    what.legend(plegend[0], plegend[1], **legendopts)

    if not nomule:
        mulify(fig)
    if 1 in showk:
        updateaxis(axs[1], fig)
    if 2 in showk and 'nnlo' in sigma:
        updateaxis(axs[2], fig)
    return fig, axs
