#!/bin/python3

# main func making Commutation Field building

from argparse import ArgumentParser  # TODO remake for argparse
from algorithms.in_out_route import In_Out_Route as routing_in
from algorithms.order_route import Order_Route as order_route
from monte_carlo.montecarlo import montedecorator, log_giver
import commutation.commutator_globals as glob
import sys
import logging as log
import commutation.commutation_field as com

# SIMULATION NUMBER DEFAULT VALUE
SIM_NUM = 200


def main(file_to_read):
    """
    main func which build commutation field
    """
    log.basicConfig(format="%(asctime)s - %(message)s", level=log.INFO)
    log.info("START OF SIMULATION")
    consts = glob.Const_For_Commutators()
    consts.aggregate_consts(file_to_read)
    COM_IN = consts.IN
    com_field = com.Commutation_Field(consts)
    key = "{}_{}"
    log_list = []

    @montedecorator(
        sim_num=SIM_NUM, com_in=COM_IN, consts=consts, field=com_field,
    )
    def start_algorithms(*args, **kwargs):
        print(kwargs["perm_mc"], "KWWAAARRGS")
        routing_in.set_data(
            consts=kwargs["consts"],
            field=kwargs["field"],
            perm_mc=kwargs["perm_mc"],
        )
        report_routing_in = routing_in.route()
        order_route.set_data(
            consts=kwargs["consts"],
            field=kwargs["field"],
            perm_mc=kwargs["perm_mc"],
        )
        report_order = order_route.main_path_searcher(
            permutations=kwargs["perm_mc"]
        )
        return {"routing_in": report_routing_in, "report_order": report_order}

    for section_nr, connection in consts.CONNECTIONS.items():
        for nr_in_section, addresses in connection["commutator"].items():
            identity = key.format(section_nr, nr_in_section)
            com_field.add_commutator(section_nr, nr_in_section)
            com_field.set_addresses_of_commutator(identity, addresses)
    routing_in.set_data(consts=consts, field=com_field)
    start_algorithms()
    log_list = log_giver()
    return log_list


if __name__ == "__main__":
    file_to_read = sys.argv[1]
    main(file_to_read)
