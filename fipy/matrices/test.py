from __future__ import unicode_literals
__all__ = []

from fipy.tests.doctestPlus import _LateImportDocTestSuite
import fipy.tests.testProgram
from fipy.solvers import solver

if solver == 'trilinos':
    docTestModuleNames = ('trilinosMatrix', 'pysparseMatrix')
elif solver == 'no-pysparse':
    docTestModuleNames = ('trilinosMatrix',)
elif solver in ['scipy', 'pyamg']:
    docTestModuleNames = ('scipyMatrix',)
elif solver == 'pysparse':
    docTestModuleNames = ('pysparseMatrix',)
elif solver == 'pyamgx':
    docTestModuleNames = ('scipyMatrix',)
elif solver == 'petsc':
    docTestModuleNames = ('petscMatrix',)
else:
    raise ImportError(f'Unknown solver package {solver}')

def _suite():
    return _LateImportDocTestSuite(docTestModuleNames=docTestModuleNames, base=__name__)

if __name__ == '__main__':
    fipy.tests.testProgram.main(defaultTest='_suite')
