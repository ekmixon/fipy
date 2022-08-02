from __future__ import unicode_literals
import re

import numpy

scanf_e = "[-+]?(\d+(\.\d*)?|\d*\.\d+)([eE][-+]?\d+)?"

reCPU = re.compile(f"cpu time: ({scanf_e}) s / step / cell")
reRSZ = re.compile(f"max resident memory: ({scanf_e}) B / cell")
reVSZ = re.compile(f"max virtual memory: ({scanf_e}) B / cell")

def monitor(p):
    r = "".join(p.communicate()[0])

    cpu = reCPU.search(r, re.MULTILINE)
    rsz = reRSZ.search(r, re.MULTILINE)
    vsz = reVSZ.search(r, re.MULTILINE)

    def numOrNaN(m, g=1):
        return numpy.NaN if m is None else float(m.group(g))

    return (numOrNaN(cpu),
            numOrNaN(rsz),
            numOrNaN(vsz))
