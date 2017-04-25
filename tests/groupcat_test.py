"""Tests for the `illustris_python` module.

Running Tests
-------------
To run all tests, this script can be executed as:
    `$ python tests/test.py [-v] [--nocapture]`
from the root directory.

Alternatively, `nosetests` can be run and it will find the tests:
    `$ nosetests [-v] [--nocapture]`

To run particular tests (for example),
    `$ nosetests tests/test.py:test_groupcat_loadSubhalos`

"""

import os

from nose.tools import assert_true, assert_equal, assert_raises
import numpy as np

# `illustris_python` is imported as `ill` in local `__init__.py`
from . import ill, BASE_PATH_ILLUSTRIS_1


# =========================
# ====    loadHalos    ====
# =========================


def test_groupcat_loadHalos():
    fields = ['GroupFirstSub']
    snap = 135
    group_first_sub = ill.groupcat.loadHalos(BASE_PATH_ILLUSTRIS_1, snap, fields=fields)
    print("group_first_sub.shape = ", group_first_sub.shape)
    assert_equal(group_first_sub.shape, (7713601,))
    print("group_first_sub = ", group_first_sub)
    assert_true(np.all(group_first_sub[:3] == [0, 16937, 30430]))

    return


def test_groupcat_loadHalos_1():
    fields = ['GroupFirstSub']
    snap = 135
    # Construct a path that should not be found: fail
    fail_path = os.path.join(BASE_PATH_ILLUSTRIS_1, 'failure')
    print("path '{}' should not be found".format(fail_path))
    assert_raises(OSError, ill.groupcat.loadHalos, fail_path, snap, fields=fields)
    return


def test_groupcat_loadHalos_2():
    fields = ['GroupFirstSub']
    snap = 136
    # Construct a path that should not be found: fail
    print("snap '{}' should not be found".format(snap))
    assert_raises(OSError, ill.groupcat.loadHalos, BASE_PATH_ILLUSTRIS_1, snap, fields=fields)
    return


def test_groupcat_loadHalos_3():
    # This field should not be found
    fields = ['GroupFailSub']
    snap = 100
    # Construct a path that should not be found: fail
    print("fields '{}' should not be found".format(fields))
    assert_raises(Exception, ill.groupcat.loadHalos, BASE_PATH_ILLUSTRIS_1, snap, fields=fields)
    return


# ==========================
# ====    loadSingle    ====
# ==========================


def test_groupcat_loadSingle():
    # Gas fractions for the first 5 subhalos
    gas_frac = [0.0344649, 0.00273708, 0.0223776, 0.0256707, 0.0134044]

    ptNumGas = ill.snapshot.partTypeNum('gas')  # 0
    ptNumStars = ill.snapshot.partTypeNum('stars')  # 4
    for i in range(5):
        # all_fields = ill.groupcat.loadSingle(BASE_PATH_ILLUSTRIS_1, 135, subhaloID=group_first_sub[i])
        all_fields = ill.groupcat.loadSingle(BASE_PATH_ILLUSTRIS_1, 135, subhaloID=i)
        gas_mass   = all_fields['SubhaloMassInHalfRadType'][ptNumGas]
        stars_mass = all_fields['SubhaloMassInHalfRadType'][ptNumStars]
        frac = gas_mass / (gas_mass + stars_mass)
        # print(i, group_first_sub[i], frac)
        print("subhalo {} with gas frac '{}' (should be '{}')".format(i, frac, gas_frac[i]))
        assert_true(np.isclose(frac, gas_frac[i]))

    return


# ============================
# ====    loadSubhalos    ====
# ============================


def test_groupcat_loadSubhalos():
    fields = ['SubhaloMass', 'SubhaloSFRinRad']
    snap = 135
    subhalos = ill.groupcat.loadSubhalos(BASE_PATH_ILLUSTRIS_1, snap, fields=fields)
    print("subhalos['SubhaloMass'] = ", subhalos['SubhaloMass'].shape)
    assert_true(subhalos['SubhaloMass'].shape == (4366546,))
    print("subhalos['SubhaloMass'] = ", subhalos['SubhaloMass'])
    assert_true(
        np.allclose(subhalos['SubhaloMass'][:3], [2.21748203e+04, 2.21866333e+03, 5.73408325e+02]))

    return