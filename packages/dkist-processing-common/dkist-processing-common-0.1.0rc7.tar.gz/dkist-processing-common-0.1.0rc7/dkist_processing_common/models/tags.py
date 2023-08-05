"""
Components of the Tag model.  Stem + Optional Suffix = Tag
"""
from enum import Enum
from typing import Union


class StemName(str, Enum):
    """
    Controlled list of Tag Stems
    """

    output = "OUTPUT"
    input = "INPUT"
    intermediate = "INTERMEDIATE"
    input_dataset = "INPUT_DATASET"
    frame = "FRAME"
    movie = "MOVIE"
    task = "TASK"
    cs_step = "CS_STEP"
    modstate = "MODSTATE"


class Tag:
    """
    Controlled methods for creating tags from stems + optional suffixes
    """

    @staticmethod
    def format_tag(stem: Union[StemName, str], *parts):
        if isinstance(stem, Enum):
            stem = stem.value
        parts = [stem, *parts]
        return "_".join([str(part).upper() for part in parts])

    # Static Tags
    @classmethod
    def input(cls):
        return cls.format_tag(StemName.input)

    @classmethod
    def output(cls):
        return cls.format_tag(StemName.output)

    @classmethod
    def frame(cls):
        return cls.format_tag(StemName.frame)

    @classmethod
    def intermediate(cls):
        return cls.format_tag(StemName.intermediate)

    @classmethod
    def input_dataset(cls):
        return cls.format_tag(StemName.input_dataset)

    @classmethod
    def movie(cls):
        return cls.format_tag(StemName.movie)

    # Dynamic Tags
    @classmethod
    def task(cls, ip_task_type: str):
        return cls.format_tag(StemName.task, ip_task_type)

    @classmethod
    def cs_step(cls, n: int):
        return cls.format_tag(StemName.cs_step, n)

    @classmethod
    def modstate(cls, n: int):
        return cls.format_tag(StemName.modstate, n)
