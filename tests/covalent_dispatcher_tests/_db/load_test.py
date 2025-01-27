# Copyright 2023 Agnostiq Inc.
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


"""Unit tests for result loading (from database) module."""

from unittest.mock import MagicMock, call

import pytest

from covalent._shared_files.util_classes import Status
from covalent_dispatcher._db.load import (
    _result_from,
    electron_record,
    get_result_object_from_storage,
    sublattice_dispatch_id,
)


def test_result_from(mocker):
    """Test the result from function in the load module."""
    mock_lattice_record = MagicMock()
    load_file_mock = mocker.patch("covalent_dispatcher._db.load.load_file")
    lattice_mock = mocker.patch("covalent_dispatcher._db.load.lattice")
    result_mock = mocker.patch("covalent_dispatcher._db.load.Result")

    result_object = _result_from(mock_lattice_record)

    assert (
        call(
            storage_path=mock_lattice_record.storage_path,
            filename=mock_lattice_record.function_filename,
        )
        in load_file_mock.mock_calls
    )
    assert (
        call(
            storage_path=mock_lattice_record.storage_path,
            filename=mock_lattice_record.function_string_filename,
        )
        in load_file_mock.mock_calls
    )
    assert (
        call(
            storage_path=mock_lattice_record.storage_path,
            filename=mock_lattice_record.docstring_filename,
        )
        in load_file_mock.mock_calls
    )
    assert (
        call(
            storage_path=mock_lattice_record.storage_path,
            filename=mock_lattice_record.executor_data_filename,
        )
        in load_file_mock.mock_calls
    )
    assert (
        call(
            storage_path=mock_lattice_record.storage_path,
            filename=mock_lattice_record.workflow_executor_data_filename,
        )
        in load_file_mock.mock_calls
    )
    assert (
        call(
            storage_path=mock_lattice_record.storage_path,
            filename=mock_lattice_record.inputs_filename,
        )
        in load_file_mock.mock_calls
    )
    assert (
        call(
            storage_path=mock_lattice_record.storage_path,
            filename=mock_lattice_record.named_args_filename,
        )
        in load_file_mock.mock_calls
    )
    assert (
        call(
            storage_path=mock_lattice_record.storage_path,
            filename=mock_lattice_record.named_kwargs_filename,
        )
        in load_file_mock.mock_calls
    )
    assert (
        call(
            storage_path=mock_lattice_record.storage_path,
            filename=mock_lattice_record.error_filename,
        )
        in load_file_mock.mock_calls
    )
    assert (
        call(
            storage_path=mock_lattice_record.storage_path,
            filename=mock_lattice_record.transport_graph_filename,
        )
        in load_file_mock.mock_calls
    )
    assert (
        call(
            storage_path=mock_lattice_record.storage_path,
            filename=mock_lattice_record.results_filename,
        )
        in load_file_mock.mock_calls
    )
    assert (
        call(
            storage_path=mock_lattice_record.storage_path,
            filename=mock_lattice_record.deps_filename,
        )
        in load_file_mock.mock_calls
    )
    assert (
        call(
            storage_path=mock_lattice_record.storage_path,
            filename=mock_lattice_record.call_before_filename,
        )
        in load_file_mock.mock_calls
    )
    assert (
        call(
            storage_path=mock_lattice_record.storage_path,
            filename=mock_lattice_record.call_after_filename,
        )
        in load_file_mock.mock_calls
    )
    assert (
        call(
            storage_path=mock_lattice_record.storage_path,
            filename=mock_lattice_record.cova_imports_filename,
        )
        in load_file_mock.mock_calls
    )
    assert (
        call(
            storage_path=mock_lattice_record.storage_path,
            filename=mock_lattice_record.lattice_imports_filename,
        )
        in load_file_mock.mock_calls
    )

    lattice_mock.assert_called_once()
    result_mock.assert_called_once()

    assert result_object._root_dispatch_id == mock_lattice_record.root_dispatch_id
    assert result_object._status == Status(mock_lattice_record.status)
    assert result_object._error == load_file_mock.return_value
    assert result_object._inputs == load_file_mock.return_value
    assert result_object._start_time == mock_lattice_record.started_at
    assert result_object._end_time == mock_lattice_record.completed_at
    assert result_object._result == load_file_mock.return_value
    assert result_object._num_nodes == mock_lattice_record.electron_num

    lattice_mock_attrs = lattice_mock().__dict__
    assert set(lattice_mock_attrs.keys()) == {
        "workflow_function",
        "workflow_function_string",
        "__name__",
        "__doc__",
        "metadata",
        "args",
        "kwargs",
        "named_args",
        "named_kwargs",
        "transport_graph",
        "cova_imports",
        "lattice_imports",
        "post_processing",
        "electron_outputs",
        "_bound_electrons",
    }
    assert lattice_mock_attrs["post_processing"] is False
    assert lattice_mock_attrs["electron_outputs"] == {}
    assert lattice_mock_attrs["_bound_electrons"] == {}

    _, args, _ = lattice_mock.mock_calls[0]
    assert args[0].__name__ == "dummy_function"


def test_get_result_object_from_storage(mocker):
    """Test the get_result_object_from_storage method."""
    from covalent_dispatcher._db.load import Lattice

    result_from_mock = mocker.patch("covalent_dispatcher._db.load._result_from")

    workflow_db_mock = mocker.patch("covalent_dispatcher._db.load.workflow_db")
    session_mock = workflow_db_mock.session.return_value.__enter__.return_value

    result_object = get_result_object_from_storage("mock-dispatch-id")

    assert call(Lattice) in session_mock.query.mock_calls
    session_mock.query().where().first.assert_called_once()

    assert result_object == result_from_mock.return_value
    result_from_mock.assert_called_once_with(session_mock.query().where().first.return_value)


def test_get_result_object_from_storage_exception(mocker):
    """Test the get_result_object_from_storage method."""
    from covalent_dispatcher._db.load import Lattice

    result_from_mock = mocker.patch("covalent_dispatcher._db.load._result_from")

    workflow_db_mock = mocker.patch("covalent_dispatcher._db.load.workflow_db")
    session_mock = workflow_db_mock.session.return_value.__enter__.return_value
    session_mock.query().where().first.return_value = None

    with pytest.raises(RuntimeError):
        get_result_object_from_storage("mock-dispatch-id")

    assert call(Lattice) in session_mock.query.mock_calls
    session_mock.query().where().first.assert_called_once()

    result_from_mock.assert_not_called()


def test_electron_record(mocker):
    """Test the electron_record method."""

    workflow_db_mock = mocker.patch("covalent_dispatcher._db.load.workflow_db")
    session_mock = workflow_db_mock.session.return_value.__enter__.return_value

    electron_record("mock-dispatch-id", "mock-node-id")
    session_mock.query().filter().filter().filter().first.assert_called_once()


def test_sublattice_dispatch_id(mocker):
    """Test the sublattice_dispatch_id method."""

    class MockObject:
        dispatch_id = "mock-dispatch-id"

    workflow_db_mock = mocker.patch("covalent_dispatcher._db.load.workflow_db")
    session_mock = workflow_db_mock.session.return_value.__enter__.return_value

    session_mock.query().filter().first.return_value = MockObject()
    res = sublattice_dispatch_id("mock-electron-id")
    assert res == "mock-dispatch-id"

    session_mock.query().filter().first.return_value = []
    res = sublattice_dispatch_id("mock-electron-id")
    assert res is None
