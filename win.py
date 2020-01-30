#!/bin/python3

import json
import logging as log
from commutation.commutator_globals import Const_For_Commutators as Consts
from main import main
from tkinter import *

global SECTIONS_IN_COMMUTATOR
global COMMUTATOR_IN_SECTION


class Api_Win:
    def __init__(self):
        log.basicConfig(
            format="%(asctime)s - %(message)s",
            level=log.INFO,
            datefmt="%d-%b-%y %H:%M:%S",
        )
        self.const = Consts()
        self.COM_LIST = list()
        self.CONNECTION_LIST = dict()
        self.SECTIONS_IN_COMMUTATOR = 0
        self.COMMUTATOR_IN_SECTION = 0
        self.canvas = None

    def send_json_to_file(self):
        build_json = {
            "commutators": {
                "IN": 2 * self.SECTIONS_IN_COMMUTATOR,
                "OUT": 2 * self.SECTIONS_IN_COMMUTATOR,
                "SECTION": self.COMMUTATOR_IN_SECTION,
                "IN_SECTION": self.SECTIONS_IN_COMMUTATOR,
                "COMMUTATORS": self.COMMUTATOR_IN_SECTION
                * self.SECTIONS_IN_COMMUTATOR,
            }
        }
        build_json.update(self.CONNECTION_LIST)
        file_write = "config/commutator_config_super.json"
        with open(file_write, "w") as data_file:
            json.dump(build_json, data_file, indent=3)
        return file_write

    def get_values(self):
        build_button.config(state=DISABLED)
        try:
            self.SECTIONS_IN_COMMUTATOR = int(input_text_sec.get())
            self.COMMUTATOR_IN_SECTION = int(input_text_sec_in.get())
        except ValueError:
            print("BAD VALUE")
        input_text_sec.set("")
        input_text_sec_in.set("")
        self.build_com(
            sec=self.SECTIONS_IN_COMMUTATOR, com=self.COMMUTATOR_IN_SECTION
        )

    def build_com(self, *args, **kwarg):
        add_con_button.config(state=NORMAL)
        clear_button.config(state=NORMAL)
        get_button.config(state=NORMAL)
        self.canvas = Canvas(com_frame, height=600)
        self.canvas.pack(side=TOP, fill=BOTH)
        self.CONNECTION_LIST.setdefault("connections", {"sections": {}})
        for column_ in range(kwarg["com"]):
            column = self.const.address_decoder[column_ + 1]
            self.CONNECTION_LIST["connections"]["sections"].setdefault(
                column, {"commutator": {}}
            )
            for row_ in range(kwarg["sec"]):
                identity = str(row_ + 1) + " " + str(column_ + 1)
                row = self.const.address_decoder[row_ + 1]
                self.CONNECTION_LIST["connections"]["sections"][column][
                    "commutator"
                ].setdefault(
                    row,
                    {
                        interface: "None"
                        for interface in self.const.in_out_entries
                    },
                )
                self.canvas.create_rectangle(
                    10 + column_ * 120,
                    10 + row_ * 70,
                    100 + column_ * 120,
                    60 + row_ * 70,
                    outline="#f11",
                    fill="#1f1",
                    width=2,
                )
                # com_button = Button(
                #     com_frame,
                #     text=identity,
                #     width=8,
                #     height=3,
                #     padx=3,
                #     pady=7,
                # )
                # self.COM_LIST.append(com_button)
                # com_button.grid(row=row_, column=column_, padx=15, pady=15)

    def remove_com(self):
        # for com in self.COM_LIST:
        # com.destroy()
        build_button.config(state=NORMAL)
        add_con_button.config(state=DISABLED)
        clear_button.config(state=DISABLED)
        get_button.config(state=DISABLED)
        results.delete(1.0, END)
        results_calculate.delete(1.0, END)
        self.canvas.destroy()
        self.SECTIONS_IN_COMMUTATOR = 0
        self.COMMUTATOR_IN_SECTION = 0
        self.COM_LIST = []
        self.CONNECTION_LIST = {}
        self.CONNECTION_LIST.setdefault("connections", {"sections": {}})

    def calculate(self):
        log_list = main(file_to_read=self.send_json_to_file())
        for log_ in log_list:
            results_calculate.insert(END, log_)

    def add_connect(self):
        try:
            result_text = ""
            conn_seq = list()
            sec = int(sec_choose.get())
            conn_seq.append(sec)
            com_in = int(com_in_sec_choose.get())
            conn_seq.append(com_in)
            port_in = int(port_in_choose.get())
            conn_seq.append(port_in)
            com_out = int(com_out_in_choose.get())
            conn_seq.append(com_out)
            port_out = int(port_out_choose.get())
            conn_seq.append(port_out)
            self.canvas.create_line(
                100 + (sec - 1) * 120,
                20 + (com_out - 1) * 70 + port_out * 30,
                130 + (sec - 1) * 120,
                20 + (com_in - 1) * 70 + port_in * 30,
                dash=(4, 2),
            )
            for conn in conn_seq:
                if conn is None:
                    log.info("None value")
                    raise ValueError("None value")
            if port_in == 0:
                interface_in = self.const.in_out_entries[0]
            elif port_in == 1:
                interface_in = self.const.in_out_entries[1]
            else:
                log.info("Bad Port")
                raise ValueError("Bad port")

            if port_out == 0:
                interface_out = self.const.in_out_entries[2]
            elif port_out == 1:
                interface_out = self.const.in_out_entries[3]
            else:
                log.info("Bad Port")
                raise ValueError("Bad Port")

            if sec > self.SECTIONS_IN_COMMUTATOR and sec < 1:
                log.info("Bad Section")
                raise ValueError("Bad Section")

            if com_in > self.COMMUTATOR_IN_SECTION and com_in < 1:
                log.info("Bad Commutator")
                raise ValueError("Bad Commutator")

            if com_out > self.COMMUTATOR_IN_SECTION and com_out < 1:
                log.info("Bad Commutator")
                raise ValueError("Bad Commutator")
            seperator = "_"
            address_out = seperator.join(
                [
                    self.const.address_decoder[sec + 1],
                    self.const.address_decoder[com_in],
                    self.const.address_decoder[port_in],
                ]
            )
            address_in = seperator.join(
                [
                    self.const.address_decoder[sec],
                    self.const.address_decoder[com_out],
                    self.const.address_decoder[port_out],
                ]
            )
            section = self.const.address_decoder[sec]
            com_out = self.const.address_decoder[com_out]
            port = self.const.address_decoder[port_out]
            result_text = (
                "S_O: "
                + section
                + " C: "
                + com_out
                + " P: "
                + port
                + " A: "
                + address_out
                + "\n"
            )
            self.CONNECTION_LIST["connections"]["sections"][section][
                "commutator"
            ][com_out][interface_out] = address_out
            com_in = self.const.address_decoder[com_in]
            section = self.const.address_decoder[sec + 1]
            port = self.const.address_decoder[port_in]
            result_text += (
                "S_I: "
                + section
                + " C: "
                + com_in
                + " P: "
                + port
                + " A: "
                + address_in
                + "\n"
            )
            self.CONNECTION_LIST["connections"]["sections"][section][
                "commutator"
            ][com_in][interface_in] = address_in
            log.info(self.CONNECTION_LIST)
            results.insert(END, result_text)
        except Exception as mistake:
            log.info("MISTAKE")
            log.info(mistake.args)


# Main functions
main_window = Tk()
api_win = Api_Win()
main_window.geometry("1200x650")
main_window.resizable(0, 0)
main_window.title("Commutator Simulator")

# Input vars
input_text_sec = StringVar()
input_text_sec_in = StringVar()
input_sec_choose = StringVar()
input_sec_in = StringVar()
input_port_choose = StringVar()
output_sec_choose = StringVar()
output_port_choose = StringVar()

# Scroll Widgets
yscrollbar = Scrollbar(main_window)
yscrollbar.pack(side=LEFT, fill=Y)

# Frames Building
control_frame = Frame(
    main_window,
    width=250,
    height=500,
    bd=0,
    highlightbackground="black",
    highlightcolor="black",
    highlightthickness=1,
)
control_frame.pack(side=LEFT, fill=Y)
input_frame = Frame(
    main_window,
    width=750,
    height=100,
    bd=0,
    highlightbackground="black",
    highlightcolor="black",
    highlightthickness=1,
)
input_frame.pack(side=TOP, fill=X)
com_frame = Frame(main_window, width=750, height=500)
com_frame.pack(fill=BOTH)


# Creating Label
label_sections = Label(input_frame, text="Com_in_sec")
label_in_section = Label(input_frame, text="Sections")
label_control = Label(control_frame, text="Control_Panel")
label_in_com = Label(input_frame, text="Com_In")
label_in_sec = Label(input_frame, text="Sec")
label_in_port = Label(input_frame, text="Port_In")
label_out_sec = Label(input_frame, text="Com_Out")
label_out_port = Label(input_frame, text="Port_Out")

# Creating Input Widgets
sec_entry = Entry(input_frame, width=20, textvariable=input_text_sec)
com_in_sec_entry = Entry(input_frame, width=20, textvariable=input_text_sec_in)
sec_choose = Entry(input_frame, width=20, textvariable=input_sec_choose)
com_in_sec_choose = Entry(input_frame, width=20, textvariable=input_sec_in)
port_in_choose = Entry(input_frame, width=20, textvariable=input_port_choose)
com_out_in_choose = Entry(
    input_frame, width=20, textvariable=output_sec_choose
)
port_out_choose = Entry(input_frame, width=20, textvariable=output_port_choose)
results_calculate = Text(
    control_frame, height=10, width=30, yscrollcommand=yscrollbar.set
)
results = Text(
    control_frame, height=15, width=30, yscrollcommand=yscrollbar.set
)
yscrollbar.config(command=results.yview)
yscrollbar.config(command=results_calculate.yview)

# Control Buttons
build_button = Button(
    control_frame,
    text="Build",
    width=8,
    height=3,
    padx=3,
    pady=7,
    command=lambda: api_win.get_values(),
)
clear_button = Button(
    control_frame,
    text="Clear",
    width=8,
    height=3,
    padx=3,
    pady=7,
    command=lambda: api_win.remove_com(),
)
clear_button.config(state=DISABLED)
get_button = Button(
    control_frame,
    text="Calc",
    width=8,
    height=3,
    padx=3,
    pady=7,
    command=lambda: api_win.calculate(),
)
get_button.config(state=DISABLED)
add_con_button = Button(
    control_frame,
    text="Add_Con",
    width=8,
    height=3,
    padx=3,
    pady=7,
    command=lambda: api_win.add_connect(),
)
add_con_button.config(state=DISABLED)

# Adding of input elements

# Builds entries
label_sections.grid(row=0, column=0)
label_in_section.grid(row=1, column=0, padx=3, pady=3)
sec_entry.grid(row=0, column=1, columnspan=2, padx=3, pady=3)
com_in_sec_entry.grid(row=1, column=1, columnspan=2, padx=3, pady=3)

# Input Controls
label_in_com.grid(row=0, column=3, padx=20, pady=3)
label_in_sec.grid(row=2, column=0, padx=20, pady=3)
com_in_sec_choose.grid(row=0, column=4, columnspan=2, padx=3, pady=3)
sec_choose.grid(row=2, column=1, columnspan=2, padx=3, pady=3)
label_in_port.grid(row=0, column=6, padx=20, pady=3)
port_in_choose.grid(row=0, column=7, columnspan=2, padx=20, pady=3)

# Output controls
label_out_sec.grid(row=1, column=3, padx=20, pady=3)
com_out_in_choose.grid(row=1, column=4, columnspan=2, padx=3, pady=3)
label_out_port.grid(row=1, column=6, padx=3, pady=3)
port_out_choose.grid(row=1, column=7, columnspan=2, padx=3, pady=3)

# Control Panel
label_control.grid(row=0, column=1, padx=1, pady=20)
build_button.grid(row=1, column=0, padx=25)
clear_button.grid(row=1, column=1, padx=20)
get_button.grid(row=1, column=2, padx=20)
results_calculate.grid(
    row=3, column=0, columnspan=4, rowspan=3, padx=10, pady=10, sticky=W + E
)
results.grid(
    row=7, column=0, columnspan=4, rowspan=3, padx=10, pady=10, sticky=W + E
)
add_con_button.grid(row=2, column=1, padx=20)

main_window.mainloop()
