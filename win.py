from tkinter import *

global SECTIONS_IN_COMMUTATOR
global COMMUTATOR_IN_SECTION


class Api_Win:
    def __init__(self):
        self.COM_LIST = []
        self.SECTIONS_IN_COMMUTATOR = 0
        self.COMMUTATOR_IN_SECTION = 0

    def get_values(self):
        build_button.config(state=DISABLED)

        try:
            self.SECTIONS_IN_COMMUTATOR = int(input_text_sec.get())
            self.COMMUTATOR_IN_SECTION = int(input_text_sec_in.get())
        except ValueError:
            print("BAD VALUE")
        input_text_sec.set("")
        input_text_sec_in.set("")
        self.build_com(sec=self.SECTIONS_IN_COMMUTATOR, com=self.COMMUTATOR_IN_SECTION)

    def build_com(self, *args, **kwarg):
        print(kwarg["sec"])
        for row_ in range(5, 5 + kwarg["sec"]):
            for column_ in range(4, 4 + kwarg["com"]):
                identity = str(row_ - 4) + " " + str(column_ - 3)
                yo_button = Button(
                    main_window,
                    text=identity,
                    width=8,
                    height=3,
                    padx=3,
                    pady=7,
                    command=lambda: self.clicked(
                        clicked_nr={"row": row_, "column": column_}
                    ),
                )
                self.COM_LIST.append(yo_button)
                yo_button.grid(row=row_, column=column_)

    def remove_com(self):
        for el in self.COM_LIST:
            el.destroy()
        build_button.config(state=NORMAL)
        self.SECTIONS_IN_COMMUTATOR = 0
        self.COMMUTATOR_IN_SECTION = 0
        self.COM_LIST = []
        pass

    def clicked(self, clicked_nr={}):
        print(clicked_nr)
        pass

    def calculate(self):
        pass


# Main functions
main_window = Tk()
api_win = Api_Win()
main_window.geometry("1000x500")
main_window.resizable(0, 0)
main_window.title("Commutator Simulator")

input_text_sec = StringVar()
input_text_sec_in = StringVar()
input_sec_choose = StringVar()
input_sec_in = StringVar()
input_port_choose = StringVar()

# Creating of elements
label_sections = Label(main_window, text="Nr_in_sec")
label_in_section = Label(main_window, text="Com_in_sec")
label_control = Label(main_window, text="Control_Panel")
label_in_com = Label(main_window, text="Sec")
label_in_sec = Label(main_window, text="Com")
label_in_port = Label(main_window, text="Port")
sec_entry = Entry(main_window, width=20, textvariable=input_text_sec)
sec_in_entry = Entry(main_window, width=20, textvariable=input_text_sec_in)
sec_choose = Entry(main_window, width=20, textvariable=input_sec_choose)
sec_in_choose = Entry(main_window, width=20, textvariable=input_sec_in)
port_choose = Entry(main_window, width=20, textvariable=input_port_choose)
results = Text(main_window, height=15, width=30)
build_button = Button(
    main_window,
    text="Build",
    width=8,
    height=3,
    padx=3,
    pady=7,
    command=lambda: api_win.get_values(),
)
clear_button = Button(
    main_window,
    text="Clear",
    width=8,
    height=3,
    padx=3,
    pady=7,
    command=lambda: api_win.remove_com(),
)
get_button = Button(
    main_window,
    text="Calc",
    width=8,
    height=3,
    padx=3,
    pady=7,
    command=lambda: api_win.calculate(),
)
yo_button = Button(
    main_window,
    text="YO",
    width=8,
    height=3,
    padx=3,
    pady=7,
    command=lambda: api_win.calculate(),
)


# Adding of input elements
label_sections.grid(row=0, column=0)
label_in_section.grid(row=1, column=0, padx=3, pady=3)
sec_entry.grid(row=0, column=1, columnspan=2, padx=3, pady=3)
sec_in_entry.grid(row=1, column=1, columnspan=2, padx=3, pady=3)
label_in_com.grid(row=0, column=3, padx=20, pady=3)
label_in_sec.grid(row=1, column=3, padx=20, pady=3)
sec_in_choose.grid(row=0, column=5, columnspan=2, padx=3, pady=3)
sec_choose.grid(row=1, column=5, columnspan=2, padx=3, pady=3)
label_in_port.grid(row=0, column=7, padx=20, pady=3)
port_choose.grid(row=0, column=8, columnspan=2, padx=3, pady=3)
port_choose.grid(row=0, column=8, columnspan=2, padx=3, pady=3)


label_control.grid(row=4, column=1, padx=1, pady=20)
build_button.grid(row=5, column=0, padx=25)
clear_button.grid(row=5, column=1, padx=20)
get_button.grid(row=5, column=2, padx=20)
results.grid(row=6, column=0, columnspan=3, rowspan=3, padx=10, pady=10, sticky=W + E)
# yo_button.grid(row=5, column=4)
# yo_button_.grid(row=6, column=4)
# yo_button__.grid(row=7, column=4)


main_window.mainloop()
