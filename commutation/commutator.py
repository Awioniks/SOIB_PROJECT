#!/bin/python3

from .commutator_globals import Address_Handler as ah


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
