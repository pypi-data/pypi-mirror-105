def make_list(input):
    """
    Utility function to ensure input is a list even with single entry
    """
    if not isinstance(input, list):
        return [input]
    else:
        return input


class InstrumentParameter:
    """
    Base class for all types of instrument parameters

    Classes derived from InstrumentParameter can be included both in the
    McStas instrument and guide_bot optimization logic. They are also used in
    constraints of the optimization. A InstrumentParameterContainer is defined
    in instrument_parameter_container.py, and an instance of this is used to
    keep all parameters which will be used by both optimizer and McStas.
    """
    def __init__(self, name):
        """
        Base initialization of InstrumentParameter with parameter name

        The InstrumentParameter is initialized with a str for its name. A
        value is initialized as None, meaning it has not been set yet. The
        category can be set to identify the origin of the parameter.

        Parameters
        ----------

        name : str
            Name of the parameter
        """
        self.name = name
        self.value = None
        self.category = None

    def clear(self):
        """
        Clears the stored value in the InstrumentParameter object.
        """

        self.value = None
    
    def calculate(self):
        """
        A calculation method needs to be provided by the derived class.
        """
        pass

    def get_value(self):
        """
        A get value method needs to be provided by the derived class, and
        should return the value of the InstrumentParameter.
        """
        print("Calling base class get_value! Problem!")

    def set_category(self, category):
        """
        Sets category for parameter

        Parameters
        ----------

        category : str
            Category describing the origin of the parameter
        """
        self.category = category


class FreeInstrumentParameter(InstrumentParameter):
    """
    Description of a Free parameter to be optimized within bounds

    A FreeInstrumentParameter is initialized with a upper and lower bound,
    which can each be None, yet have to be set before the parameter is used
    for actual optimization.
    """
    def __init__(self, name, lower_bound, upper_bound):
        """
        Initialization of FreeInstrumentParameter with name and bounds

        A free parameter can be used by the optimizer module, and will be
        optimized within the range given by the bounds. It is added to the
        container class that descripes a set of parameters, ensuring they
        are defined in the McStas instrument and are optimized while
        satisfying the constraints.

        Parameters
        ----------

        name : str
            Name of the FreeInstrumentParameter

        lower_bound : float
            Lower bound of valid interval for the parameter

        upper_bound : float
            upper bound of valid interval for the parameter
        """

        super().__init__(name)

        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
    
    def set_value(self, value):
        """
        Sets the value of the FreeInstrumentParameter (temporarily)

        Parameters
        ----------

        value : float
            Value for the free parameter for this optimization step
        """

        self.value = value
    
    def get_value(self):
        """
        Retrieves the stored value in the FreeInstrumentParameter

        Returns the value of the parameter used in this optimization step

        Returns
        -------

        value : float
            Value for the free parameter for this optimization step
        """

        return self.value

    def get_limits(self):
        """
        Returns a list with the lower and upper limit of allowed interval

        Returns
        -------

        list
            Lower bound and upper bound in list
        """
        return [self.lower_bound, self.upper_bound]
    
    def get_lower_bound(self):
        """
        Returns the lower limit of the allowed interval for this parameter

        Returns
        -------

        float
            Lower bound for allowed parameter interval
        """
        return self.lower_bound
        
    def get_upper_bound(self):
        """
        Returns the upper limit of the allowed interval for this parameter

        Returns
        -------

        float
            Upper bound for allowed parameter interval
        """
        return self.upper_bound

    def ready_for_optimization(self):
        """
        Returns True if both upper and lower bound have been set

        Returns
        -------

        bool
            Whether or not the FreeInstrumentParameter has well defined bounds

        """
        if self.lower_bound is not None and self.upper_bound is not None:
            if self.lower_bound > self.upper_bound:
                raise RuntimeError("Larger lower bound detected in " + self.name)

            return True
        else:
            return False

    def __eq__(self, other):
        """
        Override equals operator for FreeInstrumentParameter

        Returns
        -------

        bool
            True if two objects have same name and limits, False otherwise
        """

        if not isinstance(other, FreeInstrumentParameter):
            return False

        if not self.name == other.name:
            return False

        if not self.upper_bound == other.upper_bound:
            return False

        if not self.lower_bound == other.lower_bound:
            return False

        return True

    def __repr__(self):
        """
        Returns string descriping this FreeInstrumentParameter
        """

        string = "Free parameter:      "
        if self.category is None:
            string += " "*15
        else:
            string += self.category + " "*(15-len(self.category))
        string += str(self.name) + " "
        if self.value is None:
            string += "which was not set"
        else:
            string += "with value set to " + str(self.value)
        
        string += " [" + str(self.lower_bound) + ", "
        string += str(self.upper_bound) + "]"

        return string


class FixedInstrumentParameter(InstrumentParameter):
    """
    Description of fixed parameter that still needs to be tracked

    Even though the FixedInstrumentParameter is not optimized, it is still
    important as it can be used in constraints and calculations to be
    performed both in python and the McStas instrument file for each step in
    the optimization.
    """
    def __init__(self, name, value):
        """
        Sets the name and value for a fixed parameter

        Initialization of a FixedInstrumentParameter requires a name and a
        value, that can not be changed.

        Parameters
        ----------

        name : str
            Name of the FixedInstrumentParameter

        value : float
            Value associated with the FixedInstrumentParameter
        """
        super().__init__(name)
        self.value = value

    def get_value(self):
        """
        Return the value stored in the FixedInstrumentParameter.
        """

        return self.value
    
    def clear(self):
        """
        Clear method is overridden to ensure the fixed value is not removed.
        """

        # Since the value is fixed, remove capability of clearing
        pass

    def __repr__(self):
        """
        Returns a string describing this fixed parameter
        """

        string = "Fixed parameter:     "
        if self.category is None:
            string += " " * 15
        else:
            string += self.category + " " * (15 - len(self.category))
        string += str(self.name) + " "
        string += " with value " + str(self.value)

        return string


class DependentInstrumentParameter(InstrumentParameter):
    """
    The DependentInstrumentParameter can be calculated from other InstrumentParameters

    This class describes parameters that depend on other parameters, and can
    be calculated with a provided function. The function can also include
    constant values. There is no limit to the number of other parameters or
    constants that the function can depend on, but the inputs has to be
    ordered such that the parameters preceed the constants.
    """
    def __init__(self, name, dependent_on, dependent_function, constants=[]):
        """
        Creates an InstrumentParameter that depends on other parameters

        A DependentInstrumentParameter is using a supplied function to
        evaluate its value at every step in an optimization before it is being
        supplied to the McStas instrument. It can depend on any number of
        other InstrumentParameters, and they don't have to be in a container
        together in order to function. A DependentInstrumentParameter is
        allowed to depend on other DependentInstrumentParameters. Constants
        can also be used in the function, these must just be something that
        has a value when optimization happens. The function needs to have a
        number of inputs corresponding to the total InstrumentParameters and
        constants given, and the order is all InstrumentParameters first, then
        all constants.

        Parameters
        ----------

        name : str
            Name of the FreeInstrumentParameter

        dependent_on : list of InstrumentParameters
            List of InstrumentParameter objects that this parameter depends on

        dependent_function : func
            Function that takes inputs equal to dependent_on + constants

        constants : list of values
            List of values that will be used as constants in the function
        """
        super().__init__(name)
    
        # todo: check dependent_on is a instrument_parameter
        self.dependent_on = make_list(dependent_on)
        
        self.constants = make_list(constants)
        
        # todo: check dependent_function is a function
        self.dependent_function = dependent_function

    def get_value(self):
        """
        Gets the value stored in the object, but does not calculate it

        Returns
        -------
        float
            Value stored in object

        """
        #if self.value is None:
        #    raise ValueError("Calculate dependent value before getting!")
    
        return self.value

    def calculate(self):
        """
        Attempts to calculate the value for the DependentInstrumentParameter

        This method is recursive in the sense that it attempts to calculate
        the value for all InstrumentParameters that this InstrumentParameter
        depends on. If some of them can not be calculated yet, the method
        will exit early. Since it will be attempted to calculate all
        DependentInstrumentParameters, at some point it will succeed and get
        all the value attributes updated.
        """
    
        if self.value is not None:
            return self.value
    
        dependent_values = []
        for dependent in self.dependent_on:
            dependent.calculate()

        for dependent in self.dependent_on:
            returned_value = dependent.get_value()
            if returned_value is None:
                # Unable to calculate this parameter
                return
            
            dependent_values.append(returned_value)
            
        for constant in self.constants:
            dependent_values.append(constant)
        
        try:
            self.value = self.dependent_function(*dependent_values)
        except:
            self.value = self.dependent_function(dependent_values)
            if isinstance(self.value, list):
                self.value = self.value[0]

    def depends_on_free(self):
        """
        Check if this parameter depends on any free parameters

        Returns
        -------

        bool
            True if a FreeInstrumentParameter is in dependent, even recursively
        """
        for dependent in self.dependent_on:
            if isinstance(dependent, FreeInstrumentParameter):
                return True
            elif isinstance(dependent, DependentInstrumentParameter):
                if dependent.depends_on_free():
                    return True

        return False

    def __repr__(self):
        """
        Returns string describing this DependentInstrumentParameter

        Returns
        -------

        str
            String describing this DependentInstrumentParameter
        """
        string = "Dependent parameter: "
        if self.category is None:
            string += " " * 15
        else:
            string += self.category + " " * (15 - len(self.category))
        string += str(self.name) + " "
        if self.value is None:
            string += "which was not calculated"
        else:
            string += "with value set to " + str(self.value)
        string += "\n   dependent on: "
        for dependent in self.dependent_on:
            string += str(dependent.name) + " "

        return string
