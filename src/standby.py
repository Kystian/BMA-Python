from tkinter import *
from tkinter import messagebox
import machine
import pay

root = Tk()
root2 = Tk()
canvas = Canvas()
canvas2 = Canvas()
root.title("Beverage Machine")
root.geometry("790x520")
root2.title("Wallet")
root2.geometry("275x205")


def walletProtocol():
    if messagebox.askokcancel("OH NO!!!!", "Are you sure to leave your wallet at home? You won't be able to pay for your order :("):
        root2.destroy()


def machineDestroy():
    root.destroy()
    root2.destroy()


if __name__ == '__main__':
    beverage_machine = machine.MachineDraw(root, canvas)
    beverage_machine.draw_machine()
    PPay = pay.MachinePay(root2, canvas2)
    PPay.draw_machine_pay()
    root.protocol("WM_DELETE_WINDOW", machineDestroy)
    root2.protocol("WM_DELETE_WINDOW", walletProtocol)

    root.mainloop()
    root2.mainloop()
