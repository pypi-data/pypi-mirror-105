import struct
import re
import numpy as np
import time


def getplots(s):
    """
    Given a vegas dataset s, getplots(s) removes all the keys that are
    not distributions
    """
    if type(s) == dict:
        return sorted(list(set(s.keys()) - {
            'SHA','chi2a','iteration','msg','value','time',
            'ndo','randy','xi','runtime'
        }))
    elif type(s) == list:
        p = [set(getplots(i)) for i in s]
        return sorted(set.intersection(*p))


def read_record(fp, typ):
    """
    read_record(fp, typ) reads a single FORTRAN record of typ from the
    file pointer fp. Allowed types are anything that struct
    understands. Common types are

     * i: 32 bit signed integer (standard integer in Fortran)
     * I: 32 bit unsigned integer
     * q: 64 bit signed integer (integer*8 in Fortran)
     * c: 8 bit charater (character in Fortran)
     * d: 64 bit double precision (real(kind=prec) in Fortran, with
          default prec)

    Records are data structures that are build as follows:

      * 4 byte header: length of the record as a 32 bit unsigned
          integer, called l1
      * body of length l1
      * 4 byte footer: a repetition of l1 to make sure the record is
          properly closed.

    Records can contain multiple variables.
    """
    l1 = struct.unpack('<I', fp.read(4))[0]
    body = fp.read(l1)
    l2 = struct.unpack('<I', fp.read(4))[0]
    if l1 != l2:
        raise KeyError('Record is not properly close %d v %d' % (l1, l2))

    if l1 % struct.calcsize(typ):
        raise ValueError('%d does not divide %d' % (struct.calcsize(typ), l1))
    n = l1 // struct.calcsize(typ)
    body = struct.unpack('<'+typ*n, body)
    if typ == 'c':
        body = b''.join(body).decode()
        try:
            if type(body) == unicode:
                body = body.encode()
        except:
            pass
        return body
    else:
        if n == 1:
            return body[0]
        else:
            return body


def write_record(fp, typ, content):
    """
    write_record(fp, typ, content) writes a single FORTRAN record of
    typ containing content to the file pointer fp. Allowed types are
    anything that struct understands. Common types are

     * i: 32 bit signed integer (standard integer in Fortran)
     * I: 32 bit unsigned integer
     * q: 64 bit signed integer (integer*8 in Fortran)
     * c: 8 bit charater (character in Fortran)
     * d: 64 bit double precision (real(kind=prec) in Fortran, with
          default prec)

    Records are data structures that are build as follows:

      * 4 byte header: length of the record as a 32 bit unsigned
          integer, called l1
      * body of length l1
      * 4 byte footer: a repetition of l1 to make sure the record is
          properly closed.

    Records can contain multiple variables.
    """
    if type(content) == str and len(content) > 1:
        content = list(content)
    elif type(content) != list:
        content = [content]

    body = ''.join(
        struct.pack('<'+typ, i) for i in content
    )
    fp.write(struct.pack('<I', len(body)))
    fp.write(body)
    fp.write(struct.pack('<I', len(body)))


def guess_version(fp, inttype='i'):
    """
    guess_version(fp) tries to obtain the version of a vegas file (fp)
    using either the version string (since v3) or the file length (v1
    and v2).

    For v1 and v2 the inttype is assumed to be normal 32 bit integers.
    Otherwise inttype must be given as 'q'
    """
    fp.seek(0)
    magic = fp.read(17).replace(b'\00', b'')
    if magic == b'\t McMule  \t':
        version = read_record(fp, 'c').strip()
        vers, intiness = re.match('v(\\d+)([NL])', version).groups()

        return int(vers), {'N': 'i', 'L': 'q'}[intiness]

    # Test v1 vs. v2
    intsize = struct.calcsize(inttype)
    fp.seek(6893 + 3*intsize)
    nrq, nrbins = read_record(fp, inttype)
    fp.seek(6925 + 5*intsize + 22*nrq + 16*nrbins*nrq)
    try:
        time = read_record(fp, 'd')
        fp.seek(0)
        return 2, inttype
    except KeyError:
        fp.seek(0)
        return 1, inttype
    except struct.error:
        fp.seek(0)
        return 1, inttype


def importvegas(filename='', fp=None, inttype='i', returnev=False):
    """
    importvegas(filename="", fp=None) loads a vegas file, either
    specified by a filename or a file pointer. The function returns a
    vegas dict containing

     * 'time': the job's run time (since v2)
     * 'msg': any message. Usually this contains information on the
           state of the integrator (since v2)
     * 'SHA': the first 5 characters of the source-tree's SHA1 hash at
           compile time.
     * 'iteration': the number of iterations completed in this file
     * 'value': the best estimate for the cross section and its error
           as np.array([y, e])
     * 'chi2a': the chi^2 estimate of the integrator
     * all histograms as specified by their name(..) in user.f95
    """
    if not fp and filename:
        fp = open(filename, 'rb')
    version, inttype = guess_version(fp, inttype)
    dic = {}

    sha = read_record(fp, 'c')
    it = read_record(fp, inttype)
    ndo = read_record(fp, inttype)
    si = read_record(fp, 'd')
    swgt = read_record(fp, 'd')
    schi = read_record(fp, 'd')
    xi = np.reshape(read_record(fp, 'd'), (17, -1))
    randy = read_record(fp, inttype)

    if version > 2:
        nrq, nrbins, namelen = read_record(fp, inttype)
    else:
        nrq, nrbins = read_record(fp, inttype)
        namelen = 6

    bounds = np.reshape(read_record(fp, 'd'), (-1, nrq))
    names = read_record(fp, 'c')
    names = [
        names[namelen*i:(i+1)*namelen].strip().replace('\00', '')
        for i in range(len(names)//namelen)
    ]
    quant = np.array(read_record(fp, 'd'))

    if version > 1:
        dic['time'] = read_record(fp, 'd')
        dic['msg'] = read_record(fp, 'c').strip().replace('\00', '')
    else:
        dic['time'] = -1
        dic['msg'] = ''

    dic['SHA'] = sha
    dic['iteration'] = it
    dic['value'] = np.array([si/swgt, np.sqrt(1/swgt)])
    if it > 1:
        dic['chi2a'] = (schi-si**2/swgt)/(it-1)
    else:
        dic['chi2a'] = -1

    if returnev:
        dic['ndo'] = ndo
        dic['xi'] = xi
        dic['randy'] = randy

    if it > 1:
        if version >= 3:
            ouarray = lambda o, u, b: np.concatenate(([u], b, [o]))
        else:
            ouarray = lambda o, u, b: b

        delta = (bounds[1]-bounds[0])/nrbins
        nrbinsuo = nrbins + 2 if version > 2 else nrbins

        for i in range(nrq):
            if len(names[i]) == 0:
                continue
            if abs(delta[i]) < 1e-15:
                continue

            if names[i] in dic:
                names[i] += '2'
            x = ouarray(
                np.inf, -np.inf,
                np.around(
                    bounds[0,i] + delta[i]*(0.5+np.arange(nrbins)),
                    10
                )
            )
            y = quant[i:nrq*nrbinsuo:nrq] \
                / it / ouarray(1, 1, [delta[i]]*nrbins)
            e = np.sqrt(
                (quant[nrq*nrbinsuo+i::nrq]-quant[i:nrq*nrbinsuo:nrq]**2/it)
                / it / (it-1)
            ) / ouarray(1, 1, [delta[i]]*nrbins)
            dic[names[i]] = np.column_stack((x, y, e))

    if filename:
        fp.close()

    return dic


def exportvegas(dic, filename='', fp=None):
    """
    exportvegas(dic, filename="", fp=None) saves a vegas dict to a
    vegas file, either specified by a filename or a file pointer. The
    vegas dict may contain the following keys

     * 'time': the job's run time (default: CPU time since the start
           of the executing process, time.clock())
     * 'msg': any message (default: "Warning: Generated with Python")
     * 'SHA': the first five byte of a SHA1 hash of the state of the
           file (default: 00000)
     * 'iteration': the number of iterations completed in this file
           (default: 2, making sure that 1/(it-1) in various estimates
           are well-defined)
     * 'value': the best estimate for the cross section and its error
           as np.array([y, e])
     * 'chi2a': the chi^2 estimate of the integrator
     * all histograms as specified by their name(..) in user.f95
    """
    if not fp and filename:
        fp = open(filename, 'wb')

    fp.write('\t\000\000\000 McMule  \t\000\000\000')

    if 'SHA' not in dic:
        dic['SHA'] = '00000'
    if 'iteration' not in dic:
        dic['iteration'] = 2
    if 'ndo' not in dic:
        dic['ndo'] = -1
    if 'xi' not in dic:
        dic['xi'] = -np.ones((17,50))
    if 'randy' not in dic:
        dic['randy'] = -1
    if 'runtime' not in dic:
        dic['runtime'] = time.clock()
    if 'msg' not in dic:
        dic['msg'] = 'Warning: Generated with Python'

    while type(dic['chi2a']) == list:
        dic['chi2a'] = dic['chi2a'][0]

    plots = getplots(dic)

    y,e = dic['value']

    write_record(fp, 'c', 'v3N       ')
    write_record(fp, 'c', dic['SHA'])
    write_record(fp, 'i', dic['iteration'])
    write_record(fp, 'i', dic['ndo'])
    write_record(fp, 'd', y/e**2)
    write_record(fp, 'd', 1/e**2)
    write_record(
        fp, 'd',
        dic['chi2a']*(dic['iteration']-1) + y**2/e**2
    )

    write_record(fp, 'd', list(np.reshape(dic['xi'], (17*50))))
    write_record(fp, 'i', dic['randy'])

    nrbins = np.count_nonzero(~np.isinf(dic[plots[0]][:,0]))
    nrq = len(plots)
    namelen = max(max([len(i) for i in plots]),6)

    write_record(fp, 'i', [
        nrq,
        nrbins,
        namelen
    ])

    quant = np.zeros(2*(nrbins + 2)*nrq)

    minv = []
    maxv = []
    for i in range(len(plots)):
        pp = dic[plots[i]].copy()
        if len(pp) == 0:
            maxv.append(0)
            minv.append(0)
            continue
        if pp[0,0] != -np.inf:
            pp = np.concatenate(([[-np.inf,0,0]], pp))
        if pp[-1,0] != np.inf:
            pp = np.concatenate((pp, [[np.inf,0,0]]))

        delta = pp[2,0]-pp[1,0]
        maxv.append(pp[1,0] - delta/2 + nrbins * delta)
        minv.append(pp[1,0] - delta/2)

        delta = np.array([1] + [delta]*nrbins + [1])

        quant[i:nrq*(nrbins+2):nrq] = delta * dic['iteration'] * pp[:,1]

        if np.all(pp[:,2] == 0):
            quant[nrq*(nrbins + 2) + i::nrq] = \
                quant[i:nrq*(nrbins + 2):nrq]**2/dic['iteration']
        else:
            quant[nrq*(nrbins + 2) + i::nrq] = delta**2*dic['iteration']*(
                pp[:,2]**2*(dic['iteration']-1) + pp[:,1]**2
            )

    write_record(fp, 'd', minv+maxv)
    write_record(fp, 'c', ''.join([i.ljust(namelen) for i in plots]))
    write_record(fp, 'd', list(quant))

    write_record(fp, 'd', dic['runtime'])
    write_record(fp, 'c', dic['msg'])
