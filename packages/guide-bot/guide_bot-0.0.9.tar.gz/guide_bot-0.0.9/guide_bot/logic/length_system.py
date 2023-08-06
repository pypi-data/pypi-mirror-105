from guide_bot.base_elements import guide_elements
from guide_bot.base_elements import element_group as groups
from guide_bot.parameters import instrument_parameters as ipars


def length_system(elements, total_length, instrument_parameters):
    """
    System for handling length of each element with given constraints

    A total length from source to sample is given, along with a number of
    elements, each with their own constraints on starting distance from the
    source and length of the element. Some constraints are in the form of a
    fixed starting point or a fixed length, others as a range of allowed
    values. This function takes these constraints into account and adds a
    lower number of free parameters to the instrument_parameter container,
    describing the problem in terms of change points between each element.
    These change points have ranges, and constraints are imposed on that
    correspond to the constraints provided by the user. The algorithm is not
    yet able to clearly identify when an impossible problem is given.

    Parameters
    ----------

    elements : list of Element objects
        The elements describing this guide

    total_length : float
        The distance from source to sample along the guide

    instrument_parameters : InstrumentParameterContainer
        Parameter container where parameters can be added for optimization
    """
    # expect a list of elements, if not make it one
    if not isinstance(elements, list):
        elements = [elements]

    elements[0].start_point = ipars.FixedInstrumentParameter("start_point", 0.0)

    element_groups = [groups.ElementGroup()]

    # Last element free
    for element in elements:
        # Add this element to the current group
        element_groups[-1].add_element(element)
        if isinstance(element.length, ipars.FreeInstrumentParameter):  # Assume not dependent
            # If the current element has a free length, start new group
            element_groups.append(groups.ElementGroup())

    # Remove last group if it is empty
    if len(element_groups[-1].elements) == 0:
        element_groups.pop(-1)

    # Convert last group to start point if it has no free length
    last_group = element_groups[-1]
    if not last_group.has_free:
        last_group.fix_start_in_last_group(total_length)

    # Restrict min and max for groups from other fixed points
    last_fixed = 0
    for element_group in element_groups:
        if element_group.group_min_start is None:
            element_group.group_min_start = last_fixed

        if element_group.group_start is not None:
            last_fixed = element_group.group_start + element_group.group_fixed_length

    next_fixed = total_length
    for element_group in reversed(element_groups):
        if element_group.group_max_start is None:
            element_group.group_max_start = next_fixed

        if element_group.group_start is not None:
            next_fixed = element_group.group_start

    # Restrict min and max start for groups based on other min / max lengths
    last_element_group = None
    for element_group in element_groups:
        if last_element_group is not None:
            if last_element_group.group_start is not None:
                if last_element_group.group_min_length is not None:
                    new_min_start = last_element_group.group_start + last_element_group.group_min_length
                    if element_group.group_min_start is None:
                        element_group.group_min_start = new_min_start
                    elif new_min_start > element_group.group_min_start:
                        element_group.group_min_start = new_min_start

                if last_element_group.group_max_length is not None:
                    new_max_start = last_element_group.group_start + last_element_group.group_max_length
                    if element_group.group_max_start is None:
                        element_group.group_max_start = new_max_start
                    elif new_max_start < element_group.group_max_start:
                        element_group.group_max_start = new_max_start

        last_element_group = element_group

    next_element_group = None
    for element_group in reversed(element_groups):

        if next_element_group is not None:
            if next_element_group.group_start is not None:
                if element_group.group_min_length is not None:
                    new_max_start = next_element_group.group_start - element_group.group_min_length
                    if element_group.group_max_start is None:
                        element_group.group_max_start = new_max_start
                    elif new_max_start < element_group.group_max_start:
                        element_group.group_max_start = new_max_start

                if element_group.group_max_length is not None:
                    new_min_start = next_element_group.group_start - element_group.group_max_length
                    if element_group.group_min_start is None:
                        element_group.group_min_start = new_min_start
                    elif new_min_start > element_group.group_min_start:
                        element_group.group_min_start = new_min_start

        next_element_group = element_group

    # Export the information in element_groups to the instrument parameters
    for element_group in element_groups:
        element_group.export_to_pars(instrument_parameters)

    # Add the change point for guide to sample at the end at the sample location
    par = ipars.FixedInstrumentParameter("sample_cp", total_length)
    par.set_category("sample")
    instrument_parameters.add_parameter(par)
    elements[-1].next_start_point_parameter = par  # last element told sample pos

    # Assign next_start_point to each
    previous_element = None
    for element in elements:
        if previous_element is not None:
            previous_element.next_start_point_parameter = element.start_point_parameter
        previous_element = element

    # Add constraints for change points being in order and max / min length
    for element in elements:
        this_cp = element.start_point_parameter
        next_cp = element.next_start_point_parameter

        # Add constraint on element n being before n +1
        instrument_parameters.add_new_constraint([this_cp, next_cp],
                                                 lambda a, b: b - a - 1E-6)

        # Add constraint on max_length
        if isinstance(element.length, ipars.FreeInstrumentParameter):
            if element.length.get_lower_bound() is not None:
                func = lambda a, b, min_length: b - a - min_length
                instrument_parameters.add_new_constraint([this_cp, next_cp], func,
                                                         constants=element.length.get_lower_bound())

            # Add constraint on min_length
            if element.length.get_upper_bound() is not None:
                func = lambda a, b, max_length: -(b - a - max_length)
                instrument_parameters.add_new_constraint([this_cp, next_cp], func,
                                                         constants=element.length.get_upper_bound())


import matplotlib.pyplot as plt

def plot_change_points(elements, instrument_parameters):
    """
    Takes calculated instrument parameters with only change points
    """
    fig, ax = plt.subplots()

    cb_index = 0
    for par in instrument_parameters.all_parameters:
    
        if cb_index < len(elements):
            describing_string = elements[cb_index].__repr__()# + "\n length = " + length_string
        else:
            describing_string = ""
    
        if isinstance(par, ipars.FreeInstrumentParameter):
            value = par.get_value()
            if value is not None:
                ax.plot(cb_index, value, marker=".", color="blue")
                ax.text(cb_index, value, describing_string, ha="left", va="bottom", rotation=45)
            
            interval = [par.get_lower_bound(), par.get_upper_bound()]
            ax.plot([cb_index, cb_index], interval, color="blue")
    
        if isinstance(par, ipars.FixedInstrumentParameter):
            ax.plot(cb_index, par.get_value(), marker=".", color="red")
            ax.text(cb_index, par.get_value(), describing_string, ha="left", va="bottom", rotation=45)
            
        if isinstance(par, ipars.DependentInstrumentParameter):
            par.calculate()
            ax.plot(cb_index, par.get_value(), marker=".", color="purple")
            ax.text(cb_index, par.get_value(), describing_string, ha="left", va="bottom", rotation=45)

        cb_index += 1

    plt.show()


