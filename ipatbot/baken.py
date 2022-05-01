"""
## 通常投票

```
【操作ガイド】
(通常投票)

投票入力欄を選択し、次の順に入力してください。

●レース番号を2桁の数字で入力します。
01～12

●式別を1桁の数字で入力します。

単勝　: 1
複勝　: 2
枠連　: 3
馬連　: 4
ワイド: 5
馬単　: 6
３連複: 7
３連単: 8
●馬(枠)番を入力します。

単勝・複勝
 数字2桁 01～18
枠連
 数字2桁
 1－2なら12
馬連・ワイド
 数字4桁
 1番－12番なら
 0112
馬単
 数字4桁
 10番→8番なら
 1008
３連複
 数字6桁
 1番－2番－13番なら
 010213
３連単
 数字6桁
 15番→1番→6番なら
 150106
●枚数を3桁の数字で入力します。

  1枚なら001
 30枚なら030
500枚なら500

(入力例)

3レースの枠連5－8を20枚(2000円)購入する場合
03358020


3レースの馬連5番－8番を20枚(2000円)購入する場合
0340508020


4レースの馬単9番→6番を100枚(10000円)購入する場合
0460906100


5レースの３連複2番－5番－12番を200枚(20000円)購入する場合
057020512200


6レースの３連単11番→2番→9番を100枚(10000円)購入する場合
068110209100


なお、プッシュホン投票で入力可能な省略入力には対応しておりませんのでご注意ください。
```
"""


import datetime
import typing

from .baken_syurui import BakenSyurui


def get_tan_code(race_bango: int, umaban: int, maisu: int) -> str:
    return f"{race_bango:0>2}{BakenSyurui.TAN}{umaban:0>2}{maisu:0>3}"


def get_fuku_code(race_bango: int, umaban: int, maisu: int) -> str:
    return f"{race_bango:0>2}{BakenSyurui.FUKU}{umaban:0>2}{maisu:0>3}"


def get_waku_code(race_bango: int, wakuban1: int, wakuban2: int, maisu: int) -> str:
    return f"{race_bango:0>2}{BakenSyurui.WAKU}{wakuban1}{wakuban2}{maisu:0>3}"


def get_umaren_code(race_bango: int, umaban1: int, umaban2: int, maisu: int) -> str:
    return f"{race_bango:0>2}{BakenSyurui.UMAREN}{umaban1:0>2}{umaban2:0>2}{maisu:0>3}"


def get_wide_code(race_bango: int, umaban1: int, umaban2: int, maisu: int) -> str:
    return f"{race_bango:0>2}{BakenSyurui.WIDE}{umaban1:0>2}{umaban2:0>2}{maisu:0>3}"


def get_umatan_code(race_bango: int, umaban1: int, umaban2: int, maisu: int) -> str:
    return f"{race_bango:0>2}{BakenSyurui.UMATAN}{umaban1:0>2}{umaban2:0>2}{maisu:0>3}"


def get_sanfuku_code(
    race_bango: int, umaban1: int, umaban2: int, umaban3: int, maisu: int
) -> str:
    return f"{race_bango:0>2}{BakenSyurui.SANFUKU}{umaban1:0>2}{umaban2:0>2}{umaban3:0>2}{maisu:0>3}"


def get_santan_code(
    race_bango: int, umaban1: int, umaban2: int, umaban3: int, maisu: int
) -> str:
    return f"{race_bango:0>2}{BakenSyurui.SANTAN}{umaban1:0>2}{umaban2:0>2}{umaban3:0>2}{maisu:0>3}"


def get_code(
    race_bango: int,
    baken_syurui: BakenSyurui,
    bango1: int,
    bango2: int,
    bango3: int,
    maisu: int,
) -> str:
    """IPATの投票コードの生成

    Args:
        race_bango (int): レース番号
        baken_syurui (BakenSyurui): 馬券の種類
        bango1 (int): 1頭目
        bango2 (int): 2頭目
        bango3 (int): 3頭目
        maisu (int): 枚数。1 = 100円

    Returns:
        str: 投票コード
    """
    if baken_syurui == BakenSyurui.TAN:
        return get_tan_code(race_bango, bango1, maisu)
    if baken_syurui == BakenSyurui.FUKU:
        return get_fuku_code(race_bango, bango1, maisu)
    if baken_syurui == BakenSyurui.WAKU:
        return get_waku_code(race_bango, bango1, bango2, maisu)
    if baken_syurui == BakenSyurui.UMAREN:
        return get_umaren_code(race_bango, bango1, bango2, maisu)
    if baken_syurui == BakenSyurui.WIDE:
        return get_wide_code(race_bango, bango1, bango2, maisu)
    if baken_syurui == BakenSyurui.UMATAN:
        return get_umatan_code(race_bango, bango1, bango2, maisu)
    if baken_syurui == BakenSyurui.SANFUKU:
        return get_sanfuku_code(race_bango, bango1, bango2, bango3, maisu)
    if baken_syurui == BakenSyurui.SANTAN:
        return get_santan_code(race_bango, bango1, bango2, bango3, maisu)


class BakenRecord(typing.TypedDict, total=False):
    race_id: int
    race_date: datetime.datetime
    baken_syurui: BakenSyurui
    bango1: int
    bango2: int
    bango3: int
    maisu: int


class Baken:
    def __init__(
        self,
        *,
        race_id: int,
        race_date: datetime.datetime,
        baken_syurui: BakenSyurui,
        bango1: int,
        bango2: int = -1,
        bango3: int = -1,
        maisu: int,
        **args,
    ) -> None:
        self.race_id = race_id
        (
            self.year,
            self.keibajo_code,
            self.kaisai_kai,
            self.kaisai_nichime,
            self.race_bango,
        ) = self._split_race_id(race_id)
        self.race_date = race_date
        self.baken_syurui = baken_syurui
        self.bango1 = bango1
        self.bango2 = bango2
        self.bango3 = bango3
        self.maisu = maisu
        self.code = get_code(
            self.race_bango,
            self.baken_syurui,
            self.bango1,
            self.bango2,
            self.bango3,
            self.maisu,
        )

    def _split_race_id(self, race_id: int) -> typing.Tuple[int, str, int, int, int]:
        # race_id: 2021 06 05 05 11
        race_id = str(race_id)
        year, keibajo_code, kaisai_kai, kaisai_nichime, race_bango = (
            race_id[:4],
            race_id[4:6],
            race_id[6:8],
            race_id[8:10],
            race_id[10:12],
        )
        return (
            int(year),
            keibajo_code,
            int(kaisai_kai),
            int(kaisai_nichime),
            int(race_bango),
        )

    @property
    def key(self) -> typing.Tuple[str, int, int]:
        return self.keibajo_code, self.kaisai_kai, self.kaisai_nichime

    def to_dict(self) -> BakenRecord:
        return BakenRecord(
            race_id=self.race_id,
            race_date=self.race_date,
            year=self.year,
            keibajo_code=self.keibajo_code,
            kaisai_kai=self.kaisai_kai,
            kaisai_nichime=self.kaisai_nichime,
            race_bango=self.race_bango,
            baken_syurui=self.baken_syurui,
            bango1=self.bango1,
            bango2=self.bango2,
            bango3=self.bango3,
            maisu=self.maisu,
        )
