"""Utilities for the word-nonword study"""

import os.path as op


WNW_DEFAULT_ROOT = "/data/NIMH_SFIM/handwerkerd/DenoisingPilot"
WNW_SUBJECTS = [1, 3, 4]
WNW_MODALITIES = ["func", "anat", "T1w"]
WNW_RUNS = [1, 2]
WNW_ACQUISITIONS = ["a", "b", "c"]

WNW_ECHOES = {
    "a": [1, 2, 3],
    "b": [1, 2, 3, 4, 5],
    "c": [1, 2, 3],
}


class WnwProject:
    """An object to represent the underlying word-nonword data structure

    Attributes
    ----------
    _root: str
        The root directory for the project

    Methods
    -------
    path_to

    Examples
    --------
    >>> p = WnwProject()
    >>> p.path_to(subject=1, modality="func")
    '/data/tevesjb/wnw_project/sub-01/func'
    """
    def __init__(self, root: str = WNW_DEFAULT_ROOT):
        if not isinstance(root, str):
            raise TypeError(f"root should be str, is {type(root)}")
        self._root = root
    
    def path_to(
        self,
        subject: int = None,
        modality: str = 'func',
        run: int = None,
        acquisition: str = None,
        echo: int = None,
    ) -> str:
        """Generate the path to a raw data directory or file

        Parameters
        ----------
        subject: int
            The subject ID
        modality: str
            The modality
        run: int
            The run number
        acquisition: str
            The acquisition type
        echo: int
            The echo number

        Returns
        -------
        str: the path to the directory or file of interest

        Raises
        ------
        TypeError, if types are not adhered to.
        ValueError, if there are incompatible values in the call (for
        example, requesting modality=anat and acquisition="a") OR if the
        user requests a value which doesn't exist (for example, run=3).
        """
        _validate_path_to(subject, modality, run, acquisition, echo)
        sub = f"{subject:02}"
        path = op.join(self._root, f"sub-{sub}")
        if modality:
            if modality == "func":
                path = op.join(path, "func")
            else:
                if modality == "anat":
                    path = op.join(path, "anat")
                elif modality == "T1w":
                    path = op.join(
                        path, "anat", f"sub-{sub}_T1w.nii"
                    )
        # from here, everything is functional and all parameters are used
        if run is not None:
            fname = (
                f"sub-{sub}_task-wnw_acq-{acquisition}_"
                f"run-{run}_echo-{echo}_bold.nii"
            )
            path = op.join(path, fname)

        return path
    

def _validate_path_to(
    subject, modality, run, acquisition, echo
) -> None:
    _validate_param(
        "subject", subject, int, allowed_values=WNW_SUBJECTS,
        required=True,
    )
    _validate_param(
        "modality", modality, str, allowed_values=WNW_MODALITIES
    )

    if modality != "func":
        if (run is not None) or (acquisition is not None) or (echo is
            not None):
            raise ValueError(
                "Too much specifity in arguments for modality"
                f"{modality}"
            )


    # If any of run, acquisition, or echo, exist, all must exist in order
    # to specify a unique file
    if (run is not None) or (acquisition is not None) or (echo is not None):
        _validate_param(
            "run", run, int,
            allowed_values=WNW_RUNS, required=True
        )
        _validate_param(
            "acquisition", acquisition, str,
            allowed_values=WNW_ACQUISITIONS, required=True
        )
        _validate_param(
            "echo", echo, int,
            allowed_values=WNW_ECHOES[acquisition], required=True
        )


def _validate_param(
    label, param, type_expected, allowed_values=None, required=False
) -> None:
    """Validate a parameter

    Parameters
    ----------
    label: str
        the name of the parameter 
    param: object
        The parameter itself
    type_expected: type
        The parameter type
    allowed_values: list, optional
        The list of allowed values for the parameter. If None, all are
        allowed. Defalt None.
    required: bool
        Whether this object is required (if False, "None" is allowed, else
        it must match the type). Default False.
    """
    if required and param is None:
        raise ValueError(
            f"{label} is required in this context."
        )
    if not isinstance(param, type_expected):
        raise TypeError(
            f"{label} should be type {type_expected}, is {type(param)}"
        )
    if allowed_values is not None:
        if not param in allowed_values:
            allowed = str(allowed_values)
            raise ValueError(
                f"{label} {param} does not exist; "
                f"existing values are: {' '.join(allowed)}"
            )
