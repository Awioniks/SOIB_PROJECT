#!/bin/python3

from commutator_globals import Address_Handler as ah


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

    def set_addresses(self, address_list):
        """
        Set address for every commutator interface
        """
        for counter, addresses_dict in enumerate(address_list):
            interface = ah.in_out_entries[counter]
            self.addressing[interface] = addresses_dict
