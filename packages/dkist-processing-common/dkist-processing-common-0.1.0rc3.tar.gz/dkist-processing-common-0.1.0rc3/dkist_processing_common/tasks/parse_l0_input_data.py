"""
Common task to populate pipeline Constants and group files with tags by scanning headers
"""
import logging
from pathlib import Path
from typing import List
from typing import Tuple
from typing import TypeVar

from astropy.io import fits
from astropy.io.fits import HDUList
from dkist_header_validator import spec122_validator

from dkist_processing_common.models.constants import BudName
from dkist_processing_common.models.flower_pot import FlowerPot
from dkist_processing_common.models.flower_pot import Stem
from dkist_processing_common.models.tags import StemName
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.parsers.cs_step import CSStepFlower
from dkist_processing_common.parsers.cs_step import NumCSStepBud
from dkist_processing_common.parsers.l0_fits_access import L0FitsAccess
from dkist_processing_common.parsers.single_value_single_key_flower import (
    SingleValueSingleKeyFlower,
)
from dkist_processing_common.parsers.unique_bud import UniqueBud
from dkist_processing_common.tasks.base import WorkflowDataTaskBase
from dkist_processing_common.tasks.mixin.fits import FitsDataMixin
from dkist_processing_common.tasks.mixin.input_dataset import InputDatasetMixin

logger = logging.getLogger(__name__)
S = TypeVar("S", bound=Stem)


class ParseL0InputData(WorkflowDataTaskBase, FitsDataMixin, InputDatasetMixin):
    @property
    def constant_flowers(self) -> List[S]:
        return [
            NumCSStepBud(self.input_dataset_parameters_get("MAX_CS_STEP_TIME_SEC")),
            UniqueBud(constant_name=BudName.instrument.value, metadata_key="instrument"),
        ]

    @property
    def tag_flowers(self) -> List[S]:
        return [
            CSStepFlower(
                max_cs_step_time_sec=self.input_dataset_parameters_get("MAX_CS_STEP_TIME_SEC")
            ),
            SingleValueSingleKeyFlower(
                tag_stem_name=StemName.task.value, metadata_key="ip_task_type"
            ),
        ]

    @property
    def fits_parsing_class(self):
        return L0FitsAccess

    def run(self) -> None:

        with self.apm_step("Translate all input files"):
            self.translate_input()

        with self.apm_step("Ingest all input files"):
            tag_pot, constant_pot = self.make_flower_pots()

        with self.apm_step("Update constants"):
            self.update_constants(constant_pot)

        with self.apm_step("Tag files"):
            self.tag_petals(tag_pot)

    def make_flower_pots(self) -> Tuple[FlowerPot, FlowerPot]:
        """ Ingest all headers """
        tag_pot = FlowerPot()
        constant_pot = FlowerPot()
        tag_pot.flowers += self.tag_flowers
        constant_pot.flowers += self.constant_flowers
        for fits_obj in list(
            self.fits_data_read_fits_access(tags=Tag.input(), cls=self.fits_parsing_class)
        ):
            filepath = fits_obj.name
            tag_pot.add_dirt(filepath, fits_obj)
            constant_pot.add_dirt(filepath, fits_obj)

        return tag_pot, constant_pot

    def update_constants(self, constant_pot: FlowerPot):
        """ Update pipeline Constants """
        for flower in constant_pot:
            self.constants.update({flower.stem_name: flower.bud.value})

    def tag_petals(self, tag_pot: FlowerPot):
        """ Apply tags to file paths """
        for flower in tag_pot:
            for petal in flower.petals:
                tag = Tag.format_tag(flower.stem_name, petal.value)
                for path in petal.keys:
                    self.tag(path, tag)

    def translate_input(self):
        # This is the thing we want to delete when translation is handled by the Transfer task
        raw_input_paths = list(self.read(tags=Tag.input()))
        for filepath in raw_input_paths:
            hdl = self.translate_fits_file(filepath)
            self.fits_data_write(hdl, tags=Tag.input())
            self._scratch.delete(filepath)

    # Copied directly from old common.ParseInputData
    @staticmethod
    def translate_fits_file(filepath: Path) -> fits.HDUList:
        # This one gets deleted, too
        """
        Perform the spec 122 to spec 214 translation on fits files
        Parameters
        ----------
        filepath: path of the fits file to translate header for

        Returns
        -------
        the translated HDUList in spec 214 format
        """
        return spec122_validator.validate_and_translate(filepath, return_type=HDUList)
