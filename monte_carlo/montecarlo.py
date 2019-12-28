import random
import functools
import pylab
from algorithms.in_out_route import In_Out_Route

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
            x_plot = []
            y_plot_in, y_plot_or = [], []
            fig = pylab.figure()
            ax = fig.add_subplot(1, 1, 1)
            while count < sim_num:
                report = func(
                    field=field, consts=consts, perm_mc=random_list(com_in)
                )
                x_plot.append(count)
                result_in = (
                    report["routing_in"]["success"]
                    / (
                        report["routing_in"]["success"]
                        + report["routing_in"]["failure"]
                    )
                ) * 100
                y_plot_in.append(result_in)
                y_plot_or.append(report["report_order"])
                count += 1
            ax.plot(x_plot, y_plot_in, color='tab:red')
            ax.plot(x_plot, y_plot_or, color='tab:blue')
            ax.set_ylim([0, 102])
            ax.set_xlabel("samples")
            ax.set_ylabel("percentage")
            ax.set_title("Success Percentage")
            ax.grid(True)
            pylab.show()

        return wrapper_decorator

    return monterepeater
