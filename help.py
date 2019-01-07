import tkinter


class Help:
    help_window = None
    gl_img = None

    @staticmethod
    def show(parent):
        if Help.gl_img is None:
            Help.gl_img = tkinter.PhotoImage(file='assets/resources/good-luck.png')
        try:
            Help.help_window.lift()
            Help.help_window.focus_force()
        except:
            Help.help_window = tkinter.Toplevel(parent)
            Help.help_window.attributes('-toolwindow', True)
            Help.help_window.title('O hre')
            Help.help_window.attributes('-topmost', True)
            Help.help_window.resizable(False, False)
            Help.help_window.focus_force()
            Help.help_window.bind('<Escape>', lambda e: Help.close())
            canvas = tkinter.Canvas(Help.help_window, width=600, height=400)
            canvas.pack()
            canvas.create_text(10, 10, text='Ako hrať Osemsmerovky?', anchor='nw', font='Arial 16')
            canvas.create_text(10, 36, text='1.', anchor='nw')
            canvas.create_text(20, 36, text='Prvým kliknutím na políčko písmena označíte začiatok slova.', anchor='nw')
            canvas.create_text(10, 52, text='2.', anchor='nw')
            canvas.create_text(20, 52, text='Druhým kliknutím na ktorékoľvek zvýraznené políčko písmena označíte ' +
                                            'koniec slova. Ak je dané slovo\n' +
                                            'na zozname, tak sa prečiarnkne a zo zoznamu odstráni.', anchor='nw')
            canvas.create_text(10, 84, text='3.', anchor='nw')
            canvas.create_text(20, 84, text='Cieľom hry je nájsť všetky hľadané slová.', anchor='nw')
            canvas.create_text(10, 100, text='4.', anchor='nw')
            canvas.create_text(20, 100, text='Zvyšné písmená sú riešením tajničky.', anchor='nw')
            canvas.create_image(300, 210, image=Help.gl_img)
            canvas.create_text(20, 310, text='O hre', anchor='nw', font='Arial 14')
            canvas.create_text(20, 336,
                               text='Hra Osemserovky vznikla ako školský project v rámci predmetu Programovanie.',
                               anchor='nw')
            canvas.create_text(20, 356, text='Zdroj osemsemroviek: https://www.krizovkarsky-raj.sk/', anchor='nw')
            canvas.create_text(20, 378, text='Code is licensed under MIT License, Copyright 2018-2019 Juraj Marcin '
                                             + '(see LICENSE file for more details)', anchor='nw')

    @staticmethod
    def close():
        Help.help_window.destroy()
        Help.help_window = None
