"""
Global test fixtures
"""
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from random import randint
from typing import Dict
from typing import List
from typing import Tuple

import pytest
from astropy.io import fits
from dkist_data_simulator.dataset import key_function
from dkist_data_simulator.spec122 import Spec122Dataset

from dkist_processing_common._util.constants import Constants
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common._util.tags import TagDB
from dkist_processing_common.parsers.l0_fits_access import L0FitsAccess


@pytest.fixture()
def recipe_run_id():
    return randint(0, 99999)


@pytest.fixture()
def tag_db(recipe_run_id) -> TagDB:
    t = TagDB(recipe_run_id=recipe_run_id, task_name="test_tags")
    yield t
    t.purge()
    t.close()


@pytest.fixture()
def tag_db2(recipe_run_id) -> TagDB:
    """
    Another instance of a tag db in the same redis db
    """
    recipe_run_id = recipe_run_id + 15  # same db number but different namespace
    t = TagDB(recipe_run_id=recipe_run_id, task_name="test_tags2")
    yield t
    t.purge()
    t.close()


@pytest.fixture(params=[None, "use_tmp_path"])
def workflow_file_system(request, recipe_run_id, tmp_path) -> Tuple[WorkflowFileSystem, int, Path]:
    if request.param == "use_tmp_path":
        path = tmp_path
    else:
        path = request.param
    wkflow_fs = WorkflowFileSystem(
        recipe_run_id=recipe_run_id,
        task_name="wkflow_fs_test",
        scratch_base_path=path,
    )
    yield wkflow_fs, recipe_run_id, tmp_path
    wkflow_fs.purge(ignore_errors=True)
    tmp_path.rmdir()
    wkflow_fs.close()


@pytest.fixture()
def constants(recipe_run_id) -> Constants:
    constants = Constants(recipe_run_id=recipe_run_id, task_name="test_constants")
    yield constants
    constants.purge()
    constants.close()


@pytest.fixture()
def complete_common_header():
    """
    A header with some common by-frame keywords and a single instrument specific one
    """
    hdu = fits.PrimaryHDU()
    hdu.header["TELEVATN"] = 6.28
    hdu.header["TAZIMUTH"] = 3.14
    hdu.header["TTBLANGL"] = 1.23
    hdu.header["DATE-OBS"] = "1988-05-25T01:23:45.678"
    hdu.header["INST_FOO"] = "bar"
    hdu.header["DKIST004"] = "ip task type"
    hdu.header["ID___004"] = "ip id"
    hdu.header["PAC__004"] = "polarizer"
    hdu.header["PAC__005"] = 31.2
    hdu.header["PAC__006"] = "retarder"
    hdu.header["PAC__007"] = 6.66
    hdu.header["PAC__008"] = "dark shutter"
    hdu.header["INSTRUME"] = "VBI"
    hdu.header["ID___013"] = "PROPOSAL_ID1"

    return hdu.header


class CalibrationSequenceDataset(Spec122Dataset):
    def __init__(
        self,
        array_shape: Tuple[int, ...],
        time_delta: float,
        instrument="visp",
    ):
        self.num_frames_per_CS_step = 5

        # Make up a Calibration sequence. Mostly random except for two clears and two darks at start and end, which
        # we want to test
        self.pol_status = [
            "clear",
            "clear",
            "test polarizer",
            "test polarizer",
            "test polarizer",
            "clear",
            "clear",
        ]
        self.pol_theta = [0.0, 0.0, 60.0, 60.0, 120.0, 0.0, 0.0]
        self.ret_status = ["clear", "clear", "clear", "test retarder", "clear", "clear", "clear"]
        self.ret_theta = [0.0, 0.0, 0.0, 45.0, 0.0, 0.0, 0.0]
        self.dark_status = [
            "DarkShutter",
            "FieldStop",
            "FieldStop",
            "FieldStop",
            "FieldStop",
            "FieldStop",
            "DarkShutter",
        ]

        self.num_steps = len(self.pol_theta)
        dataset_shape = (self.num_steps * self.num_frames_per_CS_step,) + array_shape[1:]
        super().__init__(dataset_shape, array_shape, time_delta, instrument=instrument)
        self.add_constant_key("DKIST004", "PolCal")

    @property
    def cs_step(self) -> int:
        return self.index // self.num_frames_per_CS_step

    @key_function("PAC__004")
    def polarizer_status(self, key: str) -> str:
        return self.pol_status[self.cs_step]

    @key_function("PAC__005")
    def polarizer_angle(self, key: str) -> float:
        return self.pol_theta[self.cs_step]

    @key_function("PAC__006")
    def retarter_status(self, key: str) -> str:
        return self.ret_status[self.cs_step]

    @key_function("PAC__007")
    def retarder_angle(self, key: str) -> float:
        return self.ret_theta[self.cs_step]

    @key_function("PAC__008")
    def gos_level3_status(self, key: str) -> str:
        return self.dark_status[self.cs_step]


class NonPolCalDataset(Spec122Dataset):
    def __init__(self):
        super().__init__(
            dataset_shape=(4, 2, 2), array_shape=(1, 2, 2), time_delta=1, instrument="visp"
        )  # Instrument doesn't matter
        self.add_constant_key("DKIST004", "Dark")  # Anything that's not PolCal


@pytest.fixture(scope="session")
def grouped_cal_sequence_headers() -> Dict[int, List[L0FitsAccess]]:
    ds = CalibrationSequenceDataset(array_shape=(1, 2, 2), time_delta=2.0)
    header_list = [d.header() for d in ds]
    expected_cs_dict = defaultdict(list)
    for i in range(ds.num_steps):
        for j in range(ds.num_frames_per_CS_step):
            expected_cs_dict[i].append(L0FitsAccess.from_header(header_list.pop(0)))

    return expected_cs_dict


@pytest.fixture(scope="session")
def non_polcal_headers() -> List[L0FitsAccess]:
    ds = NonPolCalDataset()
    obj_list = [L0FitsAccess.from_header(d.header()) for d in ds]
    return obj_list
