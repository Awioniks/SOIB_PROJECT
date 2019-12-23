import random
import functools
import pylab
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
            x_plot = []
            y_plot = []
            while count < sim_num:
                report = func(
                    field=field, consts=consts, perm_mc=random_list(com_in)
                )
                x_plot.append(count)
                result = (
                    report["success"] / (report["success"] + report["failure"])
                ) * 100
                y_plot.append(result)
                count += 1
            pylab.plot(x_plot, y_plot)
            pylab.show()

        return wrapper_decorator

    return monterepeater
