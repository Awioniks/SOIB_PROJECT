import random
import functools
from algorithms.division_route import In_Out_Route

"""
Monte Carlo Decorator
"""


def montedecorator(sim_num, com_in, consts, field):
    def random_list(com_in):
        p_out = [In_Out_Route.calculate(inc, False) for inc in range(com_in)]
        p_in = [In_Out_Route.calculate(inc, False) for inc in range(com_in)]
        random.shuffle(p_in)
        return {x: y for x, y in zip(p_out, p_in)}

    def monterepeater(func):
        def wrapper_decorator():
            count = 0
            while count < sim_num:
                func(field=field, consts=consts, perm_mc=random_list(com_in))
                count += 1
        return wrapper_decorator

    return monterepeater
