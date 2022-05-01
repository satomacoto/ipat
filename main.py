import datetime

from ipatbot.baken import Baken
from ipatbot.baken_syurui import BakenSyurui
from ipatbot.bet import Bet

if __name__ == "__main__":
    bakens = [
        Baken(
            race_id=199808060210,
            race_date=datetime.date(1998, 11, 8),
            baken_syurui=BakenSyurui.TAN,
            bango1=13,
            maisu=10,
        ),
        Baken(
            race_id=199808060211,
            race_date=datetime.date(1998, 11, 8),
            baken_syurui=BakenSyurui.TAN,
            bango1=4,
            maisu=100,
        ),
        Baken(
            race_id=199808060211,
            race_date=datetime.date(1998, 11, 8),
            baken_syurui=BakenSyurui.UMATAN,
            bango1=4,
            bango2=17,
            maisu=100,
        ),
    ]
    bet = Bet(bakens)
    bet.bet(userid=1234567890, password=1234, pars=5678, dryrun=True)
