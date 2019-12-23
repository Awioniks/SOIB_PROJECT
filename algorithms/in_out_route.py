#!/bin/python3
from math import floor


class In_Out_Route:
    """
    Class which handle Imput and out routing algorithm
    for commutatos
    """

    @classmethod
    def set_data(cls, field, consts, perm_mc=None):
        """
        Set data which are required for routing
        """
        cls.consts = consts
        cls.field = field
        cls.section_loop = floor(consts.SECTIONS / 2) + 1
        if not perm_mc:
            cls.permutations = [
                (key, value) for key, value in consts.PERMUTATIONS.items()
            ]
        else:
            cls.permutations = [(key, value) for key, value in perm_mc.items()]

    @classmethod
    def look_for_permutation(cls, thing, permutations, key_or_value):
        """
        Look for value or key according to options
        """
        if key_or_value:
            for key, value in permutations:
                if key == thing:
                    return value
        else:
            for key, value in permutations:
                if value == thing:
                    return key

    @classmethod
    def insertion_sort_for_commutators(cls, permutations):
        """
        Insertion sort algorithm for ports in next iterations
        """
        for pair_counter in range(1, len(permutations)):
            next_pair_counter = 0
            key_first = cls.calculate(permutations[pair_counter][0], True)
            key_second = cls.calculate(permutations[pair_counter][1], True)
            while (
                key_first
                > cls.calculate(permutations[next_pair_counter][0], True)
                and next_pair_counter < pair_counter
            ):
                next_pair_counter += 1
            permutations.insert(
                next_pair_counter,
                (
                    cls.calculate(key_first, False),
                    cls.calculate(key_second, False),
                ),
            )
            del permutations[pair_counter + 1]
        return permutations

    @classmethod
    def set_addresses_in_commutator(
        cls, zero_layer, one_layer, section_counter
    ):
        """
        Set addresses inside commutators
        """
        key = "{}_{}"
        new_permutation = []
        is_zero_out_port = {"zero": True, "out": True}
        for (zero_layer_commutator, one_layer_commutator,) in zip(
            zero_layer, one_layer
        ):
            nr_com_left_zero, port_left_zero = zero_layer_commutator[0].split(
                "_"
            )

            nr_com_right_zero, port_right_zero = zero_layer_commutator[
                1
            ].split("_")
            nr_com_left_one, port_left_one = one_layer_commutator[0].split("_")
            nr_com_right_one, port_right_one = one_layer_commutator[1].split(
                "_"
            )

            identity = key.format(
                cls.consts.address_decoder[section_counter + 1],
                nr_com_left_zero,
            )

            is_zero_out_port["zero"] = True
            is_zero_out_port["out"] = True

            address_dict = cls.field.set_addresses_in_commutator_route_algt(
                is_zero_out_port, identity, port_left_zero
            )

            first_pair = (
                address_dict["commutator_nr"]
                + "_"
                + address_dict["interface_nr"]
            )

            right_counter = cls.consts.SECTIONS - section_counter

            identity = key.format(
                cls.consts.address_decoder[right_counter], nr_com_right_zero
            )

            is_zero_out_port["zero"] = True
            is_zero_out_port["out"] = False

            address_dict = cls.field.set_addresses_in_commutator_route_algt(
                is_zero_out_port, identity, port_right_zero
            )

            second_pair = (
                address_dict["commutator_nr"]
                + "_"
                + address_dict["interface_nr"]
            )

            new_permutation.append((first_pair, second_pair))
            identity = key.format(
                cls.consts.address_decoder[section_counter + 1],
                nr_com_left_one,
            )

            is_zero_out_port["zero"] = False
            is_zero_out_port["out"] = True

            address_dict = cls.field.set_addresses_in_commutator_route_algt(
                is_zero_out_port, identity, port_left_one
            )
            first_pair = (
                address_dict["commutator_nr"]
                + "_"
                + address_dict["interface_nr"]
            )

            identity = key.format(
                cls.consts.address_decoder[right_counter], nr_com_right_one
            )

            is_zero_out_port["zero"] = False
            is_zero_out_port["out"] = False

            address_dict = cls.field.set_addresses_in_commutator_route_algt(
                is_zero_out_port, identity, port_right_one
            )
            second_pair = (
                address_dict["commutator_nr"]
                + "_"
                + address_dict["interface_nr"]
            )
            new_permutation.append((first_pair, second_pair))
        return cls.insertion_sort_for_commutators(new_permutation)

    @classmethod
    def calculate(cls, com_port, from_to):
        """
        Calculate from string to number or adversely
        """
        if from_to:
            com, port = com_port.split("_")
            return (
                cls.consts.address_decoder[com] - 1
            ) * 2 + cls.consts.address_decoder[port]
        else:
            return (
                cls.consts.address_decoder[int(com_port / 2) + 1]
                + "_"
                + cls.consts.address_decoder[com_port % 2]
            )

    @classmethod
    def research(cls, mem=0, value=0):
        """
        research antother commutator if route()
        method get into infinite loop
        """
        return mem + 2 if value > mem else mem + 1

    @classmethod
    def algorithm_report(cls, perms):
        report = {"success": 0, "failure": 0}
        for perm in perms:
            permutation_key = perm[0].split("_")
            permutation_value = perm[1].split("_")
            if permutation_key[0] == permutation_value[0]:
                report["success"] += 1
            else:
                report["failure"] += 1
        return report

    @classmethod
    def route(cls):
        """
        route in commutators
        """
        section_counter = 0
        perm_dict_label_all = cls.permutations
        while section_counter < cls.section_loop:
            perm_dict_label_0, perm_dict_label_1 = (
                [],
                [],
            )
            counter_perm = 0
            referent_perm_key, referent_perm_value = perm_dict_label_all[0]
            perm_dict_label_0.append((referent_perm_key, referent_perm_value))
            while counter_perm < len(cls.permutations) - 1:
                if counter_perm % 2 == 0:
                    referent_perm_value_mem = referent_perm_value
                    referent_perm_value = (
                        cls.calculate(referent_perm_value, True) - 1
                        if cls.calculate(referent_perm_value, True) % 2 == 1
                        else cls.calculate(referent_perm_value, True) + 1
                    )
                    referent_perm_key = cls.look_for_permutation(
                        cls.calculate(referent_perm_value, False),
                        perm_dict_label_all,
                        False,
                    )

                    check_pair = (
                        referent_perm_key,
                        cls.calculate(referent_perm_value, False),
                    )

                    look_back_count = 0
                    for look_count in range(len(cls.permutations)):
                        if (
                            check_pair in perm_dict_label_1
                            or check_pair in perm_dict_label_0
                        ):
                            length = len(cls.permutations) - 1
                            if referent_perm_value == length:
                                look_back_count = look_count
                                referent_perm_value = 0
                            if look_count == 0:
                                referent_perm_value = cls.research(
                                    cls.calculate(
                                        referent_perm_value_mem, True
                                    ),
                                    referent_perm_value,
                                )
                            else:
                                referent_perm_value += (
                                    1 - look_back_count
                                )

                            referent_perm_key = cls.look_for_permutation(
                                cls.calculate(referent_perm_value, False),
                                perm_dict_label_all,
                                False,
                            )
                            check_pair = (
                                referent_perm_key,
                                cls.calculate(referent_perm_value, False),
                            )
                        else:
                            break
                    perm_dict_label_1.append(
                        (
                            referent_perm_key,
                            cls.calculate(referent_perm_value, False),
                        )
                    )
                    referent_perm_value = cls.calculate(
                        referent_perm_value, False
                    )
                else:
                    referent_perm_key_mem = referent_perm_key
                    referent_perm_key = (
                        cls.calculate(referent_perm_key, True) - 1
                        if cls.calculate(referent_perm_key, True) % 2 == 1
                        else cls.calculate(referent_perm_key, True) + 1
                    )
                    referent_perm_value = cls.look_for_permutation(
                        cls.calculate(referent_perm_key, False),
                        perm_dict_label_all,
                        True,
                    )

                    check_pair = (
                        cls.calculate(referent_perm_key, False),
                        referent_perm_value,
                    )
                    for look_count in range(len(cls.permutations)):
                        if (
                            check_pair in perm_dict_label_0
                            or check_pair in perm_dict_label_1
                        ):
                            length = len(cls.permutations) - 1
                            if referent_perm_key == length:
                                look_back_count = look_count
                                referent_perm_key = 0
                            if look_count == 0:
                                referent_perm_key = cls.research(
                                    cls.calculate(referent_perm_key_mem, True),
                                    referent_perm_key,
                                )
                            else:
                                referent_perm_key += (
                                    1 - look_back_count
                                )
                            referent_perm_value = cls.look_for_permutation(
                                cls.calculate(referent_perm_key, False),
                                perm_dict_label_all,
                                True,
                            )
                            check_pair = (
                                cls.calculate(referent_perm_key, False),
                                referent_perm_value,
                            )
                        else:
                            break
                    perm_dict_label_0.append(
                        (
                            cls.calculate(referent_perm_key, False),
                            referent_perm_value,
                        )
                    )
                    referent_perm_key = cls.calculate(referent_perm_key, False)
                counter_perm += 1

            if section_counter + 1 < cls.section_loop:
                perm_dict_label_all.clear()
                perm_dict_label_all.extend(
                    cls.set_addresses_in_commutator(
                        perm_dict_label_0, perm_dict_label_1, section_counter
                    )
                )
            else:
                perm_dict_label_0.extend(perm_dict_label_1)
                return cls.algorithm_report(perm_dict_label_0)
            section_counter += 1
