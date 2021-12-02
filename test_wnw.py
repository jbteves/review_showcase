"""Tests for wnw"""

import os.path as op

import pytest

from wnw import WnwProject, WNW_DEFAULT_ROOT


# Failure tests
def test_init_fails_nonstr():
    with pytest.raises(TypeError):
        _ = WnwProject(1)


def test_path_to_fails_types():
    p = WnwProject()

    with pytest.raises(TypeError):
        _ = p.path_to(subject="1")

    with pytest.raises(TypeError):
        _ = p.path_to(subject=1, modality=1)

    with pytest.raises(TypeError):
        _ = p.path_to(subject=1, modality="func", run="01", acquisition="a", echo=1)

    with pytest.raises(TypeError):
        _ = p.path_to(subject=1, modality="func", run=1, acquisition=2, echo=1)

    with pytest.raises(TypeError):
        _ = p.path_to(subject=1, modality="func", run=1, acquisition="a", echo="c")


def test_path_to_fails_values():
    p = WnwProject()

    # raw value errors
    with pytest.raises(ValueError):
        _ = p.path_to(5)

    with pytest.raises(ValueError):
        _ = p.path_to(subject=1, modality="eeg")

    with pytest.raises(ValueError):
        _ = p.path_to(subject=1, modality="func", run=3)

    with pytest.raises(ValueError):
        _ = p.path_to(subject=1, modality="func", run=1, acquisition="d")

    with pytest.raises(ValueError):
        _ = p.path_to(subject=1, modality="func", run=1, acquisition="a", echo=4)

    # incompatible argument specificities
    with pytest.raises(ValueError):
        # anatomical modality but more specificity asked for
        _ = p.path_to(subject=1, modality="anat", run=1)

    with pytest.raises(ValueError):
        # missing echo
        _ = p.path_to(subject=1, modality="func", acquisition="b")


def test_path_to_works():
    p = WnwProject()

    expected = op.join(WNW_DEFAULT_ROOT, "sub-01", "anat")
    assert expected == p.path_to(subject=1, modality="anat")

    expected = op.join(WNW_DEFAULT_ROOT, "sub-01", "func")
    assert expected == p.path_to(subject=1, modality="func")

    expected = op.join(WNW_DEFAULT_ROOT, "sub-01", "anat", f"sub-01_T1w.nii")
    assert expected == p.path_to(subject=1, modality="T1w")

    expected_fname = "sub-01_task-wnw_acq-a_run-1_echo-1_bold.nii"
    expected = op.join(
        WNW_DEFAULT_ROOT, "sub-01", "func", expected_fname
    )
    result = p.path_to(
        subject=1, modality="func", acquisition="a", run=1, echo=1
    )
    assert expected == result
