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

# pylint: disable=no-member

import pennylane as qml
import pytest
from numpy import isclose

import covalent as ct

EXECUTORS = [
    ct.executor.QiskitExecutor(device="local_sampler", shots=10_000),
    ct.executor.Simulator(),
]


@pytest.mark.parametrize("executor", EXECUTORS)
def test_qaoa(executor):
    """
    Test that `run_later` produces the same result as the normal call.
    """
    from networkx import Graph
    from pennylane import qaoa

    wires = range(10)
    graph = Graph([(0, 1), (1, 2), (2, 0)])
    cost_h, mixer_h = qaoa.maxcut(graph)

    def qaoa_layer(gamma, alpha):
        qaoa.cost_layer(gamma, cost_h)
        qaoa.mixer_layer(alpha, mixer_h)

    @ct.qelectron(executors=executor)
    @qml.qnode(qml.device("lightning.qubit", wires=len(wires)))
    def circuit(params):
        for w in wires:
            qml.Hadamard(wires=w)
        qml.layer(qaoa_layer, 2, params[0], params[1])
        return qml.expval(cost_h)

    inputs = [[1, 1.0], [1.2, 1]]
    output_1 = circuit(inputs.copy())
    output_2 = circuit.run_later(inputs.copy()).result()

    assert isclose(output_1, output_2, rtol=0.1), "Call and run later results are different"


@pytest.mark.parametrize("executor", EXECUTORS)
def test_multi_return_async(executor):
    """
    Test that `run_later` produces the same result as the normal call.
    """

    @qml.qnode(qml.device("default.qubit", wires=2, shots=4096))
    def circuit(theta):
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.RY(theta, wires=0)

        return [
            qml.expval(qml.PauliZ(0) @ qml.PauliZ(1)),
            qml.expval(qml.PauliZ(0) @ qml.PauliX(1)),
            qml.expval(qml.PauliX(0) @ qml.PauliZ(1)),
            qml.expval(qml.PauliX(0) @ qml.PauliX(1)),
        ]

    qe_circuit = ct.qelectron(circuit, executors=executor)

    thetas = [0.1, 0.9]

    output_1 = [circuit(theta) for theta in thetas]

    futures = [qe_circuit.run_later(theta) for theta in thetas]
    output_2 = [future.result() for future in futures]

    msg = "Call and run later results are different"
    for o1, o2 in zip(output_1, output_2):
        assert isclose(o1, o2, atol=0.1).all(), msg
