#!/bin/python3

# main func making Commutation Field building

from argparse import ArgumentParser
import sys
import commutation.commutation_field as com
from algorithms.in_out_route import In_Out_Route as routing_in
from algorithms.division_route import Division_Route as div
from monte_carlo.montecarlo import montedecorator
import commutation.commutator_globals as glob

# SIMULATION NUMBER DEFAULT VALUE
SIM_NUM = 20000000


def main(file_to_read):
    """
    main func which build commutation field
    """
    consts = glob.Const_For_Commutators()
    consts.aggregate_consts(file_to_read)
    COM_IN = consts.IN
    com_field = com.Commutation_Field(consts)
    key = "{}_{}"

    @montedecorator(
        sim_num=SIM_NUM, com_in=COM_IN, consts=consts, field=com_field
    )
    def start_algorithms(*args, **kwargs):
        routing_in.set_data(
            consts=kwargs["consts"],
            field=kwargs["field"],
            perm_mc=kwargs["perm_mc"],
        )
        report = routing_in.route()
        print(report)
        #div.hello()

    for section_nr, connection in consts.CONNECTIONS.items():
        for nr_in_section, addresses in connection["commutator"].items():
            identity = key.format(section_nr, nr_in_section)
            com_field.add_commutator(section_nr, nr_in_section)
            com_field.set_addresses_of_commutator(identity, addresses)
    routing_in.set_data(consts=consts, field=com_field)
    start_algorithms()


if __name__ == "__main__":
    file_to_read = sys.argv[1]
    main(file_to_read)
