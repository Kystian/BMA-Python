from tkinter import *
import machine
from state_machine import (State, Event, acts_as_state_machine, after, before, InvalidStateTransition)

cards = [1000, 200, 100]
cup_size_name = machine.size
price_price = int(machine.price)
counter = 0

  

  
@acts_as_state_machine
class MachinePay:
    screen_text = ""

    before_paying = State(initial=True)
    paying = State()
    after_paying = State()
    pay = Event(from_states=before_paying, to_state=paying)
    finish = Event(from_states=paying, to_state=after_paying)
    restart = Event(from_states=after_paying, to_state=before_paying)

    def __init__(self, root2, canvas2):
        self.root = root2
        self.canvas = canvas2

    def clear(self):
        if self.current_state == self.before_paying:
            self.transition(self.pay, "clear_pay")
        if self.current_state == self.paying:
            self.transition(self.finish, "clear_finish")
        if self.current_state == self.after_paying:
            self.transition(self.restart, "restart")

    def transition(self, event, event_name):
        try:
            event()
        except InvalidStateTransition as err:
            print(f'Error: transition of process from {self.current_state} to {event_name} failed')

    def draw_machine_pay(self):
        self.add_buttons()

    def add_buttons(self):
        cash = Button(self.root, text="Cash", width=15, height=2, command=lambda: self.button_action("Cash"))
        card = Button(self.root, text="Card points", width=15, height=2, command=lambda: self.button_action("card"))
        cash.grid(row=1, column=0, sticky=SE)
        card.grid(row=2, column=0, sticky=SE)

    def button_action(self, name):
        if self.current_state == self.before_paying:
            if name == "Cash":
                self.transition(self.pay, "paying")
                cash = Button(self.root, text="20gr", width=10, height=2,
                              command=lambda: self.button_cash_action("0.2"))
                cash1 = Button(self.root, text="50gr", width=10, height=2,
                               command=lambda: self.button_cash_action("0.5"))
                cash2 = Button(self.root, text="1zl", width=10, height=2, command=lambda: self.button_cash_action("1"))
                cash3 = Button(self.root, text="2zl", width=10, height=2, command=lambda: self.button_cash_action("2"))
                cash4 = Button(self.root, text="5zl", width=10, height=2, command=lambda: self.button_cash_action("5"))
                cash5 = Button(self.root, text="10zl", width=10, height=2,
                               command=lambda: self.button_cash_action("10"))
                cash6 = Button(self.root, text="20zl", width=10, height=2,
                               command=lambda: self.button_cash_action("20"))
                cash7 = Button(self.root, text="50zl", width=10, height=2,
                               command=lambda: self.button_cash_action("50"))
                cash8 = Button(self.root, text="100zl", width=10, height=2,
                               command=lambda: self.button_cash_action("100"))
                cash9 = Button(self.root, text="200zl", width=10, height=2,
                               command=lambda: self.button_cash_action("200"))
                cash.grid(row=1, column=2)
                cash1.grid(row=2, column=2)
                cash2.grid(row=3, column=2)
                cash3.grid(row=4, column=2)
                cash4.grid(row=5, column=2)
                cash5.grid(row=1, column=3)
                cash6.grid(row=2, column=3)
                cash7.grid(row=3, column=3)
                cash8.grid(row=4, column=3)
                cash9.grid(row=5, column=3)
            else:
                self.transition(self.pay, "paying")
                card1 = Button(self.root, text="card1", width=15, height=2, command=lambda: self.button_card_action(0))
                card2 = Button(self.root, text="card2", width=15, height=2, command=lambda: self.button_card_action(1))
                card3 = Button(self.root, text="card3", width=15, height=2, command=lambda: self.button_card_action(2))
                card1.grid(row=1, column=1, sticky=SW)
                card2.grid(row=2, column=1, sticky=SW)
                card3.grid(row=3, column=1, sticky=SW)

    def button_card_action(self, card_index):
        global cup_size_name
        is_allowed = machine.is_payment_allowed
        cup_size_name = machine.size
        if is_allowed:
            self.card_transaction(card_index)

    def card_transaction(self, card_index):
        global cards, cup_size_name
        if not self.current_state == self.after_paying:
            if cup_size_name == "small cup":
                if cards[card_index] >= 100:
                    cards[card_index] = cards[card_index] - 100
                    amount = str(cards[card_index])
                    self.screen_text = "Paid with points card.\npick up a drink\nPoints left: " + amount
                    machine.label_text = self.screen_text
                    self.transition(self.finish, "paid")
                else:
                    self.screen_text = "The card is empty"
                    machine.label_text = self.screen_text
            elif cup_size_name == "big cup":
                if cards[card_index] >= 200:
                    cards[card_index] = cards[card_index] - 200
                    amount = str(cards[card_index])
                    self.screen_text = "Paid with points card.\npick up a drink\nPoints left: " + amount
                    machine.label_text = self.screen_text
                    self.transition(self.finish, "paid")
                else:
                    amount = str(cards[card_index])
                    self.screen_text = "Transaction failed.\nThe card is empty\nYou have only "+ amount
                    machine.label_text = self.screen_text
                    self.transition(self.finish, "finish")

    def button_cash_action(self, name):
        global counter, price_price
        price_price = int(machine.price)
        is_allowed = machine.is_payment_allowed
        payment = float(name)
        counter = counter + payment
        if is_allowed:
            if counter < price_price:
                missing = price_price - counter
                missing_str = str(round(missing, 2))
                current_screen_txt = ('Missing ' + missing_str)
                self.screen_text = current_screen_txt
                machine.label_text = self.screen_text

            elif counter == price_price:
                self.screen_text = "Payment accepted\npick up a drink"
                machine.label_text = self.screen_text
                self.transition(self.finish, "paid")

            elif counter > price_price:
                change = counter - price_price
                change_str = str(change)
                current_screen_txt = ('Payment accepted \npick up a drink\n Change = ' + change_str)
                self.screen_text = current_screen_txt
                machine.label_text = self.screen_text
                self.transition(self.finish, "paid")
