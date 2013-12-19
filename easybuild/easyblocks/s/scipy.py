##
# Copyright 2009-2013 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://vscentrum.be/nl/en),
# the Hercules foundation (http://www.herculesstichting.be/in_English)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# http://github.com/hpcugent/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
##
"""
EasyBuild support for building and installing scipy, implemented as an easyblock

@author: Stijn De Weirdt (Ghent University)
@author: Dries Verdegem (Ghent University)
@author: Kenneth Hoste (Ghent University)
@author: Pieter De Baets (Ghent University)
@author: Jens Timmerman (Ghent University)
"""
from distutils.version import LooseVersion

from easybuild.easyblocks.generic.fortranpythonpackage import FortranPythonPackage
import easybuild.tools.toolchain as toolchain


class EB_scipy(FortranPythonPackage):
    """Support for installing the scipy Python package as part of a Python installation."""

    def __init__(self, *args, **kwargs):
        """Set scipy-specific test command."""
        super(EB_scipy, self).__init__(*args, **kwargs)

        self.testinstall = True
        self.testcmd = "cd .. && python -c 'import numpy; import scipy; scipy.test(verbose=2)'"

    def install_step(self):
        """Custom install step for scipy: set extra installation options when needed."""
        if LooseVersion(self.version) >= LooseVersion('0.13'):
            # in recent scipy versions, additional compilation is done in the install step,
            # which requires unsetting $LDFLAGS
            if comp_fam in [toolchain.GCC, toolchain.CLANGGCC]:  # @UndefinedVariable
                self.cfg.update('preinstallopts', "unset LDFLAGS && ")
                self.cfg.update('installopts', "--fcompiler=gnu95")
