from tkinter import *
import sys
import os

addition_size = []
counter = 0
is_beverage_chosen = False
is_size_chosen = False
is_order_finished = False
is_payment_allowed = False
size = "size"
label_text = "Choose beverage"
price = "0"


class MachineDraw:
    beverage_name = "Choose drink"
    size_name = "choose Size cup"
    summary_str = []
    payment_info = ".\n\nTap a card to use points or\ninsert coins/bills to pay with cash"
    bg_color = "yellow"

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if MachineDraw.__instance is None:
            MachineDraw(Tk(), Canvas())
        return MachineDraw.__instance

    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.screen_bg = Frame(self.root,bg=self.bg_color, width=280, height=100).grid(row=1, column=4, sticky=S)
        self.screen = Label(self.screen_bg, bg=self.bg_color, text="CHOOSE BEVERAGE", font="Helvetica 13 bold")
        if MachineDraw.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            MachineDraw.__instance = self

    def clear(self):
        self.__instance = None

    def update_text(self):
        global label_text
        self.screen.config(text=label_text)

    @staticmethod
    def change_screen_text(change_text):
        global label_text
        label_text = change_text

    def draw_machine(self):
        self.screen.grid(row=1, column=4, sticky=S)
        self.add_buttons()

    def add_buttons(self):
        button_bg = Frame(self.root, bg="grey", width=450, height=380, borderwidth=1).grid(row=1, column=0, rowspan=3, columnspan=4, sticky=N, padx=20, pady=40)

        coffee_black = Button(button_bg, text="Black Coffee", width=15, height=2, command=lambda: self.button_beverage_action("black coffee"))
        price_black_coffee = Label(button_bg, text="4/5zł", width=4, font="Helvetica 15 bold", pady=6)
        coffee_white = Button(button_bg, text="White Coffee", width=15, height=2, command=lambda: self.button_beverage_action("white coffee"))
        price_white_coffee = Label(button_bg, text="3/4zł", width=4, font="Helvetica 15 bold", pady=6)
        tea = Button(button_bg, text="Tea", width=15, height=2, command=lambda: self.button_beverage_action("tea"))
        price_tea = Label(button_bg, text="2/3zł", width=4, font="Helvetica 15 bold", pady=6)
        chicken_soup = Button(button_bg, text="Chicken Soup", width=15, height=2, command=lambda: self.button_beverage_action("chicken soup"))
        price_soup = Label(button_bg, text="4/5zł", width=4, font="Helvetica 15 bold", pady=6)
        borscht = Button(button_bg, text="Borscht", width=15, height=2, command=lambda: self.button_beverage_action("borscht"))
        price_borscht = Label(button_bg, text="5/6zł", width=4, font="Helvetica 15 bold", pady=6)
        cup = Label(self.root, text="CUP SIZE", font="Helvetica 10 bold")
        size_small = Button(self.root, text="SMALL", width=10, height=2, command=lambda: self.button_size_action("small cup"))
        size_big = Button(self.root, text="BIG", width=10, height=2, command=lambda: self.button_size_action("big cup"))
        Label(self.root, text="SUGAR / PEPPER", font="Helvetica 10 bold").grid(row=2, column=4, pady=10)
        extra_minus = Button(self.root, text="-", width=4, command=lambda: self.button_add_action("-"))
        extra_plus = Button(self.root, text="+", width=4, command=lambda: self.button_add_action("+"))
        cancel = Button(button_bg, text="Cancel/Restart", command=lambda: self.button_cancel_action())
        edit = Button(button_bg, text="Edit", command=lambda: self.button_edit_action())
        next = Button(button_bg, text="Next to pay", command=lambda: self.button_action_next())
        pay = Button(button_bg, text="Check payment status", command=lambda: self.button_pay_action())
        pay.grid(row=4, column=4, sticky=NE)
        next.grid(row=3, column=4, sticky=E)
        edit.grid(row=3, column=4, sticky=W)
        cancel.grid(row=4, column=4, sticky=NW)
        coffee_black.grid(row=1, column=2, sticky=SE, padx=10)
        price_black_coffee.grid(row=1, column=0, sticky= SE)
        coffee_white.grid(row=1, column=1, sticky=SW, padx=10)
        price_white_coffee.grid(row=1, column=3, sticky= SW)
        tea.grid(row=2, column=1, sticky=W, padx=10)
        price_tea.grid(row=2, column=0, sticky=E)
        chicken_soup.grid(row=2, column=2, sticky=E, padx=10)
        price_soup.grid(row=2, column=3, sticky=W)
        borscht.grid(row=3, column=1, sticky=NW, padx=10)
        price_borscht.grid(row=3, column=0, sticky=NE)
        cup.grid(row=4, column=1, columnspan=2)
        size_small.grid(row=4, column=1, sticky=W, columnspan=2)
        size_big.grid(row=4, column=1, sticky=E, columnspan=2)
        extra_minus.grid(row=2, column=4, sticky=W, pady=10)
        extra_plus.grid(row=2, column=4, sticky=E, pady=10)

    def button_pay_action(self):
        global is_payment_allowed
        if is_payment_allowed:
            self.update_text()

    def button_beverage_action(self, name):
        global is_beverage_chosen
        if not is_beverage_chosen:
            self.beverage_name = name
            self.screen.config(text=self.beverage_name)

            is_beverage_chosen = True

    def button_size_action(self, name):
        global is_size_chosen, size
        if not is_size_chosen:
            self.size_name = name
            size = name
            self.screen.config(text=self.size_name)

            is_size_chosen = True

    def button_add_action(self, name):
        global addition_size, counter
        if not is_order_finished:
            if name == "+" and counter < 5:
                addition_size.append('+')
                counter += 1
            elif name == "-" and counter > 0:
                addition_size.remove('+')
                counter -= 1
            self.screen.config(text=addition_size)

    def get_summary(self):
        global counter, is_order_finished
        if is_beverage_chosen == True and is_size_chosen == True:
            str1 = " "
            str1.join(addition_size)
            name_pepper = ('You chose ' + self.beverage_name + ' \n in ' + self.size_name + ' and ' + str(counter) + ' pepper')
            name_sugar = ('You chose ' + self.beverage_name + ' \n in ' + self.size_name + ' and ' + str(counter) + ' sugar')
            is_order_finished = True
            if self.beverage_name == "black coffee" or self.beverage_name == "white coffee" or self.beverage_name == "tea":
                self.summary_str = name_sugar
                return name_sugar
            else:
                self.summary_str = name_pepper
                return name_pepper
        elif is_beverage_chosen == True and is_size_chosen == False:
            return "You did not choose cup size"
        elif is_size_chosen == True and is_beverage_chosen == False:
            return "You did not choose beverage"
        else:
            return "Choose beverage"

    def button_edit_action(self):
        global is_size_chosen, is_order_finished, is_beverage_chosen
        is_size_chosen = False
        is_order_finished = False
        self.change_screen_text("Edit cup size and additions")
        self.update_text()

    def calculate_price(self):
        global is_payment_allowed, is_beverage_chosen, is_size_chosen
        self.change_screen_text(self.get_summary())
        self.update_text()
        if is_beverage_chosen and is_size_chosen:
            screen_txt = self.summary_str + self.payment_info
            self.screen.config(text=screen_txt)
            is_payment_allowed = True
            self.change_screen_text("Not paid yet")

            if self.beverage_name == "white coffee" or self.beverage_name == "chicken soup":
                if self.size_name == "SMALL":
                    return "4"
                else:
                    return "5"
            elif self.beverage_name == "black coffee":
                if self.size_name == "SMALL":
                    return "3"
                else:
                    return "4"
            elif self.beverage_name == "tea":
                if self.size_name == "SMALL":
                    return "2"
                else:
                    return "3"
            else:
                if self.size_name == "SMALL":
                    return "5"
                else:
                    return "6"
        else:
            return "0"

    def button_cancel_action(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def button_action_next(self):
        global price
        price = self.calculate_price()
