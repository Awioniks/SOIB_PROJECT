#!/bin/python3
from algorithms.in_out_route import In_Out_Route
from collections import defaultdict


class Order_Route(In_Out_Route):
    """
    Class which handle Order route algorithms.
    """

    @classmethod
    def set_data(cls, field, consts, perm_mc=None):
        """
        Set data which are required for routing.
        """
        super().set_data(field, consts, perm_mc)
        cls.section_loop = consts.SECTIONS
        cls.path_list = list()
        cls.success_counter = 0
        cls.failure_counter = 0

    @classmethod
    def main_path_searcher(cls, permutations=None):
        """
        Main path searcher which look path for every
        commutator.
        """
        for perm in cls.permutations:
            path_creator = cls.look_for_path(perm=perm, section_counter=0)
            potential_list_of_paths = list()
            for dicter in path_creator:
                keys = [key for key in dicter.keys()]
                data = keys[0].split("_")
                com = perm[1].split("_")
                if com[0] == data[2]:
                    potential_list_of_paths.append(dicter)

            if len(potential_list_of_paths) == 0:
                cls.failure_counter += 1
            elif cls.add_path(path_lister=potential_list_of_paths):
                cls.success_counter += 1
            else:
                cls.failure_counter += 1
        return (
            cls.success_counter / (cls.success_counter + cls.failure_counter)
        ) * 100

    @classmethod
    def change_direction(cls, path):
        sec_counter = 0
        list_we_look = list()
        while sec_counter < cls.section_loop - 1:
            for key in path:
                list_we_look.append(key)
                path = path[key]
            sec_counter += 1
            if sec_counter == cls.section_loop - 1:
                list_we_look.append(path)
                break
        return list_we_look

    @classmethod
    def choose_the_best_path(cls, paths):
        the_best_path_in_dict = paths[0]
        the_best_path = cls.change_direction(paths[0])
        for path in paths:
            path_in_dict = path
            path = cls.change_direction(path)
            counter = len(the_best_path)
            while counter > 0:
                best_nums = path[counter - 1].split("_")
                nums = the_best_path[counter - 1].split("_")
                best_num = cls.consts.address_decoder[best_nums[3]]
                num = cls.consts.address_decoder[nums[3]]
                if num < best_num:
                    the_best_path = path
                    the_best_path_in_dict = path_in_dict
                    break
                counter -= 1
        cls.path_list.append(the_best_path_in_dict)

    @classmethod
    def add_path(cls, path_lister):
        """
        Add new path to path list and check if they intersect other
        paths.
        """
        sec_counter = 0
        next_dict = None
        next_dict_list = None
        is_found = True
        temporary_list = list()

        if len(cls.path_list) == 0:
            for path in path_lister:
                temporary_list.append(path)
            cls.choose_the_best_path(temporary_list)
            return True

        for path in path_lister:
            found_path = path
            is_found = True
            for path_check in cls.path_list:
                while sec_counter < cls.section_loop - 1:
                    for key, key_ in zip(path, path_check):
                        if key == key_:
                            is_found = False
                            break
                        next_dict_list = path_check[key_]
                        next_dict = path[key]
                    if not is_found:
                        break
                    path = next_dict
                    path_check = next_dict_list
                    sec_counter += 1
                    if sec_counter == cls.section_loop - 1:
                        if path == path_check:
                            is_found = False
                        path = found_path
                        break
                sec_counter = 0
                if not is_found:
                    break
            if is_found:
                temporary_list.append(found_path)
        if len(temporary_list) == 0:
            return False
        else:
            cls.choose_the_best_path(temporary_list)
            return True

    @classmethod
    def look_for_path(cls, perm=None, section_counter=None, path_creator=None):
        """
        Look for path inside commutation field.
        """
        tree = lambda: defaultdict(tree)
        keys = ["out_zero", "out_one"]
        if section_counter == 0:
            path_new_list = list()
            first_com_address = perm[0].split("_")
            start_com = (
                "_"
                + cls.consts.address_decoder[section_counter + 1]
                + "_"
                + perm[0]
                + "_"
            )
            identity = (
                cls.consts.address_decoder[section_counter + 1]
                + "_"
                + first_com_address[0]
            )

            for key in cls.consts.in_out_entries:
                if key in keys:
                    path_creator = tree()
                    address_format = ""
                    for address in cls.consts.address_format:
                        address_format += (
                            "_"
                            + cls.field.commutators[identity].addressing[key][
                                address
                            ]
                        )
                    address_format += "_"
                    path_creator[address_format] = start_com
                    path_new_list.append(path_creator)
        else:
            path_new_list = list()
            for path_creator_new in path_creator:
                for next_sec, prev_sec in path_creator_new.items():
                    dict_next = {next_sec: prev_sec}
                    sections = next_sec.split("_")
                    identity = sections[1] + "_" + sections[2]
                    for interface in cls.consts.in_out_entries:
                        path_creator_new_dict = tree()
                        if interface in keys:
                            address_format = ""
                            for address in cls.consts.address_format:
                                address_format += (
                                    "_"
                                    + cls.field.commutators[
                                        identity
                                    ].addressing[interface][address]
                                )
                            address_format += "_"
                            path_creator_new_dict[address_format] = dict_next
                            path_new_list.append(path_creator_new_dict)
        section_counter += 1
        if section_counter != cls.section_loop:
            path_creator = cls.look_for_path(
                section_counter=section_counter, path_creator=path_new_list
            )
        return path_creator
