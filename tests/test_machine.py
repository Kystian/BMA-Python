import pytest
import src.machine
import src.standby
from tkinter import *
global beverage_machine

@pytest.fixture(scope="session", autouse=True)
def setup():
    global beverage_machine
    root = Tk()
    canvas = Canvas()
    beverage_machine = src.machine.MachineDraw(root, canvas)
    beverage_machine.draw_machine()


@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    global beverage_machine
    yield
    beverage_machine.clear()


@pytest.mark.parametrize("beverage", ["black coffee", "white coffee", "tea"])
def test_get_summary_sugar(beverage):
    # prepare
    global beverage_machine
    src.machine.is_beverage_chosen = True
    src.machine.is_size_chosen = True
    beverage_machine.size_name = "small cup"
    beverage_machine.beverage_name = beverage
    # do
    summary = beverage_machine.get_summary()
    # check
    assert summary == "You chose " + beverage + " \n in small cup and 0 sugar"


@pytest.mark.parametrize("beverage", ["chicken soup", "borscht"])
def test_get_summary_pepper(beverage):
    # prepare
    global beverage_machine
    src.machine.is_beverage_chosen = True
    src.machine.is_size_chosen = True
    beverage_machine.size_name = "small cup"
    beverage_machine.beverage_name = beverage
    # do
    summary = beverage_machine.get_summary()
    # check
    assert summary == "You chose " + beverage + " \n in small cup and 0 pepper"


@pytest.mark.parametrize("size", ["small cup", "big cup"])
def test_get_summary_cup_size(size):
    # prepare
    global beverage_machine
    src.machine.is_beverage_chosen = True
    src.machine.is_size_chosen = True
    beverage_machine.size_name = size
    beverage_machine.beverage_name = "chicken soup"
    # do
    summary = beverage_machine.get_summary()
    # check
    assert summary == "You chose chicken soup \n in " + size + " and 0 pepper"


def test_get_summary_no_size():
    # prepare
    global beverage_machine
    src.machine.is_beverage_chosen = True
    src.machine.is_size_chosen = False
    beverage_machine.beverage_name = "chicken soup"
    # do
    summary = beverage_machine.get_summary()
    # check
    assert summary == "You did not choose cup size"


def test_get_summary_no_beverage():
    # prepare
    global beverage_machine
    src.machine.is_beverage_chosen = False
    src.machine.is_size_chosen = True
    beverage_machine.size_name = "small cup"
    # do
    summary = beverage_machine.get_summary()
    # check
    assert summary == "You did not choose beverage"


def test_get_summary_nothing_chosen():
    # prepare
    global beverage_machine
    src.machine.is_beverage_chosen = False
    src.machine.is_size_chosen = False
    # do
    summary = beverage_machine.get_summary()
    # check
    assert summary == "Choose beverage"


@pytest.mark.parametrize("beverage, size, expected", [("chicken soup", "SMALL", "4"), ("chicken soup", "BIG", "5")])
def test_calculate_price_chicken_soup(beverage, size, expected):
    # prepare
    global beverage_machine
    src.machine.is_beverage_chosen = True
    src.machine.is_size_chosen = True
    src.machine.is_payment_allowed = False
    beverage_machine.beverage_name = beverage
    beverage_machine.size_name = size
    # do
    price = beverage_machine.calculate_price()
    # check
    assert price == expected
    assert src.machine.is_payment_allowed


@pytest.mark.parametrize("beverage, size, expected", [("black coffee", "SMALL", "3"), ("black coffee", "BIG", "4")])
def test_calculate_price_black_coffee(beverage, size, expected):
    # prepare
    global beverage_machine
    src.machine.is_beverage_chosen = True
    src.machine.is_size_chosen = True
    src.machine.is_payment_allowed = False
    beverage_machine.beverage_name = beverage
    beverage_machine.size_name = size
    # do
    price = beverage_machine.calculate_price()
    # check
    assert price == expected
    assert src.machine.is_payment_allowed


@pytest.mark.parametrize("beverage, size, expected", [("white coffee", "SMALL", "4"), ("white coffee", "BIG", "5")])
def test_calculate_price_white_coffee(beverage, size, expected):
    # prepare
    global beverage_machine
    src.machine.is_beverage_chosen = True
    src.machine.is_size_chosen = True
    src.machine.is_payment_allowed = False
    beverage_machine.beverage_name = beverage
    beverage_machine.size_name = size
    # do
    price = beverage_machine.calculate_price()
    # check
    assert price == expected
    assert src.machine.is_payment_allowed


@pytest.mark.parametrize("beverage, size, expected", [("tea", "SMALL", "2"), ("tea", "BIG", "3")])
def test_calculate_price_tea(beverage, size, expected):
    # prepare
    global beverage_machine
    src.machine.is_beverage_chosen = True
    src.machine.is_size_chosen = True
    src.machine.is_payment_allowed = False
    beverage_machine.beverage_name = beverage
    beverage_machine.size_name = size
    # do
    price = beverage_machine.calculate_price()
    # check
    assert price == expected
    assert src.machine.is_payment_allowed


@pytest.mark.parametrize("beverage, size, expected", [("borscht", "SMALL", "5"), ("borscht", "BIG", "6")])
def test_calculate_price_borscht(beverage, size, expected):
    # prepare
    global beverage_machine
    src.machine.is_beverage_chosen = True
    src.machine.is_size_chosen = True
    src.machine.is_payment_allowed = False
    beverage_machine.beverage_name = beverage
    beverage_machine.size_name = size
    # do
    price = beverage_machine.calculate_price()
    # check
    assert price == expected
    assert src.machine.is_payment_allowed


def test_calculate_price_nothing_chosen():
    # prepare
    global beverage_machine
    src.machine.is_beverage_chosen = False
    src.machine.is_size_chosen = False
    src.machine.is_payment_allowed = False
    # do
    price = beverage_machine.calculate_price()
    # check
    assert price == "0"
    assert src.machine.is_payment_allowed == False
