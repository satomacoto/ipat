import typing
import uuid
from dataclasses import dataclass
from itertools import groupby

import pandas as pd

from .baken import Baken
from .ipat import bet_codes


@dataclass
class BetUnit:
    def __init__(self, bakens: typing.List[Baken]) -> None:
        self.bakens = bakens

    def __repr__(self) -> str:
        return f"total_amount: {self.total_amount}, codes: {self.codes}"

    @property
    def codes(self) -> typing.List[str]:
        return [baken.code for baken in self.bakens]

    @property
    def total_amount(self) -> int:
        total_maisu = 0
        for code in self.codes:
            total_maisu += int(code[-3:])
        return total_maisu * 100


class Bet:
    """IPATでベットするためのクラス"""

    def __init__(self, bakens: typing.List[Baken]) -> None:
        self.uuid = uuid.uuid4()

        bakens = list(bakens)
        self.bakens = bakens

        bet_units = {}
        bakens.sort(key=lambda x: x.key)
        for key, group in groupby(bakens, key=lambda x: x.key):
            bet_units[key] = BetUnit(list(group))  # TODO: check max bet_unit size
        self._bet_units = bet_units

    def bet(self, *, userid, password, pars, dryrun=True) -> "Bet":
        for (
            (keibajo_code, kaisai_kai, kaisai_nichime),
            bet_unit,
        ) in self._bet_units.items():
            bet_codes(
                userid,
                password,
                pars,
                keibajo_code,
                kaisai_kai,
                kaisai_nichime,
                bet_unit.codes,
                bet_unit.total_amount,
                dryrun=dryrun,
            )
        return self

    def to_frame(self) -> pd.DataFrame:
        dicts = [baken.to_dict() for baken in self.bakens]
        return pd.DataFrame(dicts)
