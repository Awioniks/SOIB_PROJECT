#!/bin/python3


class Commutator:
    """
    Commutator Class
    """

    def __init__(self, commutator_nr=None, section_nr=None):
        """
        Constructor of commutator class init with id and
        empty addressing dict
        """
        self.id = (commutator_nr, section_nr)
        self.addressing = {}
        self.in_addressing = {}

    def set_addresses(self, interface, address_dict):
        """
        Set address for every commutator interface
        """
        self.addressing[interface] = address_dict

    def set_in_addresses(self, port_in, port_out, is_out):
        """
        Set ports inside commutator and return connected interface
        """
        direction = None
        if is_out:
            direction = "out" + "_" + port_out
            self.in_addressing[port_in] = port_out
        else:
            direction = "in" + "_" + port_out
            self.in_addressing[port_out] = port_in
        print(direction)
        print(self.addressing[direction])
        return self.addressing[direction]
