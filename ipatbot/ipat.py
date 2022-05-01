import logging
import time
import typing

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return driver


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


def login(driver: webdriver.Remote, userid: int, password: int, pars: int):
    driver.get("https://g.ipat.jra.go.jp/")
    driver.find_element(By.XPATH, "/html/body/form/p[2]/input").send_keys(userid)
    driver.find_element(By.XPATH, "/html/body/form/p[4]/input").send_keys(password)
    driver.find_element(By.XPATH, "/html/body/form/p[6]/input").send_keys(pars)
    driver.find_element(By.XPATH, "/html/body/form/p[8]/input").click()
    if driver.find_element(By.XPATH, "/html/body/header/p[2]").text == "【お客様へ】":
        driver.find_element(By.XPATH, "/html/body/form/p/input").click()
    return driver


def move_to_keibajo(
    driver: webdriver.Remote, keibajo_code: str, kaisai_kai: int, kaisai_nichime: int
):
    keibajo = get_keibajo(keibajo_code, kaisai_kai, kaisai_nichime)
    driver.find_element(By.XPATH, f'//input[contains(@value, "{keibajo}")]').click()
    return driver


def bet(driver: webdriver.Remote, codes: typing.List[str], total_amount: int):
    for i, code in enumerate(codes):
        driver.find_elements(By.XPATH, '//input[@type="tel"]')[i].send_keys(code)
    driver.find_element(By.XPATH, '//input[@value="入力終了"]').click()
    # confirm
    driver.find_element(By.XPATH, "/html/body/form/p[2]/input").send_keys(total_amount)
    driver.find_element(By.XPATH, "/html/body/form/p[3]/input").click()
    return driver


def deposit(driver: webdriver.Remote, amount: int, password: int):
    driver.find_element(By.XPATH, "/html/body/form[2]/p/input").click()
    driver.find_element(By.XPATH, '//*[@id="sokupat"]/form[1]/div/input').click()
    driver.find_element(
        By.XPATH, "/html/body/section[1]/form[1]/label/div/input"
    ).send_keys(amount)
    driver.find_element(By.XPATH, "/html/body/section[1]/form[1]/div[2]/input").submit()
    driver.find_element(By.XPATH, '//*[@id="_pin1M"]').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="main"]/form/div[4]/input').submit()


def quit(driver: webdriver.Remote):
    driver.close()
    driver.quit()


def screenshot(driver: webdriver.Remote, filename: str):
    w = driver.execute_script("return document.body.scrollWidth")
    h = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(w, h)
    driver.save_screenshot(filename)


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
    if dryrun:
        return
    try:
        driver = get_driver()
        login(driver, userid, password, pars)
        move_to_keibajo(driver, keibajo_code, kaisai_kai, kaisai_nichime)
        bet(driver, codes, total_amount)
        time.sleep(3)
        logger.info("success to bet")
    except Exception as e:
        logger.info(e)
        screenshot(driver, "error.png")
    finally:
        quit(driver)
        logger.info("quit driver")


def deposit_amount(userid: int, password: int, pars: int, amount: int):
    try:
        driver = get_driver()
        login(driver, userid, password, pars)
        deposit(driver, amount, password)
    except Exception as e:
        logger.info(e)
        screenshot(driver, "error.png")
    finally:
        quit(driver)
