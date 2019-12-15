#!/bin/python3

# Globals for commutators

import json


class Const_For_Commutators:
    def __init__(self):
        self.IN = None
        self.OUT = None
        self.SECTIONS = None
        self.COMMUTATORS = None
        self.CONNECTIONS = None
        self.PERMUTATIONS = None
        self.in_out_entries = ["in_zero", "in_one", "out_zero", "out_one"]
        self.address_format = ["section_nr", "commutator_nr", "interface_nr"]
        self.section_type = ["in", "middle", "out"]
        self.address_decoder = {
            0: "zero",
            1: "one",
            2: "two",
            3: "three",
            4: "four",
            5: "five",
            6: "six",
            7: "seven",
            8: "eight",
            9: "nine",
            10: "ten",
            "zero": 0,
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
            "ten": 10,
        }

    def aggregate_consts(self, file_to_read):
        with open(file_to_read) as json_file:
            data = json.load(json_file)
            self.IN = data["commutators"]["IN"]
            self.OUT = data["commutators"]["OUT"]
            self.IN_SECTIONS = data["commutators"]["IN_SECTION"]
            self.SECTIONS = data["commutators"]["SECTION"]
            self.COMMUTATORS = data["commutators"]["COMMUTATORS"]
            self.CONNECTIONS = data["connections"]["sections"]
            self.PERMUTATIONS = data["permutation"]["commutators"]
