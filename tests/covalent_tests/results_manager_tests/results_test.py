# Copyright 2021 Agnostiq Inc.
#
# This file is part of Covalent.
#
# Licensed under the Apache License 2.0 (the "License"). A copy of the
# License may be obtained with this software package or at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Use of this file is prohibited except in compliance with the License.
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unit tests for the Result object."""

import os
from pathlib import Path

import pytest

import covalent as ct
from covalent._results_manager.result import Result
from covalent._workflow.lattice import Lattice as LatticeClass
from covalent.executor import LocalExecutor

# TEMP_RESULTS_DIR = "/tmp/results"
TEMP_RESULTS_DIR = os.environ.get("COVALENT_DATA_DIR") or os.path.join(
    os.environ["HOME"], ".local/share/covalent/data"
)


def get_mock_result() -> Result:
    """Construct a mock result object corresponding to a lattice."""

    import sys

    @ct.electron(executor="local")
    def task(x):
        print(f"stdout: {x}")
        print("Error!", file=sys.stderr)
        return x

    @ct.lattice
    def pipeline(x):
        res1 = task(x)
        res2 = task(res1)
        return res2

    pipeline.build_graph(x="absolute")
    received_workflow = LatticeClass.deserialize_from_json(pipeline.serialize_to_json())
    result_object = Result(
        received_workflow,
        "pipeline_workflow",  # pipeline.metadata["results_dir"], "pipeline_workflow"
    )

    return result_object


le = LocalExecutor(log_stdout="/tmp/stdout.log")


@pytest.fixture
def result_1():
    @ct.electron(executor="dask")
    def task_1(x, y):
        return x * y

    @ct.electron(executor=le)
    def task_2(x, y):
        return x + y

    @ct.lattice(executor=le, workflow_executor=le)
    def workflow_1(a, b):
        """Docstring"""
        res_1 = task_1(a, b)
        return task_2(res_1, b)

    Path(f"{TEMP_RESULTS_DIR}/dispatch_1").mkdir(parents=True, exist_ok=True)
    workflow_1.build_graph(a=1, b=2)
    received_lattice = LatticeClass.deserialize_from_json(workflow_1.serialize_to_json())
    result = Result(lattice=received_lattice, dispatch_id="dispatch_1")
    #    result.lattice.metadata["results_dir"] = TEMP_RESULTS_DIR
    result._initialize_nodes()
    return result


@pytest.fixture
def result_2():
    @ct.electron(executor=le)
    def task_1(x, y):
        raise RuntimeError("error")

    @ct.lattice(executor=le, workflow_executor=le)
    def workflow_1(a, b):
        """Docstring"""
        res_1 = task_1(a, b)
        return res_1

    Path(f"{TEMP_RESULTS_DIR}/dispatch_1").mkdir(parents=True, exist_ok=True)
    workflow_1.build_graph(a=1, b=2)
    received_lattice = LatticeClass.deserialize_from_json(workflow_1.serialize_to_json())
    result = Result(lattice=received_lattice, dispatch_id="dispatch_1")
    #    result.lattice.metadata["results_dir"] = TEMP_RESULTS_DIR
    result._initialize_nodes()
    return result


def test_get_node_error(result_1):
    """Test result method to get the node error."""
    assert not result_1._get_node_error(node_id=0)


def test_get_all_node_results(result_1, mocker):
    """Test result method to get all the node results."""

    for data_row in result_1.get_all_node_results():
        if data_row["node_id"] == 0:
            assert data_row["node_name"] == "task_1"
        elif data_row["node_id"] == 1:
            assert data_row["node_name"] == ":parameter:1"


def test_get_failed_nodes(result_1, mocker):
    """Test result method to get all failed nodes"""
    result_1.lattice.transport_graph.set_node_value(0, "status", Result.FAILED)
    result_1.lattice.transport_graph.set_node_value(1, "status", Result.COMPLETED)
    result_1.lattice.transport_graph.set_node_value(2, "status", Result.COMPLETED)
    assert result_1._get_failed_nodes() == [(0, "task_1")]


def test_str_result(result_2, mocker):
    """Test result __str__ method"""
    s = str(result_2)
    assert "task_1" in s


def test_result_status_comparison(result_2, mocker):
    """Test result.status __eq__ and __ne__ methods"""
    assert result_2.status == "NEW_OBJECT"
    assert result_2.status == Result.NEW_OBJ
    assert result_2.status != "COMPLETED"
    assert result_2.status != Result.COMPLETED


def test_result_root_dispatch_id(result_1):
    """Test the `root_dispatch_id` property`"""

    assert result_1.root_dispatch_id == result_1._root_dispatch_id


def test_result_post_process(
    mocker,
):
    """Test client-side post-processing of results."""

    import covalent as ct

    @ct.electron
    def construct_cu_slab(x):
        return x

    @ct.electron
    def compute_system_energy(x):
        return x

    @ct.electron
    def construct_n_molecule(x):
        return x

    @ct.electron
    def get_relaxed_slab(x):
        return x

    @ct.lattice
    def compute_energy(n):
        N2 = construct_n_molecule(1)
        e_N2 = compute_system_energy(N2)

        slab = construct_cu_slab(2)
        e_slab = compute_system_energy(slab)

        relaxed_slab = get_relaxed_slab(3)
        e_relaxed_slab = compute_system_energy(relaxed_slab)
        for i in range(n):
            pass

        return (N2, e_N2, slab, e_slab, relaxed_slab, e_relaxed_slab)

    compute_energy.build_graph(3)

    compute_energy = LatticeClass.deserialize_from_json(compute_energy.serialize_to_json())

    node_outputs = {
        "construct_n_molecule(0)": 1,
        ":parameter:1(1)": 1,
        "compute_system_energy(2)": 1,
        "construct_cu_slab(3)": 2,
        ":parameter:2(4)": 2,
        "compute_system_energy(5)": 2,
        "get_relaxed_slab(6)": 3,
        ":parameter:3(7)": 3,
        "compute_system_energy(8)": 3,
    }

    encoded_node_outputs = {
        k: ct.TransportableObject.make_transportable(v) for k, v in node_outputs.items()
    }

    res = Result(compute_energy)
    res._initialize_nodes()

    for i, v in enumerate(encoded_node_outputs.values()):
        compute_energy.transport_graph.set_node_value(i, "output", v)

    res._status = Result.PENDING_POSTPROCESSING
    res._dispatch_id = "MOCK"
    res._root_dispatch_id = "MOCK"

    execution_result = res.post_process()

    assert execution_result == compute_energy(3)


def test_update_node(result_1, mocker):
    result_1._update_node(node_id=0, status=Result.COMPLETED, sub_dispatch_id="subdispatch")

    tg = result_1.lattice.transport_graph
    assert tg.get_node_value(0, "sub_dispatch_id") == "subdispatch"
    assert tg.get_node_value(0, "status") == Result.COMPLETED
