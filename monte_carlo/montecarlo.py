import random
import functools
import pylab
import logging as log
from algorithms.in_out_route import In_Out_Route

"""
Monte Carlo Decorator.
"""
log_aller = []


def log_giver():
    return log_aller


def log_all(*args, **kwargs):
    # TODO BETTER IMPORTS I AM NOOB
    log_list = []
    log.basicConfig(
        format="%(asctime)s - %(message)s",
        level=log.INFO,
        datefmt="%d-%b-%y %H:%M:%S",
    )
    log_data_str = [
        str(iner) + " " + str(outer)
        for iner, outer in zip(kwargs["y_in"], kwargs["y_or"])
    ]
    log.info("         IN   ORD")
    for counter, login in enumerate(log_data_str):
        log_to_log = str(counter) + " sample " + login + " y_in y_or"
        log_aller.append(log_to_log + "\n")
        log.info(log_to_log)
    return log_list


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
            fig = pylab.figure(figsize=(20, 10))
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
            log_all(y_in=y_plot_in, y_or=y_plot_or, x_data=x_plot)
            ax.plot(x_plot, y_plot_in, color="tab:red", label="Order algt")
            ax.plot(x_plot, y_plot_or, color="tab:blue", label="In_Out algt")
            legend = ax.legend(
                loc="lower center", shadow=True, fontsize="x-large"
            )
            legend.get_frame().set_facecolor("#eafff5")
            ax.set_ylim([0, 102])
            ax.set_xlabel("samples")
            ax.set_ylabel("percentage")
            ax.set_title("Success Percentage")
            ax.grid(True)
            pylab.show()

        return wrapper_decorator

    return monterepeater
