# Copyright 2023 Agnostiq Inc.

"""Module for Covalent Cloud dispatching and related functionalities."""


import lzma
from copy import deepcopy
from functools import wraps
from typing import Any, Callable

from covalent._results_manager.result import Result
from covalent._workflow.lattice import Lattice
from covalent._workflow.transport import TransportableObject

from covalent_cloud.shared.classes.exceptions import CovalentAPIKeyError

from ..shared.classes.settings import Settings, settings
from . import results_manager as rm
from .helpers import register, start, validate_executors

API_KEY = "fake"  # pragma: allowlist secret


def _compressed_transportable(data: Any) -> bytes:
    """Applies LZMA compression to a transportable object serialized into bytes."""
    return lzma.compress(TransportableObject(data).serialize())


def dispatch(
    orig_lattice: Lattice,
    settings: Settings = settings,
) -> Callable:
    """
    Dispatches a Covalent workflow to the Covalent Cloud and returns the assigned dispatch ID.
    The dispatch function takes a Covalent workflow, also called a lattice, and sends it to the Covalent Cloud Server for execution. Once dispatched, the workflow runs on a the cloud and can be monitored using the dispatch ID in the application. The dispatch function returns a wrapper function that takes the inputs of the workflow as arguments. This wrapper function can be called to execute the workflow.

    Args:
        orig_lattice: The Covalent workflow to send to the cloud.
        settings: The settings object to use. If None, the default settings will be used.

    Returns:
        A wrapper function which takes the inputs of the workflow as arguments.

    Examples:

        # define a simple lattice
        import covalent_cloud as ctc
        import covalent as ct
        
        @ct.lattice
        def my_lattice(a: int, b: int) -> int:
            return a + b

        # dispatch the lattice and get the assigned dispatch ID
        dispatch_id = ctc.dispatch(my_lattice)(2, 3)
    """

    dispatcher_addr = settings.dispatcher_uri

    @wraps(orig_lattice)
    def wrapper(*args, **kwargs) -> str:
        """
        Send the lattice to the dispatcher server and return
        the assigned dispatch id.

        Args:
            *args: The inputs of the workflow.
            **kwargs: The keyword arguments of the workflow.

        Returns:
            The dispatch id of the workflow.

        """

        try:
            lattice = deepcopy(orig_lattice)
            lattice.build_graph(*args, **kwargs)

            # Check that only CloudExecutors are specified.
            if settings.validate_executors and not validate_executors(lattice):
                raise ValueError("One or more electrons have invalid executors.")

            dispatch_id = register(lattice, settings)(*args, **kwargs)
            return start(dispatch_id)

        except CovalentAPIKeyError as e:
            e.rich_print(level="error")

    return wrapper


def get_result(
    dispatch_id: str,
    wait: bool = False,
    settings: Settings = settings,
    *,
    status_only: bool = False,
) -> Result:
    """
    Gets the result of a Covalent workflow that has been dispatched to the cloud.

    This function retrieves the result of a dispatched Covalent workflow that has been executed on the cloud. The function takes the dispatch ID of the workflow and retrieves the results from the cloud. The result is returned as a `Result` object that contains the status of the workflow, the final result of the lattice, and any error messages that may have occurred during execution.

    Args:
        dispatch_id: The dispatch ID assigned to the workflow.
        wait: Controls how long the function waits for the server to return a result. If False, the function will not wait and will return the current status of the workflow. If True, the function will wait for the result to finish and keep retrying until the result is available.
        status_only: If True, only retrieves the status of the workflow and not the full result.
        settings: The Covalent settings to use for the request.

    Returns:
        A `Result` object that contains the status of the workflow, the final result of the lattice, and any error messages that may have occurred during execution.

    Examples:

    # define a simple lattice
    import covalent_cloud as ctc
    import covalent as ct
    
    @ct.lattice
    def my_lattice(a: int, b: int) -> int:
        return a + b

    # dispatch the lattice and get the assigned dispatch ID
    dispatch_id = ctc.dispatch(my_lattice)(2, 3)

    # get the result of the dispatched lattice
    result = ctc.get_result(dispatch_id, wait=True)

    # print the final result of the lattice
    print(result.result)
    """

    return rm.get_result(
        dispatch_id=dispatch_id,
        wait=wait,
        settings=settings,
        status_only=status_only,
    )
