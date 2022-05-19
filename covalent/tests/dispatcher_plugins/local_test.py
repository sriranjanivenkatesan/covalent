# Copyright 2021 Agnostiq Inc.
#
# This file is part of Covalent.
#
# Licensed under the GNU Affero General Public License 3.0 (the "License").
# A copy of the License may be obtained with this software package or at
#
#      https://www.gnu.org/licenses/agpl-3.0.en.html
#
# Use of this file is prohibited except in compliance with the License. Any
# modifications or derivative works of this file must retain this copyright
# notice, and modified files must contain a notice indicating that they have
# been altered from the originals.
#
# Covalent is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the License for more details.
#
# Relief from the License may be granted by purchasing a commercial license.
import pytest

import covalent as ct


@ct.electron
def add(a, b):
    return a + b


@ct.lattice
def workflow(x, y):
    res = add(x, y)
    return add(res, y)


@pytest.mark.skip(
    reason="NATS replaced with Amazon SQS as a result microservices is not functional locally."
)
def test_local_dispatcher_dispatch():
    """Tests whether the local dispatcher can dispatch a workflow successfully."""

    dispatch_id = ct.dispatch(workflow)(1, 2)

    assert isinstance(dispatch_id, str)


@pytest.mark.skip(reason="synchronous dispatch freezes the shell and needs to be updated")
def test_local_dispatcher_dispatch_sync():
    """Tests whether the local dispatcher can synchronously dispatch a workflow successfully."""

    result = ct.dispatch_sync(workflow)(1, 2)
    assert result.result == 5
