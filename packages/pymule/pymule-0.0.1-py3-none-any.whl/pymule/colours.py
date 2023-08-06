from cycler import cycler
from matplotlib import rc


# Mathematica colour scheme 112 `vibrant'

# Apply[
#   StringJoin["#", ##] &,
#   Map[
#     IntegerString[#, 16, 2] &,
#     Round[255 List @@@ ColorData[112] /@ {2, 3, 4, 1, 5, 6, 7, 8, 9, 10}]
#   ],
#   {1}
# ]
schema = [
  '#84b3d6', '#f0cd88', '#94c266', '#d58a83', '#9ba7d1'
]
schema = ['#3f88bf', '#e8b145', '#58a010', '#bd483d', '#6376b7']
rc('axes', prop_cycle=cycler('color', schema))

orderscheme = {
  'lo': 'C2', 'nlo': 'C0', 'nnlo': 'C3', 'np': 'C1'
}

mathcolour = '#00009c'

defcol = ['C%d' % i for i in range(10)]


def alpha_composite(bg, fg, alpha):
    import matplotlib.colors
    def hex2rgb(h):
        h = h.lstrip('#')
        return tuple(int(h[i:i+2], 16)/255. for i in (0, 2, 4))
    bg = hex2rgb(matplotlib.colors.to_hex(bg))
    fg = hex2rgb(matplotlib.colors.to_hex(fg))
    return '#%02x%02x%02x' % (
        int(255.*((1-alpha) * bg[0] + alpha * fg[0])),
        int(255.*((1-alpha) * bg[1] + alpha * fg[1])),
        int(255.*((1-alpha) * bg[2] + alpha * fg[2]))
    )
