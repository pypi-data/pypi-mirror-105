# Stolen from
# https://github.com/ryutok/mpl_axes_aligner


def _calc_rorg(org, ival, fval):
    rorg = (org - ival) / (fval - ival)
    if rorg < 0:
        rorg = 0
        ival = org
    elif rorg > 1:
        rorg = 1
        fval = org
    return rorg, ival, fval


def _calc_pos(org1, org2, lim1, lim2):
    ival1, fval1 = lim1
    ival2, fval2 = lim2

    rorg1, ival1, fval1 = _calc_rorg(org1, ival1, fval1)
    rorg2, ival2, fval2 = _calc_rorg(org2, ival2, fval2)
    pos = (rorg1 + rorg2) / 2.

    if pos == 0 or pos == 1:
        print('When pos=None, at least one origin should be ' + \
              'within the initial plotting range.')
        pos = 0.5

    return pos


def _expand_range(org, pos, ival, fval):
    if pos <= 0 or pos >= 1:
        raise ValueError('When expand=True, the position to align the origin '
                         'should be 0 < pos < 1.')

    rorg = (org - ival) / (fval - ival)
    if rorg > pos:
        fval = (org - ival + pos*ival) / pos
    else:
        ival = (org - pos*fval) / (1. - pos)
    return ival, fval


def shiftyaxis(ax, org, pos, expand=False):
    bottom, top = ax.get_ylim()
    bottom, top = _expand_range(org, pos, bottom, top)
    ax.set_ylim(bottom, top)


def yaxes(ax1, ax2, y1=1, y2=None):
    """
    yaxes(ax1, ax2, y=1) changes the limits of ax1 and ax2 to align the
    values of y on both axis.

    yaxes(ax1, y1, ax2, y2) changes the limits of the axis ax1 and ax2
    such that the value for y1 on ax1 is aligned to the value of y2 on
    ax2.
    """
    if y2 is None:
        y2 = y1
    # Get plotting ranges
    try:
        lim1 = list(ax1.get_ylim())
        lim2 = list(ax2.get_ylim())
    except AttributeError or TypeError:
        raise TypeError('"ax1" and "ax2" should be Axes objects of '
                        'matplotlib.')

    # Calculate the position
    pos = _calc_pos(y1, y2, lim1, lim2)

    # Apply the new ranges
    shiftyaxis(ax1, y1, pos, True)
    shiftyaxis(ax2, y2, pos, True)
