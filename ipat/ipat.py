import logging
import time
import typing

import requests
import bs4
import urllib.parse

logger = logging.getLogger(__name__)


def get_keibajo(keibajo_code: str, kaisai_kai: int, kaisai_nichime: int):
    keibajo_code_name = {
        "01": "札幌",
        "02": "函館",
        "03": "福島",
        "04": "新潟",
        "05": "東京",
        "06": "中山",
        "07": "中京",
        "08": "京都",
        "09": "阪神",
        "10": "小倉",
    }
    return f"{kaisai_kai:0>2}{keibajo_code_name[keibajo_code]}{kaisai_nichime:0>2}"


def login(userid: int, password: int, pars: int) -> requests.Response:
    response = requests.get("https://g.ipat.jra.go.jp")
    soup = bs4.BeautifulSoup(response.content.decode("euc-jp"), features="html.parser")

    query = {"i": userid, "p": password, "r": pars}
    for input in soup.select("input[type=hidden]"):
        query[input.attrs["name"]] = input.attrs["value"]

    # TODO: Skip お知らせ

    url = "https://g.ipat.jra.go.jp/kw_020.cgi"
    data = urllib.parse.urlencode(query)

    response = requests.post(url, data=data)
    response.raise_for_status()

    return response


def move_to_keibajo(
    response: requests.Response, keibajo_code: str, kaisai_kai: int, kaisai_nichime: int
) -> requests.Response:
    kaisai = get_keibajo(keibajo_code, kaisai_kai, kaisai_nichime)

    # 開催選択

    soup = bs4.BeautifulSoup(response.content.decode("euc-jp"), features="html.parser")
    submit = soup.select(f'input[value^="{kaisai}"]')[0]

    query = {}
    query[submit.attrs["name"]] = submit.attrs["value"]
    for input in soup.select("form[name=jyou] input[type=hidden]"):
        query[input.attrs["name"]] = input.attrs["value"]

    url = "https://g.ipat.jra.go.jp/kw_050.cgi"
    data = urllib.parse.urlencode(query)
    response = requests.post(url, data=data)
    response.raise_for_status()

    return response


def bet(response: requests.Response, codes: typing.List[str]) -> requests.Response:
    # 馬券コード入力

    soup = bs4.BeautifulSoup(response.content.decode("euc-jp"), features="html.parser")

    query = {}
    for i, code in enumerate(codes):
        query[i] = code
    for input in soup.select("form[name=tousend] input[type=hidden]"):
        query[input.attrs["name"]] = input.attrs["value"]

    url = "https://g.ipat.jra.go.jp/kw_060.cgi"
    data = urllib.parse.urlencode(query)
    response = requests.post(url, data=data)
    response.raise_for_status()

    return response

def confirm(response: requests.Response, total_amount: int) -> requests.Response:
    # 注文確定

    soup = bs4.BeautifulSoup(response.content.decode("euc-jp"), features="html.parser")

    query = {"s": total_amount}
    for input in soup.select("form[name=touhyou] input[type=hidden]"):
        query[input.attrs["name"]] = input.attrs["value"]

    url = "https://g.ipat.jra.go.jp/kw_070.cgi"
    data = urllib.parse.urlencode(query)
    response = requests.post(url, data=data)
    response.raise_for_status()

    return response


def bet_codes(
    userid: int,
    password: int,
    pars: int,
    keibajo_code: str,
    kaisai_kai: int,
    kaisai_nichime: int,
    codes: typing.List[str],
    total_amount: int,
    dryrun=True,
):
    logger.info(
        f"keibajo_code, kaisai_kai, kaisai_nichime: {keibajo_code}, {kaisai_kai}, {kaisai_nichime}"
    )
    logger.info(f"codes: {codes}")
    logger.info(f"total_amount: {total_amount}")
    logger.info(f"dryrun: {dryrun}")

    response = login(userid, password, pars)
    response = move_to_keibajo(response, keibajo_code, kaisai_kai, kaisai_nichime)
    response = bet(response, codes)
    if dryrun:
        logger.info("dryrun: skip confirm")
        return
    else:
        response = confirm(response, total_amount)

    time.sleep(3)

    logger.info("finished to bet")
