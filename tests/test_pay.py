import pytest
import src.pay
import src.machine
from tkinter import *

global payment_handler


@pytest.fixture(scope="session", autouse=True)
def setup():
    global payment_handler
    root2 = Tk()
    canvas2 = Canvas()
    payment_handler = src.pay.MachinePay(root2, canvas2)
    payment_handler.draw_machine_pay()


@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    global payment_handler
    yield
    payment_handler.clear()


@pytest.mark.parametrize("method", ["Cash", "card"])
def test_button_action(method):
    # prepare
    global payment_handler
    # do
    payment_handler.button_action(method)
    # check
    assert payment_handler.current_state == payment_handler.paying


@pytest.mark.parametrize("index, size", [(0, "small cup"), (0, "big cup"), (1, "small cup"), (1, "big cup"),
                                         (2, "small cup"), (2, "big cup")])
def test_card_transaction(index, size):
    # prepare
    global payment_handler
    src.pay.cards = [1000, 200, 100]
    src.pay.cup_size_name = size
    payment_handler.transition(payment_handler.pay, "test_pay")
    # do
    payment_handler.card_transaction(index)
    # check
    assert payment_handler.current_state == payment_handler.after_paying

