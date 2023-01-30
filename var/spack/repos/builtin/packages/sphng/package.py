# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install sphng
#
# You can edit this file again by typing:
#
#     spack edit sphng
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *
import os

class Sphng(MakefilePackage):
    """sphNG benchmark for DiRAC."""

    homepage = "https://github.com/UniOfLeicester/benchmark-sphng"
    git = "ssh://git@github.com/UniOfLeicester/benchmark-sphng.git"

    maintainers = ["TomMelt"]

    version("v1.0.0", tag="v1.0.0")

    executables = [r"^sph_tree_rk_gradh$"]

    depends_on("mpi")

    parallel=False

    def edit(self, spec, prefix):

        self.fc = spack_fc if "~mpi" in spec else spec["mpi"].mpifc

        env['PREFIX'] = prefix
        env['SYSTEM'] = "dirac3-intel19"

        env['FC'] = self.fc
        env['OMPFLAG'] = self.compiler.openmp_flag
        if self.compiler.name == 'intel':
            env['FFLAGS'] = "-O3 -mavx2 -mfma -mcmodel=medium -warn uninitialized -warn truncated_source -warn interfaces -nogen-interfaces -DINCMPI"
            env['DBLFLAG'] = "-r8"
            env['DEBUGFLAG'] = "-check all -traceback -g -fpe0 -fp-stack-check -heap-arrays -O0"
            env['ENDIANFLAGBIG'] = "-convert big_endian"
            env['ENDIANFLAGLITTLE'] = "-convert little_endian"
        elif self.compiler.name == 'gcc':
            env['FFLAGS'] = "-m64 -mcmodel=medium -O3 -I. -Wall -Wno-conversion -Wno-unused-dummy-argument -Wno-maybe-uninitialized -Warray-temporaries"
            env['DBLFLAG'] = "-fdefault-real-8 -fdefault-double-8"
            env['DEBUGFLAG'] = "-g"
            env['ENDIANFLAGBIG'] = "-fconvert=big-endian"
            env['ENDIANFLAGLITTLE'] = "-fconvert=little-endian"
        else:
            msg  = "The compiler you are building with, "
            msg += "'{0}', is not supported by sphng yet."
            raise InstallError(msg.format(self.compiler.name))

    def build(self, spec, prefix):

        make('mpi=yes openmp=yes gradhrk')

    def install(self, spec, prefix):

        make('install')
