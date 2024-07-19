
import os
from random import randint
import time
from tkinter import NO, Button, Tk, Frame, Label, mainloop, messagebox, PhotoImage
from tda import Cola_Circular_Doble
from typing import cast
from copy import deepcopy
from constants import *


class Btn():
    def __init__(self, root, text: str, row: int, col: int, color: str, cmd, index):
        self.btn = Button(root, text=text, command=lambda: self.on_click(cmd, index),
                          font=BUTTON_FONT, padx=0, pady=0, borderwidth=1, relief='solid', bg=color)
        self.btn.grid(row=row, column=col)

    def on_click(self, callback, index):
        self.btn.config(command=lambda: callback(index))


class Text():
    def __init__(self, parent, text: str, x: int, y: int):
        self.text = Label(parent, text=text, font=TEXT_FONT, bg='#fff')
        self.text.place(x=x, y=y)

    def update(self, texto: str):
        self.text.config(text=texto)

    def get(self) -> str:
        return self.text.cget('text')


class Box():
    def __init__(self, root, row, col, icon, color):
        self.root = root
        self.box = Frame(root, width=BOX_SIZE, height=BOX_SIZE)
        self.box.grid(row=row, column=col)
        self.icon = Label(self.box, text=icon,
                          font=ICON_FONT, fg=color, bg='#fff')
        self.icon.pack(fill='both', expand=True)

    def highlight(self):
        cast(Label, self.box.children['!label']).config(bg='#fd606e')

    def highlight_winner(self):
        cast(Label, self.box.children['!label']).config(bg='#2196f3')

    def unhighlight(self):
        cast(Label, self.box.children['!label']).config(bg='#fff')


class Window():
    boxes_ref: list[Box] = [None] * 16  # type: ignore
    values_ref: list[Label] = [None] * 7  # type: ignore
    buttons_ref: list[Btn] = [None] * 7  # type: ignore
    score_ref: Text = None  # type: ignore
    coins_ref: Text = None  # type: ignore

    start_ref: Btn = None  # type: ignore
    collect_ref: Btn = None  # type: ignore
    money_ref: Btn = None  # type: ignore

    boxes = Frame

    def __init__(self, queue: Cola_Circular_Doble):
        width = WINDOW_SIZE[0]
        height = WINDOW_SIZE[1]
        self.root = Tk()
        self.root.config(bg='#fff')
        self.queue = queue
        self.root.title('Slot Machine 🍒')
        self.root.resizable(False, False)
        self.root.geometry(f'{width}x{height}')
        self.boxes_ref = self.gen_boxes()
        self.gen_labels()
        self.values_ref = self.gen_values()
        self.buttons_ref = self.gen_buttons()
        self.gen_scores()
        self.gen_controls()

    def gen_scores(self):
        width = WINDOW_SIZE[0]
        width_middle = int(width / 2) - 50
        height_middle = int(width / 2) - 50
        self.score_ref = Text(self.root, 'Points: 0',
                              width_middle, height_middle)
        self.coins_ref = Text(self.root, 'Coins: 0',
                              width_middle, height_middle + 30)
        return self.values_ref

    def gen_boxes(self):
        size = WINDOW_SIZE[0]
        self.boxes = Frame(self.root, width=size, height=size, bg='#fff')
        self.boxes.grid(row=1, column=1)
        row, col = 0, 0
        while not self.queue.cola_vacia():
            box = cast(dict, self.queue.quitar_principio())
            icon = box['emoji']
            i = box['indice'] - 1
            color = [x[3] for x in OPTIONS if x[0] == icon][0]
            if row == 0:
                self.boxes_ref[i] = Box(self.boxes, row, col, icon, color)
            elif col == 4:
                self.boxes_ref[i] = Box(self.boxes, row, col, icon, color)
            elif row == 4:
                self.boxes_ref[i] = Box(self.boxes, row, col, icon, color)
            elif col == 0:
                self.boxes_ref[i] = Box(self.boxes, row, col, icon, color)
            if row == 0 and col < 4:
                col += 1
            elif col == 4 and row < 4:
                row += 1
            elif row == 4 and col > 0:
                col -= 1
            elif col == 0 and row > 0:
                row -= 1
        return self.boxes_ref

    def gen_labels(self):
        width = WINDOW_SIZE[0]
        height = BOX_SIZE
        self.labels = Frame(self.root, width=width, height=height, pady=5)
        self.labels.grid(row=2, column=1)

        for i in range(len(OPTIONS)):
            value = OPTIONS[i][2]
            label = Label(self.labels, text=value,
                          font=BUTTON_FONT, bg='#09f', width=2, pady=7, padx=11, borderwidth=2, relief='solid')
            label.grid(row=1, column=i)

    def gen_values(self):
        width = WINDOW_SIZE[0]
        height = BOX_SIZE
        self.label_bets = Frame(self.root, width=width, height=height, pady=0)
        self.label_bets.grid(row=3, column=1)

        for i in range(len(OPTIONS)):
            label = Label(
                self.label_bets,
                text='0',
                font=BUTTON_FONT,
                bg='#E11D48',
                fg='#fff',
                width=2,
                pady=7,
                padx=11,
                borderwidth=2,
                relief='solid'
            )
            label.grid(row=1, column=i)
            self.values_ref[i] = label
        return self.values_ref

    def gen_buttons(self):
        width = WINDOW_SIZE[0]
        height = BOX_SIZE
        self.buttons = Frame(self.root, width=width, height=height, pady=5)
        self.buttons.grid(row=4, column=1)

        for i in range(len(OPTIONS)):
            self.buttons_ref[i] = Btn(
                self.buttons, OPTIONS[i][0], 0, i, OPTIONS[i][3], lambda: None, i)

        return self.buttons_ref

    def gen_controls(self):
        width = WINDOW_SIZE[0]
        height = BOX_SIZE
        self.controls = Frame(self.root, width=width, height=height, pady=5)
        self.controls.grid(row=5, column=1)
        self.collect_ref = Btn(
            self.controls, '🤑', 0, 0, '#e53e3e', lambda: None, 0)
        self.start_ref = Btn(
            self.controls, '⏯️', 0, 1, '#4ade80', lambda: None, 1)
        self.money_ref = Btn(
            self.controls, '💰', 0, 2, '#fff', lambda: None, 2)


class Game():
    coins = 0
    points = 0
    bets = [0, 0, 0, 0, 0, 0, 0]
    winner_index = None
    winner_box = tuple[str, tuple[int], int, str]

    def splash_screen(self):
        self.sc = Tk()
        self.sc.geometry('394x394')
        # mostrar imagen
        dir = os.path.dirname(__file__)
        path = os.path.join(dir, 'sc.gif')
        self.img = PhotoImage(file=path)
        Label(self.sc, image=self.img).pack(fill='both', expand=True)
        self.sc.title('Slot Machine 🍒')

    def __init__(self, queue: Cola_Circular_Doble):
        queue2 = deepcopy(queue)
        self.splash_screen()
        self.sc.after(2000, self.load)
        self.queue = queue
        self.queue2 = queue2
        mainloop()

    def load(self):
        self.sc.destroy()
        self.window = Window(self.queue)
        self.window.boxes_ref[0].highlight()

        for i in range(len(self.window.buttons_ref)):
            self.window.buttons_ref[i].on_click(self.update_bet, i)

        self.window.start_ref.on_click(self.start, 0)
        self.window.collect_ref.on_click(self.collect, 0)
        self.window.money_ref.on_click(self.add_money, 0)
        self.window.root.mainloop()

    def update_bet(self, index):
        if self.coins > 0:
            self.coins -= 1
            self.bets[index] += 1
            self.window.values_ref[index].config(text=str(self.bets[index]))
            self.window.coins_ref.update(f'Coins: {self.coins}')
        else:
            messagebox.showwarning('No tienes monedas',
                                   'No tienes monedas para apostar')

    def start(self, index):
        has_bet = [x for x in self.bets if x > 0]
        if self.coins == 0 and len(has_bet) == 0:
            messagebox.showwarning('No tienes monedas',
                                   'No tienes monedas para apostar')
            return

        lap = 1  # Contador de vueltas (4 vueltas)

        while not self.queue2.cola_vacia() and lap <= 4:
            box = cast(dict, self.queue2.quitar_principio())
            i = box['indice'] - 1
            if i == 15:
                lap += 1

            if lap == 3 and i == 0:
                self.winner_index = randint(0, 15)

            self.window.boxes_ref[i].highlight()
            # Actualiza la interfaz gráfica para mostrar el cambio de color
            self.window.root.update_idletasks()
            time.sleep(0.1)
            self.window.boxes_ref[i].unhighlight()
            self.window.root.update_idletasks()  # Actualiza la interfaz gráfica nuevamente
            self.queue2.insertar_final(box)

            if self.winner_index is not None and i == self.winner_index:
                self.window.boxes_ref[i].highlight_winner()
                self.winner_box = [
                    x for x in OPTIONS if x[0] == box['emoji']][0]

        index = cast(int, self.winner_index)
        self.window.boxes_ref[index].highlight_winner()
        self.window.root.update_idletasks()
        selected_emoji = self.winner_box[0]  # type: ignore
        winner_index = [x[0]
                        for x in OPTIONS].index(selected_emoji)  # type: ignore

        if (self.bets[winner_index]):
            bet_count = self.bets[winner_index]
            bet_value = self.winner_box[2]  # type: ignore
            self.points += bet_count * int(bet_value)  # type: ignore
            self.window.score_ref.update(f'Points: {self.points}')
            self.reset_values()
        else:
            messagebox.showwarning('Has perdido',
                                   f'No le apostaste a {selected_emoji}')
            self.reset_values()

    def reset_values(self):
        self.winner_index = None
        self.winner_box = tuple[str, tuple[int], int, str]
        for i in range(len(self.window.values_ref)):
            self.window.values_ref[i].config(text='0')
        self.bets = [0, 0, 0, 0, 0, 0, 0]

    def add_money(self, index):
        self.coins += 1
        self.window.coins_ref.update(f'Coins: {self.coins}')

    def collect(self, index):
        text = self.window.score_ref.get()
        points = text.split(' ')[1]
        self.points += int(points)
        self.reset_values()
        messagebox.showinfo('Puntos', f'Has ganado {points} puntos')
        self.points = 0
        self.window.score_ref.update('Points: 0')
