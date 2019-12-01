#!/bin/python3

from .commutator import Commutator
from .commutator_globals import Address_Handler as ah


class Commutation_Field:
    """
    Commutation_Field Class
    """

    def __init__(self):
        """
        Comutation Field Constructor with empty commutators list
        """
        self.commutators = {}

    def add_commutator(self, section_nr, nr_in_section):
        """
        Method for adding new commutators to list
        """
        key = "{}_{}"
        commutator = Commutator(section_nr, nr_in_section)
        key = key.format(section_nr, nr_in_section)
        self.commutators[key] = commutator

    def set_addresses_of_commutator(self, identity, addresses):
        """
        Method for setting addresses in particular commutator
        according to his identity
        """
        if identity in self.commutators:
            for interface, address in addresses.items():
                ad_num = address.split("_")
                if len(ad_num) != 3:
                    ad_num = ["None" for count in range(3)]
                self.commutators[identity].set_addresses(interface, {ah.address_format[counter]: num for counter,
                                                                     num in enumerate(ad_num)})
    def show_com(self):
        """
        Show commutation field
        """
        for identity, com in self.commutators.items():
            print("identity: ", identity, " com ", com.addressing)

