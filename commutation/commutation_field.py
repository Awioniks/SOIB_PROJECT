#!/bin/python3

from commutator import Commutator
from commutator_globals import Address_Handler as ah

class Commutation_Field:
    """
    Commutation_Field Class
    """

    def __init__(self):
        """
        Comutation Field Constructor with empty commutators list
        """
        self.commutators = []

    def add_commutator(self, section_nr, nr_in_section):
        """
        Method for adding new commutators to list
        """
        commutator = Commutator(section_nr, nr_in_section)
        self.comutators.append(commutator)

    def set_addresses_of_commutator(self, identity, addresses):
        """
        Method for setting addresses in particular commutator
        according to his identity
        """
        for com in self.commutators:
            if identity == com.id:
                addresses_list = []
                for address in addresses:
                    ad_num = address.split("_")
                    address_list.append({ah.address_format[counter] : num for counter,
                            num in enumerate(ad_num)})
                com.set_adresses(addresses_list)
                break
