#!/bin/python3

# Globals for commutators

import json


class Const_For_Commutators:

    def __init__(self):
        IN = None
        OUT = None
        SECTIONS = None
        COMMUTATORS = None
        CONNECTIONS = None

    def aggregate_consts(self, file_to_read):
        with open(file_to_read) as json_file:
            data = json.load(json_file)
            self.IN = data["commutators"]["IN"]
            self.OUT = data["commutators"]["OUT"]
            self.IN_SECTIONS = data["commutators"]["IN_SECTION"]
            self.SECTIONS = data["commutators"]["SECTION"]
            self.COMMUTATORS = data["commutators"]["COMMUTATORS"]
            self.CONNECTIONS = data["connections"]["sections"]


class Address_Handler:
    """
    Addressing For Every Commutator
    """
    in_out_entries = ['in_zero', 'in_one', 'out_zero', 'out_one']
    address_format = ['section_nr', 'commutator_nr', 'interface_nr']
    section_type = ['in', 'middle', 'out']
