#!/usr/bin/env python

## -*-Pyth-*-
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "matplotlibVectorViewer.py"
 #                                    created: 9/14/04 {2:48:25 PM} 
 #                                last update: 11/8/07 {6:51:16 PM} { 2:45:36 PM}
 #  Author: Jonathan Guyer <guyer@nist.gov>
 #  Author: Daniel Wheeler <daniel.wheeler@nist.gov>
 #  Author: James Warren   <jwarren@nist.gov>
 #    mail: NIST
 #     www: http://www.ctcms.nist.gov/fipy/
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  FiPy is an experimental
 # system.  NIST assumes no responsibility whatsoever for its use by
 # other parties, and makes no guarantees, expressed or implied, about
 # its quality, reliability, or any other characteristic.  We would
 # appreciate acknowledgement if the software is used.
 # 
 # This software can be redistributed and/or modified freely
 # provided that any derivative works bear some notice that they are
 # derived from it, and any modified versions bear some notice that
 # they have been modified.
 # ========================================================================
 #  See the file "license.terms" for information on usage and  redistribution
 #  of this file, and for a DISCLAIMER OF ALL WARRANTIES.
 #  
 #  Description: 
 # 
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2003-11-10 JEG 1.0 original
 # ###################################################################
 ##
 
__docformat__ = 'restructuredtext'

from fipy.tools import numerix
from matplotlibViewer import MatplotlibViewer
from fipy.variables.faceVariable import FaceVariable
from fipy.variables.cellVariable import CellVariable

class MatplotlibVectorViewer(MatplotlibViewer):
    """
    Displays a vector plot of a 2D rank-1 `CellVariable` or
    `FaceVariable` object using Matplotlib_

    .. _Matplotlib: http://matplotlib.sourceforge.net/

    """

    def __init__(self, vars, limits=None, title=None, scale=None, sparsity=None):
        """
        Creates a `Matplotlib2DViewer`.
        
            >>> from fipy import *
            >>> from fipy.tools.numerix import *
            >>> mesh = Grid2D(nx=50, ny=100, dx=0.1, dy=0.01)
            >>> x, y = mesh.getCellCenters()
            >>> xyVar = CellVariable(mesh=mesh, name="x y", value=x * y)
            >>> k = Variable(name="k")
            >>> viewer = MatplotlibVectorViewer(vars=sin(k * xyVar).getGrad(), 
            ...                                 # limits={'ymin':0.1, 'ymax':0.9},
            ...                                 title="MatplotlibVectorViewer test")
            >>> for kval in numerix.arange(0,10,1):
            ...     k.setValue(kval)
            ...     viewer.plot()
            >>> viewer._promptForOpinion()
            >>> del viewer

            >>> viewer = MatplotlibVectorViewer(vars=sin(k * xyVar).getFaceGrad(), 
            ...                                 # limits={'ymin':0.1, 'ymax':0.9},
            ...                                 title="MatplotlibVectorViewer test")
            >>> for kval in numerix.arange(0,10,1):
            ...     k.setValue(kval)
            ...     viewer.plot()
            >>> viewer._promptForOpinion()
            >>> del viewer

            >>> viewer = MatplotlibVectorViewer(vars=sin(k * xyVar).getFaceGrad(), 
            ...                                 # limits={'ymin':0.1, 'ymax':0.9},
            ...                                 title="MatplotlibVectorViewer test",
            ...                                 sparsity=1000)
            >>> for kval in numerix.arange(0,10,1):
            ...     k.setValue(kval)
            ...     viewer.plot()
            >>> viewer._promptForOpinion()
            >>> del viewer

        :Parameters:
          - `vars`: A `CellVariable` object.
          - `limits`: A dictionary with possible keys `'xmin'`, `'xmax'`, 
            `'ymin'`, `'ymax'`, `'datamin'`, `'datamax'`. Any limit set to 
            a (default) value of `None` will autoscale.
          - `title`: displayed at the top of the Viewer window
          - `scale`: if not `None`, scale all arrow lengths by this value
          - `sparsity`: if not `None`, then this number of arrows will be
            randomly chosen (weighted by the cell volume or face area)

        """
        MatplotlibViewer.__init__(self, vars = vars, limits = limits, title = title)

        var = self.vars[0]
        mesh = var.getMesh()

        if isinstance(var, FaceVariable):
            N = mesh._getNumberOfFaces() 
            V = mesh._getFaceAreas()
            X, Y = mesh.getFaceCenters()
        elif isinstance(var, CellVariable):
            N = mesh.getNumberOfCells() 
            V = mesh.getCellVolumes()
            X, Y = mesh.getCellCenters()

        if sparsity is not None and N > sparsity:
            self.indices = numerix.random.rand(N) * V
            self.indices = self.indices.getValue().argsort()[-sparsity:]
        else:
            self.indices = numerix.arange(N)

        X = numerix.take(X, self.indices, axis=-1)
        Y = numerix.take(Y, self.indices, axis=-1)
        
        U = V = numerix.ones(X.shape)
        
        import pylab
        
        self.quiver = pylab.quiver(X, Y, U, V, scale=scale)
        self.colorbar = False
        
        self._plot()
        
    def _getSuitableVars(self, vars):
        from fipy.meshes.numMesh.mesh2D import Mesh2D

        vars = [var for var in MatplotlibViewer._getSuitableVars(self, vars) \
                if (isinstance(var.getMesh(), Mesh2D) \
                    and (isinstance(var, FaceVariable) \
                         or isinstance(var, CellVariable)) and var.getRank() == 1)]
        if len(vars) == 0:
            from fipy.viewers import MeshDimensionError
            raise MeshDimensionError, "The mesh must be a Mesh2D instance"
        # this viewer can only display one variable
        return [vars[0]]
                
    def _plot(self):

        var = self.vars[0]
        mesh = var.getMesh()

        U, V = var.getNumericValue()

        U = numerix.take(U, self.indices, axis=-1)
        V = numerix.take(V, self.indices, axis=-1)

        self.quiver.set_UVC(U, V)
        
        import pylab
                            
        pylab.xlim(xmin = self._getLimit('xmin'))
        pylab.xlim(xmax = self._getLimit('xmax'))
        pylab.ylim(ymin = self._getLimit('ymin'))
        pylab.ylim(ymax = self._getLimit('ymax'))

if __name__ == "__main__": 
    import fipy.tests.doctestPlus
    fipy.tests.doctestPlus.execButNoTest()
