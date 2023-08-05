# ------------------------------------------------------------------------------
# Copyright (C) 2018-2019 Maximilian Stahlberg
#
# This file is part of PICOS.
#
# PICOS is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# PICOS is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------

"""Implementation of :class:`MOSEKSolver`."""

import math
import sys

import cvxopt

from ..apidoc import api_end, api_start
from ..constraints import (AffineConstraint, ConvexQuadraticConstraint,
                           DummyConstraint, LMIConstraint, RSOCConstraint,
                           SOCConstraint)
from ..expressions import (AffineExpression, BinaryVariable, IntegerVariable,
                           QuadraticExpression)
from ..modeling.footprint import Specification
from ..modeling.solution import (PS_FEASIBLE, PS_ILLPOSED, PS_INFEASIBLE,
                                 PS_UNBOUNDED, PS_UNKNOWN, SS_FEASIBLE,
                                 SS_INFEASIBLE, SS_OPTIMAL, SS_UNKNOWN)
from .solver import ProblemUpdateError, Solver

_API_START = api_start(globals())
# -------------------------------


class MOSEKSolver(Solver):
    """Interface to the MOSEK solver via its low level Optimizer API.

    Supports both MOSEK 8 and 9.

    The low level API is tedious to interface, but is currently much faster than
    the high level Fusion API, which would be the prefered interface otherwise.
    """

    SUPPORTED = Specification(
        objectives=[
            AffineExpression,
            QuadraticExpression],
        constraints=[
            DummyConstraint,
            AffineConstraint,
            SOCConstraint,
            RSOCConstraint,
            ConvexQuadraticConstraint,
            LMIConstraint])

    @classmethod
    def supports(cls, footprint, explain=False):
        """Implement :meth:`~.solver.Solver.supports`."""
        result = Solver.supports(footprint, explain)
        if not result or (explain and not result[0]):
            return result

        # No nonconvex quadratic objectives.
        if footprint.nonconvex_quadratic_objective:
            if explain:
                return False, "Problems with nonconvex quadratic objectives."
            else:
                return False

        conic = any(("con", constraint) in footprint
            for constraint in (SOCConstraint, RSOCConstraint, LMIConstraint))

        quadratic = footprint.objective.clstype is QuadraticExpression \
            or ("con", ConvexQuadraticConstraint) in footprint

        # No mixing of quadratic and conic problems.
        if conic and quadratic:
            if explain:
                return (False,
                    "Problems that mix conic and quadratic constraints.")
            else:
                return False

        # No integer SDPs.
        if footprint.integer and ("con", LMIConstraint) in footprint:
            if explain:
                return False, "Integer Semidefinite Programs."
            else:
                return False

        if footprint not in cls.SUPPORTED:
            if explain:
                return False, cls.SUPPORTED.mismatch_reason(footprint)
            else:
                return False

        return (True, None) if explain else True

    @classmethod
    def default_penalty(cls):
        """Implement :meth:`~.solver.Solver.default_penalty`."""
        return 0.0  # Commercial solver.

    @classmethod
    def test_availability(cls):
        """Implement :meth:`~.solver.Solver.test_availability`."""
        cls.check_import("mosek")

    @classmethod
    def names(cls):
        """Implement :meth:`~.solver.Solver.names`."""
        return "mosek", "MOSEK (Optimizer)", "MOSEK via Optimizer API"

    @classmethod
    def is_free(cls):
        """Implement :meth:`~.solver.Solver.is_free`."""
        return False

    def __init__(self, problem):
        """Initialize a MOSEK (Optimizer) solver interface.

        :param ~picos.Problem problem: The problem to be solved.
        """
        super(MOSEKSolver, self).__init__(problem)

        self._mosekVarOffset = dict()
        """Maps a PICOS (multidimensional) variable to a MOSEK scalar variable
        (start) index."""

        self._mosekLinConOffset = dict()
        """Maps a PICOS (multidimensional) linear constraint to a MOSEK scalar
        constraint (start) index."""

        self._mosekQuadConIndex = dict()
        """Maps a PICOS quadratic constraint to a MOSEK constraint index."""

        self._mosekCone = dict()
        """
        Maps a PICOS SOCC or RSOCC to a triple:

        - The first entry is the index of a MOSEK conic constraint.
        - The second entry is a list of MOSEK scalar (auxiliary) variable
          indices that appear in the MOSEK conic constraint.
        - The third entry is another list of same size containing auxiliary
          constraints (or None). If an entry in the second list is None, then
          the corresponding index in the first list is of a proper MOSEK scalar
          variable instead of an auxiliary one, which can happen at most once
          per variable and only if the structure of the PICOS constraint allows
          it (that is, if the repspective entry of the cone member happens to be
          a PICOS scalar variable as opposed to a composed affine expression).
        """

        self._mosekLMI = dict()
        """Maps a PICOS LMI to a pair representing its MOSEK representation. The
        first entry is the index of a MOSEK symmetric PSD "bar variable", the
        second entry is the offset for a number of scalar linear equalities."""

        self._mosekBarUnitCoefs = dict()
        """Maps the row (column) count of a symmetric matrix to a list of MOSEK
        symmetric coefficient matrices. More precisely, if X is a n×n symmetric
        matrix, 0 ≤ k ≤ n*(n+1)/2, then <_mosekBarUnitCoefs[n][k], X> = h(X)[k]
        where h refers to the lower-triangular, column-major half-vectorization
        of X. These matrices are used to represent LMIs. Unlike values of
        _mosekLMI, they are shared between LMIs of same size."""

    def reset_problem(self):
        """Implement :meth:`~.solver.Solver.reset_problem`."""
        self.int = None

        self._mosekVarOffset.clear()
        self._mosekLinConOffset.clear()
        self._mosekQuadConIndex.clear()
        self._mosekCone.clear()
        self._mosekLMI.clear()
        self._mosekBarUnitCoefs.clear()

    @classmethod
    def _get_environment(cls):
        if not hasattr(cls, "mosekEnvironment"):
            import mosek
            cls.mosekEnvironment = mosek.Env()

        return cls.mosekEnvironment

    env = property(lambda self: self.__class__._get_environment())
    """This references a MOSEK environment, which is shared among all
    MOSEKSolver instances. (The MOSEK documentation states that "[a]ll tasks in
    the program should share the same environment.")"""

    @classmethod
    def _get_major_version(cls):
        if not hasattr(cls, "mosekVersion"):
            import mosek
            cls.mosekVersion = mosek.Env.getversion()

        return cls.mosekVersion[0]

    ver = property(lambda self: self.__class__._get_major_version())
    """The major version of the available MOSEK library."""

    @staticmethod
    def _streamprinter(text):
        sys.stdout.write(text)
        sys.stdout.flush()

    @staticmethod
    def _low_tri_indices(rowCount):
        """Yield lower triangular (row, col) indices in column-major order."""
        for col in range(rowCount):
            for row in range(col, rowCount):
                yield (row, col)

    def _scalar_affinexp_pic2msk(self, picosExpression):
        assert len(picosExpression) == 1
        return picosExpression.sparse_rows(self._mosekVarOffset)[0]

    def _affinexp_pic2msk(self, picosExpression):
        return picosExpression.sparse_rows(self._mosekVarOffset)

    def _quadexp_pic2msk(self, picosExpression):
        """Transform a quadratic expression from PICOS to MOSEK.

        Tranforms the quadratic part of a PICOS quadratic expression to a
        symmetric, sparse biliniar form of which only the lower triangular
        entries are given, and that can be used with MOSEK's variable vector.
        Note that MOSEK applies a built-in factor of 0.5 to all biliniar forms
        while PICOS doesn't, so a factor of 2 is applied here to cancel it out.
        """
        assert isinstance(picosExpression, QuadraticExpression)
        numVars = self.int.getnumvar()

        # Make a sparse representation of the strict lower, diagonal and strict
        # upper parts of the matrix.
        IL, JL, VL = [], [], []
        ID, JD, VD = [], [], []
        IU, JU, VU = [], [], []
        for (picosVar1, picosVar2), picosCoefs \
        in picosExpression._sparse_quads.items():
            for sparseIndex in range(len(picosCoefs)):
                localVar1Index   = picosCoefs.I[sparseIndex]
                localVar2Index   = picosCoefs.J[sparseIndex]
                localCoefficient = picosCoefs.V[sparseIndex]
                mskVar1Index = self._mosekVarOffset[picosVar1] + localVar1Index
                mskVar2Index = self._mosekVarOffset[picosVar2] + localVar2Index

                if   mskVar2Index < mskVar1Index:
                    I, J, V = IL, JL, VL
                elif mskVar1Index < mskVar2Index:
                    I, J, V = IU, JU, VU
                else:
                    I, J, V = ID, JD, VD

                I.append(mskVar1Index)
                J.append(mskVar2Index)
                V.append(localCoefficient)

        # Compute the lower triangular part of the biliniar form.
        L = cvxopt.spmatrix(VL, IL, JL, (numVars, numVars))
        D = cvxopt.spmatrix(VD, ID, JD, (numVars, numVars))
        U = cvxopt.spmatrix(VU, IU, JU, (numVars, numVars))
        Q = 2*D + L + U.T

        # Return it as a sparse triple for MOSEK to consume.
        return list(Q.I), list(Q.J), list(Q.V)

    def _import_variable(self, picosVar):
        import mosek

        numVars = self._mosekVarOffset[picosVar] = self.int.getnumvar()
        dim     = picosVar.dim
        indices = range(numVars, numVars + dim)
        self.int.appendvars(dim)

        # Set the variable type.
        if isinstance(picosVar, (IntegerVariable, BinaryVariable)):
            self.int.putvartypelist(
                indices, [mosek.variabletype.type_int]*dim)

        # Import bounds, including the implied bounds of a BinaryVariable.
        if isinstance(picosVar, BinaryVariable):
            self.int.putvarboundlist(
                indices, [mosek.boundkey.ra]*dim, [0]*dim, [1]*dim)
        else:
            boundKeys   = [mosek.boundkey.fr]*dim
            lowerBounds = [0.0]*dim
            upperBounds = [0.0]*dim

            lower, upper = picosVar.bound_dicts

            for i, b in lower.items():
                boundKeys[i] = mosek.boundkey.lo
                lowerBounds[i] = b

            for i, b in upper.items():
                if boundKeys[i] == mosek.boundkey.fr:
                    boundKeys[i] = mosek.boundkey.up
                else:  # Also has a lower bound.
                    if lowerBounds[i] == b:
                        boundKeys[i] = mosek.boundkey.fx
                    else:
                        boundKeys[i] = mosek.boundkey.ra

                upperBounds[i] = b

            self.int.putvarboundlist(
                indices, boundKeys, lowerBounds, upperBounds)

    def _import_linear_constraint(self, picosConstraint):
        import mosek

        numCons = self.int.getnumcon()
        conLen  = len(picosConstraint)
        self.int.appendcons(conLen)

        rows = picosConstraint.sparse_Ab_rows(self._mosekVarOffset)

        if picosConstraint.is_equality():
            boundKey = mosek.boundkey.fx
        elif picosConstraint.is_increasing():
            boundKey = mosek.boundkey.up
        else:
            boundKey = mosek.boundkey.lo

        for localConIndex, (mosekVarIndices, coefs, offset) in enumerate(rows):
            mosekConIndex = numCons + localConIndex

            self.int.putarow(mosekConIndex, mosekVarIndices, coefs)
            self.int.putconbound(mosekConIndex, boundKey, offset, offset)

        self._mosekLinConOffset[picosConstraint] = numCons

    def _import_quad_constraint(self, picosConstraint):
        # Import the linear part first.
        picosLinConPart = picosConstraint.le0.aff < 0
        self._import_linear_constraint(picosLinConPart)
        mosekConIndex = self._mosekLinConOffset.pop(picosLinConPart)

        # Add the quadratic part.
        self.int.putqconk(
            mosekConIndex, *self._quadexp_pic2msk(picosConstraint.le0))

        self._mosekQuadConIndex[picosConstraint] = mosekConIndex

    def _var_was_used_in_cone(self, mosekVariableIndex, usedJustNow=[]):
        if mosekVariableIndex in usedJustNow:
            return True
        for _, mosekVarIndices, _ in self._mosekCone.values():
            if mosekVariableIndex in mosekVarIndices:
                return True
        return False

    def _import_quad_conic_constraint(self, picosConstraint):
        import mosek

        isRotated = isinstance(picosConstraint, RSOCConstraint)
        mosekVars, mosekCons = [], [None]*len(picosConstraint)

        # Get an initial MOSEK representation of the cone member.
        entries = []
        if isRotated:
            # MOSEK internally adds a factor of 2 to the upper bound while PICOS
            # doesn't, so cancel it out by adding a factor of 1/sqrt(2) to both
            # factors of the upper bound.
            f = 1.0 / math.sqrt(2.0)
            entries.append(self._scalar_affinexp_pic2msk(f*picosConstraint.ub1))
            entries.append(self._scalar_affinexp_pic2msk(f*picosConstraint.ub2))
        else:
            entries.append(self._scalar_affinexp_pic2msk(picosConstraint.ub))
        entries += self._affinexp_pic2msk(picosConstraint.ne)

        # Map cone member entries to existing MOSEK variables, if possible.
        mosekVarsMissing = []
        for scalarVarNum, (indices, values, offset) in enumerate(entries):
            if len(values) == 1 and values[0] == 1.0 and offset == 0.0 \
            and not self._var_was_used_in_cone(indices[0], mosekVars):
                mosekVars.append(indices[0])
            else:
                mosekVars.append(None)
                mosekVarsMissing.append(scalarVarNum)

        # Create auxiliary variables and constraints.
        numAux = len(mosekVarsMissing)
        auxVarOffset = self.int.getnumvar()
        auxConOffset = self.int.getnumcon()
        self.int.appendvars(numAux)
        self.int.appendcons(numAux)

        # Mosek fixes (!) new variables at zero, so set them free.
        self.int.putvarboundlist(range(auxVarOffset, auxVarOffset + numAux),
            [mosek.boundkey.fr]*numAux, [0.0]*numAux, [0.0]*numAux)

        # Constrain the auxiliary variables to be equal to the cone member
        # entries for which no existing MOSEK variable could be used.
        for auxNum, missingVarIndex in enumerate(mosekVarsMissing):
            auxVarIndex = auxVarOffset + auxNum
            auxConIndex = auxConOffset + auxNum

            # Prepare the auxiliary constraint.
            indices, values, offset = entries[missingVarIndex]

            # TODO: Instead of always creating a constraint, fix variables via
            #       their bound whenever possible.
            # if len(indices) is 0:
            #     if self._debug():
            #         self._debug("  Fixing MOSEK auxiliary variable: "
            #                 "x[{}] = {}".format(auxVarIndex, offset))
            #
            #     self.int.putvarbound(
            #         auxVarIndex, mosek.boundkey.fx, offset, offset)
            # else:
            indices.append(auxVarIndex)
            values.append(-1.0)

            if self._debug():
                self._debug("  Adding MOSEK auxiliary constraint: "
                    "{}.T * x{} = {}".format(values, indices, -offset))

            # Add the auxiliary constraint.
            self.int.putarow(auxConIndex, indices, values)
            self.int.putconbound(
                auxConIndex, mosek.boundkey.fx, -offset, -offset)

            # Complete the mapping of cone member entries to MOSEK (auxiliary)
            # variables (and auxiliary constraints).
            mosekVars[missingVarIndex] = auxVarIndex
            mosekCons[missingVarIndex] = auxConIndex

        if self._debug():
            self._debug("  Adding MOSEK conic constraint: {} in {}".format(
                mosekVars, "Qr" if isRotated else "Q"))

        # Add the conic constraint.
        coneIndex = self.int.getnumcone()
        mosekCone = mosek.conetype.rquad if isRotated else mosek.conetype.quad
        self.int.appendcone(mosekCone, 0.0, mosekVars)

        self._mosekCone[picosConstraint] = (coneIndex, mosekVars, mosekCons)

    def _import_sdp_constraint(self, picosConstraint):
        import mosek

        n = picosConstraint.size[0]
        dim = (n*(n + 1)) // 2

        # MOSEK does not support general LMIs but so called "bar vars" which
        # are variables in the symmetric positive semidefinite cone. We use them
        # in combination with linear equalities to represent the LMI.
        barVar = self.int.getnumbarvar()
        mosekConOffset = self.int.getnumcon()
        self.int.appendbarvars([n])
        self.int.appendcons(dim)

        # MOSEK uses a storage of symmetric coefficient matrices that are used
        # as dot product coefficients to build scalar constraints involving both
        # "bar vars" and normal scalar variables. We build a couple of these
        # matrices to be able to select individual entries of our "bar vars".
        # More precisely, if X is a n×n symmetric matrix and 0 ≤ k ≤ n*(n+1)/2,
        # then <Units[n][k],X> = h(X)[k] where h refers to the lower-triangular,
        # column-major half-vectorization of X.
        if n in self._mosekBarUnitCoefs:
            Units = self._mosekBarUnitCoefs[n]
        else:
            Units = self._mosekBarUnitCoefs[n] = [
                self.int.appendsparsesymmat(
                    n, [row], [col], [1.0 if row == col else 0.5])
                for row, col in self._low_tri_indices(n)]

        # We iterate over the lower triangular scalar sub-expressions of the
        # expression that the PICOS constraint states to be PSD, and constrain
        # them to be eqal to the MOSEK "bar var" at the same index.
        psd = picosConstraint.psd
        psdRows = psd.sparse_rows(self._mosekVarOffset, lowerTriangle=True)
        for lowTriIndex, (row, col) in enumerate(self._low_tri_indices(n)):
            mosekConIndex = mosekConOffset + lowTriIndex
            indices, coefficients, offset = psdRows[lowTriIndex]

            # The lower-triangular entries in the PSD-constrained matrix …
            self.int.putarow(mosekConIndex, indices, coefficients)

            # … minus the corresponding bar var entries …
            self.int.putbaraij(
                mosekConIndex, barVar, [Units[lowTriIndex]], [-1.0])

            # … should equal zero.
            self.int.putconbound(
                mosekConIndex, mosek.boundkey.fx, -offset, -offset)

            if self._debug():
                self._debug("  Index {} ({}, {}): indices = {}, coefs = {}"
                    .format(lowTriIndex, row, col, indices, coefficients))

        self._mosekLMI[picosConstraint] = (barVar, mosekConOffset)

    def _import_constraint(self, picosConstraint):
        if self._debug():
            self._debug("Importing Constraint: {}".format(picosConstraint))

        if   isinstance(picosConstraint, AffineConstraint):
            self._import_linear_constraint(picosConstraint)
        elif isinstance(picosConstraint, ConvexQuadraticConstraint):
            self._import_quad_constraint(picosConstraint)
        elif isinstance(picosConstraint, SOCConstraint) \
        or   isinstance(picosConstraint, RSOCConstraint):
            self._import_quad_conic_constraint(picosConstraint)
        elif isinstance(picosConstraint, LMIConstraint):
            self._import_sdp_constraint(picosConstraint)
        else:
            assert isinstance(picosConstraint, DummyConstraint), \
                "Unexpected constraint type: {}".format(
                picosConstraint.__class__.__name__)

    def _reset_objective(self):
        # Reset affine part.
        numVars = self.int.getnumvar()
        self.int.putclist(range(numVars), [0.0]*numVars)
        self.int.putcfix(0.0)

        # Reset quadratic part.
        self.int.putqobj([], [], [])

    def _import_affine_objective(self, picosObjective):
        mosekIndices      = []
        mosekCoefficients = []

        for picosVar, picosCoef in picosObjective._linear_coefs.items():
            for localIndex in range(picosVar.dim):
                if picosCoef[localIndex]:
                    mosekIndex = self._mosekVarOffset[picosVar] + localIndex
                    mosekIndices.append(mosekIndex)
                    mosekCoefficients.append(picosCoef[localIndex])

        self.int.putclist(mosekIndices, mosekCoefficients)

        if picosObjective._constant_coef:
            self.int.putcfix(picosObjective._constant_coef[0])

    def _import_quadratic_objective(self, picosObjective):
        # Import the quadratic part.
        self.int.putqobj(*self._quadexp_pic2msk(picosObjective))

        # Import the affine part.
        self._import_affine_objective(picosObjective.aff)

    def _import_objective(self):
        import mosek

        picosSense, picosObjective = self.ext.no

        # Import objective sense.
        if picosSense == "min":
            self.int.putobjsense(mosek.objsense.minimize)
        else:
            assert picosSense == "max"
            self.int.putobjsense(mosek.objsense.maximize)

        # Import objective function.
        if isinstance(picosObjective, AffineExpression):
            self._import_affine_objective(picosObjective)
        else:
            assert isinstance(picosObjective, QuadraticExpression)
            self._import_quadratic_objective(picosObjective)

    def _import_problem(self):
        # Create a problem instance.
        self.int = self.env.Task()

        # Import variables.
        for variable in self.ext.variables.values():
            self._import_variable(variable)

        # Import constraints.
        for constraint in self.ext.constraints.values():
            self._import_constraint(constraint)

        # Set objective.
        self._import_objective()

    def _update_problem(self):
        for oldConstraint in self._removed_constraints():
            raise ProblemUpdateError("PICOS does not support removing "
                "constraints from a MOSEK instance.")

        for oldVariable in self._removed_variables():
            raise ProblemUpdateError("PICOS does not support removing variables"
                " from a MOSEK instance.")

        for newVariable in self._new_variables():
            self._import_variable(newVariable)

        for newConstraint in self._new_constraints():
            self._import_constraint(newConstraint)

        if self._objective_has_changed():
            self._reset_objective()
            self._import_objective()

    def _solve(self):
        import mosek

        # Determine whether a basic solution will be available.
        # TODO: Give Problem an interface for checks like this.
        isLP = isinstance(self.ext.no.function, AffineExpression) \
            and all(isinstance(constraint, AffineConstraint)
            for constraint in self.ext.constraints.values())

        # Reset all solver options to default.
        self.int.setdefaults()

        # verbosity
        if self._verbose():
            self.int.set_Stream(mosek.streamtype.log, self._streamprinter)
            self.int.putintparam(mosek.iparam.log, self.ext.verbosity())

        # abs_prim_fsb_tol
        if self.ext.options.abs_prim_fsb_tol is not None:
            value = self.ext.options.abs_prim_fsb_tol

            # Interior-point primal feasibility tolerances.
            self.int.putdouparam(mosek.dparam.intpnt_tol_pfeas,    value)
            self.int.putdouparam(mosek.dparam.intpnt_co_tol_pfeas, value)
            self.int.putdouparam(mosek.dparam.intpnt_qo_tol_pfeas, value)
            if self.ver <= 8:
                self.int.putdouparam(mosek.dparam.intpnt_nl_tol_pfeas, value)

            # Simplex primal feasibility tolerance.
            self.int.putdouparam(mosek.dparam.basis_tol_x, value)

            # Mixed-integer (primal) feasibility tolerance.
            self.int.putdouparam(mosek.dparam.mio_tol_feas, value)

        # abs_dual_fsb_tol
        if self.ext.options.abs_dual_fsb_tol is not None:
            value = self.ext.options.abs_dual_fsb_tol

            # Interior-point dual feasibility tolerances.
            self.int.putdouparam(mosek.dparam.intpnt_tol_dfeas,    value)
            self.int.putdouparam(mosek.dparam.intpnt_co_tol_dfeas, value)
            self.int.putdouparam(mosek.dparam.intpnt_qo_tol_dfeas, value)
            if self.ver <= 8:
                self.int.putdouparam(mosek.dparam.intpnt_nl_tol_dfeas, value)

            # Simplex dual feasibility (optimality) tolerance.
            self.int.putdouparam(mosek.dparam.basis_tol_s, value)

        # rel_dual_fsb_tol
        if self.ext.options.rel_dual_fsb_tol is not None:
            # Simplex relative dual feasibility (optimality) tolerance.
            self.int.putdouparam(mosek.dparam.basis_rel_tol_s,
                self.ext.options.rel_dual_fsb_tol)

        # rel_ipm_opt_tol
        if self.ext.options.rel_ipm_opt_tol is not None:
            value = self.ext.options.rel_ipm_opt_tol

            # Interior-point primal feasibility tolerances.
            self.int.putdouparam(mosek.dparam.intpnt_tol_rel_gap,    value)
            self.int.putdouparam(mosek.dparam.intpnt_co_tol_rel_gap, value)
            self.int.putdouparam(mosek.dparam.intpnt_qo_tol_rel_gap, value)
            if self.ver <= 8:
                self.int.putdouparam(mosek.dparam.intpnt_nl_tol_rel_gap, value)

        # abs_bnb_opt_tol
        if self.ext.options.abs_bnb_opt_tol is not None:
            self.int.putdouparam(mosek.dparam.mio_tol_abs_gap,
                self.ext.options.abs_bnb_opt_tol)

        # rel_bnb_opt_tol
        if self.ext.options.rel_bnb_opt_tol is not None:
            self.int.putdouparam(mosek.dparam.mio_tol_rel_gap,
                self.ext.options.rel_bnb_opt_tol)

        # integrality_tol
        if self.ext.options.integrality_tol is not None:
            self.int.putdouparam(mosek.dparam.mio_tol_abs_relax_int,
                self.ext.options.integrality_tol)

        # max_iterations
        if self.ext.options.max_iterations is not None:
            value = self.ext.options.max_iterations
            self.int.putintparam(mosek.iparam.bi_max_iterations,     value)
            self.int.putintparam(mosek.iparam.intpnt_max_iterations, value)
            self.int.putintparam(mosek.iparam.sim_max_iterations,    value)

        _lpm = {
            "interior": (mosek.optimizertype.intpnt if isLP
                else mosek.optimizertype.conic),
            "psimplex": mosek.optimizertype.primal_simplex,
            "dsimplex": mosek.optimizertype.dual_simplex}

        # lp_node_method
        if self.ext.options.lp_node_method is not None:
            value = self.ext.options.lp_node_method
            assert value in _lpm, "Unexpected lp_node_method value."
            self.int.putintparam(mosek.iparam.mio_node_optimizer, _lpm[value])

        # lp_root_method
        if self.ext.options.lp_root_method is not None:
            value = self.ext.options.lp_root_method
            assert value in _lpm, "Unexpected lp_root_method value."
            self.int.putintparam(mosek.iparam.mio_root_optimizer, _lpm[value])

        # timelimit
        if self.ext.options.timelimit is not None:
            value = float(self.ext.options.timelimit)
            self.int.putdouparam(mosek.dparam.optimizer_max_time, value)
            self.int.putdouparam(mosek.dparam.mio_max_time,       value)

        # max_fsb_nodes
        if self.ext.options.max_fsb_nodes is not None:
            self.int.putintparam(mosek.iparam.mio_max_num_solutions,
                self.ext.options.max_fsb_nodes)

        # Handle MOSEK-specific options.
        for key, value in self.ext.options.mosek_params.items():
            try:
                self.int.putparam(key.upper(), str(value))
            except mosek.Error as error:
                self._handle_bad_solver_specific_option(key, value, error)

        # Handle unsupported options.
        # TODO: Handle "hotstart" option (via mio_construct_sol).
        self._handle_unsupported_option("hotstart", "treememory")

        # Attempt to solve the problem.
        with self._header(), self._stopwatch():
            try:
                self.int.optimize()
            except mosek.Error as error:
                if error.errno in (
                        mosek.rescode.err_con_q_not_psd,
                        mosek.rescode.err_con_q_not_nsd,
                        mosek.rescode.err_obj_q_not_psd,
                        mosek.rescode.err_obj_q_not_nsd,
                        mosek.rescode.err_toconic_constr_q_not_psd,
                        mosek.rescode.err_toconic_objective_not_psd):
                    self._handle_continuous_nonconvex_error(error)
                else:
                    raise

        # Set the solution to be retrieved.
        if self.ext.is_continuous():
            if isLP:
                solType = mosek.soltype.bas
            else:
                solType = mosek.soltype.itr
        else:
            solType = mosek.soltype.itg

        # Retrieve primals.
        primals = {}
        if self.ext.options.primals is not False:
            values = [float("nan")]*self.int.getnumvar()
            self.int.getxx(solType, values)

            for picosVar in self.ext.variables.values():
                mosekOffset = self._mosekVarOffset[picosVar]
                primal = values[mosekOffset:mosekOffset + picosVar.dim]

                if float("nan") in primal:
                    primals[picosVar] = None
                else:
                    primals[picosVar] = primal

        # Retrieve duals.
        duals = {}
        if self.ext.options.duals is not False and self.ext.is_continuous():
            minimizing = self.int.getobjsense() == mosek.objsense.minimize

            for constraint in self.ext.constraints.values():
                if isinstance(constraint, DummyConstraint):
                    duals[constraint] = cvxopt.spmatrix(
                        [], [], [], constraint.size)
                    continue

                length = len(constraint)
                dual   = [float("nan")]*length

                if isinstance(constraint, AffineConstraint):
                    offset = self._mosekLinConOffset[constraint]
                    self.int.getyslice(solType, offset, offset + length, dual)
                elif isinstance(constraint, ConvexQuadraticConstraint):
                    # TODO: Implement consistent QCQP dual retrieval for all
                    #       solvers that return such duals.
                    dual = None
                elif isinstance(constraint, SOCConstraint) \
                or isinstance(constraint, RSOCConstraint):
                    mosekVars = self._mosekCone[constraint][1]
                    for localConeIndex in range(length):
                        x = [float("nan")]
                        offset = mosekVars[localConeIndex]
                        self.int.getsnxslice(solType, offset, offset + 1, x)
                        dual[localConeIndex] = x[0]

                    if isinstance(constraint, SOCConstraint):
                        dual = [-du for du in dual]
                    elif isinstance(constraint, RSOCConstraint):
                        dual[0] = -dual[0] / math.sqrt(2.0)
                        dual[1] = -dual[1] / math.sqrt(2.0)
                        dual[2:] = [-du for du in dual[2:]]
                elif isinstance(constraint, LMIConstraint):
                    n = constraint.size[0]
                    barVar, _ = self._mosekLMI[constraint]
                    lowerTriangularDual = [float("nan")]*(n*(n + 1) // 2)
                    self.int.getbarsj(solType, barVar, lowerTriangularDual)
                    for lti, (row, col) in enumerate(self._low_tri_indices(n)):
                        value = lowerTriangularDual[lti]
                        dual[n*row + col] = value
                        if row != col:
                            dual[n*col + row] = value
                else:
                    assert False, "Constraint type not supported."

                if dual is None:
                    pass
                elif float("nan") in dual:
                    dual = None
                else:
                    dual = cvxopt.matrix(dual, constraint.size)

                    if isinstance(constraint, AffineConstraint) \
                    or isinstance(constraint, LMIConstraint):
                        if not constraint.is_increasing():
                            dual = -dual

                    if minimizing:
                        dual = -dual

                duals[constraint] = dual

        # Retrieve objective value.
        value = self.int.getprimalobj(solType)

        # Retrieve solution status.
        primalStatus  = self._solution_status_pic2msk(
            self.int.getsolsta(solType), primalSolution=True)
        dualStatus    = self._solution_status_pic2msk(
            self.int.getsolsta(solType), primalSolution=False)
        problemStatus = self._problem_status_pic2msk(
            self.int.getprosta(solType), not self.ext.is_continuous())

        return self._make_solution(
            value, primals, duals, primalStatus, dualStatus, problemStatus)

    def _solution_status_pic2msk(self, statusCode, primalSolution):
        from mosek import solsta as ss
        dualSolution = not primalSolution

        map = {
            ss.unknown:                 SS_UNKNOWN,
            ss.optimal:                 SS_OPTIMAL,
            ss.prim_feas:
                SS_FEASIBLE   if primalSolution else SS_UNKNOWN,
            ss.dual_feas:
                SS_FEASIBLE   if dualSolution   else SS_UNKNOWN,
            ss.prim_and_dual_feas:      SS_FEASIBLE,
            ss.prim_infeas_cer:
                SS_INFEASIBLE if primalSolution else SS_UNKNOWN,
            ss.dual_infeas_cer:
                SS_INFEASIBLE if dualSolution   else SS_UNKNOWN,
            ss.prim_illposed_cer:       SS_UNKNOWN,
            ss.dual_illposed_cer:       SS_UNKNOWN,
            ss.integer_optimal:         SS_OPTIMAL,
        }

        if self.ver < 9:
            map.update({
                ss.near_optimal:            SS_FEASIBLE,
                ss.near_prim_feas:          SS_UNKNOWN,
                ss.near_dual_feas:          SS_UNKNOWN,
                ss.near_prim_and_dual_feas: SS_UNKNOWN,
                ss.near_prim_infeas_cer:    SS_UNKNOWN,
                ss.near_dual_infeas_cer:    SS_UNKNOWN,
                ss.near_integer_optimal:    SS_FEASIBLE
            })

        try:
            return map[statusCode]
        except KeyError:
            self._warn(
                "The MOSEK solution status code {} is not known to PICOS."
                .format(statusCode))
            return SS_UNKNOWN

    def _problem_status_pic2msk(self, statusCode, integerProblem):
        from mosek import prosta as ps

        map = {
            ps.unknown:                  PS_UNKNOWN,
            ps.prim_and_dual_feas:       PS_FEASIBLE,
            ps.prim_feas:
                PS_FEASIBLE if integerProblem else PS_UNKNOWN,
            ps.dual_feas:                PS_UNKNOWN,
            ps.prim_infeas:              PS_INFEASIBLE,
            ps.dual_infeas:              PS_UNBOUNDED,  # TODO: UNB_OR_INF
            ps.prim_and_dual_infeas:     PS_INFEASIBLE,
            ps.ill_posed:                PS_ILLPOSED,
            ps.prim_infeas_or_unbounded: PS_UNKNOWN  # TODO: UNB_OR_INF
        }

        if self.ver < 9:
            map.update({
                ps.near_prim_and_dual_feas:  PS_UNKNOWN,
                ps.near_prim_feas:           PS_UNKNOWN,
                ps.near_dual_feas:           PS_UNKNOWN
            })

        try:
            return map[statusCode]
        except KeyError:
            self._warn("The MOSEK problem status code {} is not known to PICOS."
                .format(statusCode))
            return PS_UNKNOWN


# --------------------------------------
__all__ = api_end(_API_START, globals())
