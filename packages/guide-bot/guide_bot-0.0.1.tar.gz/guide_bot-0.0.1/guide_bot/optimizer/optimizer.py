import os
import pyswarm

import numpy as np

from mcstasscript.interface import instr, functions, plotter


class RunInfo:
    """
    Container for information from a single optimization step

    Saves the optimizer state and figure of merit from a step in the
    optimization.
    """
    def __init__(self, optimized_x, fom):
        self.optimized_x = optimized_x
        self.fom = fom


class History:
    """
    Container for RunInfo instances for each step in the optimization

    Keeps a history of optimizer states and figure of merits organized in
    RunInfo instances.
    """
    def __init__(self):
        """
        Starts a history container
        """
        self.histories = []
    
    def add_run_info(self, optimized_x, fom):
        """
        Appends information to the history

        Parameters
        ----------

        optimized_x : list
            Optimizer state, list of values for each free parameter

        fom : float
            Figure of merit attained by optimized_x state
        """
        self.histories.append(RunInfo(optimized_x, fom))


def optimizer_func(optimizer_x, *args, **kwargs):
    """
    Optimizer function for swarm algorithm, calculates fom with simulation

    The optimizer function is responsible for calculating the figure of merit
    given an optimizer state. The figure of merit is returned from a McStas
    simulation of the guide performed with McStasScript. Access to the
    necessary objects are provided through the keyword arguments. The used
    SWAM algorithm still evaluates the fom when the constraints are not
    satisfied, in these cases a figure of merit of 0 is returned to avoid
    running simulations that may not succeed due to meaningless input. The
    optimizer state and returned figure of merit is saved to the history.

    Parameters
    ----------

    optimized_x : list
        Optimizer state, list of values for each free parameter

    Keyword arguments
    -----------------

    instrument : McStasScript instrument object
        Instrument object that describe the guide to be optimized

    instrument_parameters : InstrumentParameterContainer
        Parameters and constraints for the optimization

    settings : dict
        Dictionary with settings, ncount and optimized monitor
    """
    instrument = kwargs["instrument"]
    instr_parameters = kwargs["instrument_parameters"]
    settings = kwargs["settings"]

    instr_parameter_input = instr_parameters.extract_instrument_parameters(optimizer_x)
    print(instr_parameters)

    constraint_values = instr_parameters.evaluate_constraints()

    if np.min(constraint_values) < 0.0:
        print(" -- Returned 0 for fom due to unfulfilled constraints! -- ")
        return 0.0

    print("Running with \n", instr_parameter_input)

    sim_data = instrument.run_full_instrument(foldername=settings["foldername"],
                                              increment_folder_name=True, force_compile=False,
                                              parameters=instr_parameter_input, ncount=settings["ncount"])

    remove_data_folder(settings["foldername"])

    optimizer_data = functions.name_search(settings["optimized_monitor"], sim_data)

    fom = -np.sum(np.sum(optimizer_data.Intensity))
    print("  fom =", fom)

    if not isinstance(fom, float):
        print("Warning! FOM not a float!")
    
    kwargs["history"].add_run_info(optimizer_x, fom)
    
    return fom

def remove_data_folder(path):
    """
    Safe remove function that will only delete folders that do not contain
    folders, lowers risk of deleting wrong data.
    """

    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    os.rmdir(path)


def optimizer_f_ieqcons(optimizer_x, *args, **kwargs):
    """
    Constraint function for SWARM algorithm

    The constraint function returns a list of values, if any of these are
    negative the constraints are not satisfied.

    Parameters
    ----------

    optimizer_x : list
        Optimizer state, list of values for each free parameter
    """
    instr_parameters = kwargs["instrument_parameters"]
    return instr_parameters.evaluate_constraints(optimizer_x)


def run_optimizer(instrument, my_parameters, settings):
    """
    Performs optimization of given instrument with parameters and settings

    The given instrument must have input parameters corresponding to all
    parameters in the my_parameters. The limits and constraints for the
    parameters are included in the InstrumentParameterContainer, and so this
    defines the optimization. As each step is a Monte Carlo simulation of the
    guide, there is some noise in the signal, so a SWARM optimizer was
    selected due to their resiliance to such nosy signals. Since the
    compilation of McStas instruments can take a significant amount of time,
    compile is just performed once and then disabled for the subsequent steps.

    Parameters
    ----------

    instrument : McStasScript instrument object
        Instrument object that describe the guide to be optimized

    my_parameters : InstrumentParameterContainer
        Parameters and constraints for the optimization

    settings : dict
        Dict with options for the optimization
    """
    instrument.write_full_instrument()

    if my_parameters.get_N_free_parameters() == 0:
        print("No free parameters, optimization skipped.")
        return []

    lb = my_parameters.get_lower_bounds()
    ub = my_parameters.get_upper_bounds()

    my_history = History()

    kw_package = {"instrument": instrument, "instrument_parameters": my_parameters,
                  "settings": settings, "history": my_history}

    xopt, fopt = pyswarm.pso(optimizer_func, lb, ub, f_ieqcons=optimizer_f_ieqcons, kwargs=kw_package,
                             swarmsize=settings["swarmsize"], omega=settings["omega"], phip=settings["phip"],
                             phig=settings["phig"], maxiter=settings["maxiter"], minstep=settings["minstep"],
                             minfunc=settings["minfunc"], debug=False)

    print("-"*50, "done", "-"*50)
    print(xopt)
    print(fopt)

    print("-"*50, "showing history", "-"*50)
    lowest_fom = 1
    lowest_fom_pars = None
    for history in my_history.histories:
        instrument_pars = my_parameters.extract_instrument_parameters(history.optimized_x)
        print(history.fom, "\tFrom this set:", instrument_pars)
        if history.fom < lowest_fom:
            lowest_fom = history.fom
            lowest_fom_pars = instrument_pars

    print("-"*50, "best from history", "-"*50)
    print("Best fom: ", lowest_fom)
    print("From parameters", lowest_fom_pars)

    print("Retrying with these parameters")
    sim_data = instrument.run_full_instrument(foldername=settings["foldername"],
                                              increment_folder_name=True,
                                              parameters=lowest_fom_pars, ncount=settings["ncount"],
                                              force_compile=False)

    optimizer_data = functions.name_search(settings["optimized_monitor"], sim_data)
    fom = -np.sum(np.sum(optimizer_data.Intensity))
    print("redone fom", fom)
    print("fom in optimization: ", lowest_fom)
    print("ratio = ", fom/lowest_fom)

    print("For par file:")
    for key in lowest_fom_pars:
        print(key + "=" + str(lowest_fom_pars[key]))

    return xopt

    # General call
    #xopt, fopt = pyswarm.pso(func, lb, ub, ieqcons=[], f_ieqcons=None, args=(), kwargs={},
    #                         swarmsize=100, omega=0.5, phip=0.5, phig=0.5, maxiter=100, minstep=1e-8,
    #                         minfunc=1e-8, debug=False)
