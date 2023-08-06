from guide_bot.base_elements import guide_elements
from guide_bot.parameters import instrument_parameters as ipars


class Elliptic(guide_elements.GuideElement):
    """
    Elliptic GuideElement that inserts an elliptic section into a guide

    The elliptic guide needs to have start and end dimensions set to fit
    into the guide_bot logic, so the focal points are determined by these
    dimensions and the minor_axis in each direction. The minor_axis can be
    limited or specified as the normal Element parameters. In addition it
    is possible to set a maximum width / height of the element for cases
    where the guide has to fit within a narrow space. The minor axis can
    be greater than the maximum width of the guide, as only a segment of
    the full ellipse is simulated, and the minor axis might be outside
    that segment. If end_width or end_height is specified, they will
    override the  start_width or start_height setting of the next Element
    in the guide.
    """
    def __init__(self, name, length=None, start_point=None, start_width=None, start_height=None,
                 end_width=None, end_height=None, minor_axis_x=None, minor_axis_y=None,
                 max_width=None, max_height=None,  **kwargs):
        """
        Elliptic GuideElement that inserts an elliptic section into a guide

        The elliptic guide needs to have start and end dimensions set to fit
        into the guide_bot logic, so the focal points are determined by these
        dimensions and the minor_axis in each direction. The minor_axis can be
        limited or specified as the normal Element parameters. In addition it
        is possible to set a maximum width / height of the element for cases
        where the guide has to fit within a narrow space. The minor axis can
        be greater than the maximum width of the guide, as only a segment of
        the full ellipse is simulated, and the minor axis might be outside
        that segment. If end_width or end_height is specified, they will
        override the  start_width or start_height setting of the next Element
        in the guide.

        Parameters
        ----------
        name : str
            Name of the element

        length : (float, None, InstrumentParameter)
            Length of guide element, optimized parameter

        start_point : (float, None, InstrumentParameter)
            Distance from source to start of the gap element

        start_width : (float, None, InstrumentParameter)
            Width of the start of the gap

        start_height : (float, None, InstrumentParameter)
            Height of the start of the gap

        end_width : (float, None, InstrumentParameter)
            Width of the end of the gap

        end_height : (float, None, InstrumentParameter)
            Height of the end of the gap

        minor_axis_x : (float, None, InstrumentParameter)
            Minor axis of the full ellipse, horizontal direction

        minor_axis_y : (float, None, InstrumentParameter)
            Minor axis of the full ellipse, vertical direction

        max_width : float
            Maximum width of the inserted guide segment

        max_height : float
            Maximum height of the inserted guide segment
        """
        # Internalize stuff relevant for this module
        self.minor_axis_x = guide_elements.handle_input_parameter(name + "_minor_axis_x", minor_axis_x,
                                                                  default_min=0.005, default_max=0.3)

        self.minor_axis_y = guide_elements.handle_input_parameter(name + "_minor_axis_y", minor_axis_y,
                                                                  default_min=0.005, default_max=0.3)

        # max_width is the upper limit for minor axis, which is not true, it should be upper limit
        #  for the actual width of the guide segment which can be much smaller for e.g. a parabola

        self.max_width = max_width
        self.max_height = max_height

        super().__init__(name, length=length, start_point=start_point,
                         start_width=start_width, start_height=start_height,
                         end_width=end_width, end_height=end_height,
                         **kwargs)

        # temporary reflectivity model
        if "R0" in kwargs:
            self.R0 = kwargs["R0"]
        else:
            self.R0 = 0.99

        if "Qc" in kwargs:
            self.Qc = kwargs["Qc"]
        else:
            self.Qc = 0.0217

        if "alpha" in kwargs:
            self.alpha = kwargs["alpha"]
        else:
            self.alpha = 6.07

        if "m" in kwargs:
            self.m = kwargs["m"]
        else:
            self.m = 1.0

        if "W" in kwargs:
            self.W = kwargs["W"]
        else:
            self.W = 0.003

        if "enableGravity" in kwargs:
            self.enableGravity = kwargs["enableGravity"]
        else:
            self.enableGravity = 1

    def add_to_instr(self):
        """
        Adds code describing the elliptic element to the current McStas instrument

        This methods uses McStasScript to add components and code to a McStas
        instrument object. The McStas instrument object is an attribute of the
        class called current_instrument. New instrument parameters can also be
        created and added to the optimization by using the current_parameters
        attribute.

        Since the add_to_instr method of all the Elements are called in order
        from the sample to the source, it is important the components are
        added after the Origin component to ensure the correct order.
        """

        # Need to add minor_axis_x and y to parameter pool
        self.current_parameters.add_parameter(self.minor_axis_x)
        self.current_parameters.add_parameter(self.minor_axis_y)

        # Add constraints ensuring that minor axis is wider than both start and end
        # If the user has set both minor_axis and a dimension with the same userdefined parameter, they will
        #  be equal, and thus the constraint is not needed. Furthermore, it would be a floating point rounding
        #  that determines whether the constraint is fulfilled or not, causing problems.
        if not self.minor_axis_x is self.start_width:
            self.current_parameters.add_new_constraint([self.minor_axis_x, self.start_width], lambda x, y: abs(x) - y)
        if not self.minor_axis_x is self.end_width:
            self.current_parameters.add_new_constraint([self.minor_axis_x, self.end_width], lambda x, y: abs(x) - y)

        if not self.minor_axis_y is self.start_height:
            self.current_parameters.add_new_constraint([self.minor_axis_y, self.start_height], lambda x, y: abs(x) - y)
        if not self.minor_axis_y is self.end_height:
            self.current_parameters.add_new_constraint([self.minor_axis_y, self.end_height], lambda x, y: abs(x) - y)

        # When minor_axis_x is negative, the minor axis is outside, and the widest point is the largest entry/exit
        # When minor_axis_y is positive, the minor axis is inside, and the widest point is the small axis
        if self.max_width is not None:
            self.current_parameters.add_new_constraint(self.start_width, lambda x, a: a - x, constants=self.max_width)
            self.current_parameters.add_new_constraint(self.end_width, lambda x, a: a - x, constants=self.max_width)
            self.current_parameters.add_new_constraint(self.minor_axis_x, lambda x, a: a - x, constants=self.max_width)

        if self.max_height is not None:
            self.current_parameters.add_new_constraint(self.start_height, lambda x, a: a - x, constants=self.max_height)
            self.current_parameters.add_new_constraint(self.end_height, lambda x, a: a - x, constants=self.max_height)
            self.current_parameters.add_new_constraint(self.minor_axis_y, lambda x, a: a - x, constants=self.max_height)

        # Instruct instrument to calculate length and get name
        length_name = self.get_length_name()

        instr = self.current_instrument

        # Calculate ellipse parameters in McStas instrument
        instr.add_declare_var("double", "tmp_w1")
        instr.add_declare_var("double", "tmp_w2")
        instr.append_initialize('')
        instr.append_initialize('tmp_w1=' + self.start_width.name + ';')
        instr.append_initialize('tmp_w2=' + self.end_width.name + ';')

        instr.add_declare_var("double", "tmp_b")
        instr.add_declare_var("double", "tmp_L")
        instr.append_initialize('tmp_b=fabs(0.5*' + self.minor_axis_x.name + ');')
        instr.append_initialize('tmp_L=' + length_name + ';')

        instr.add_declare_var("double", "tmp_k")
        instr.append_initialize('if (' + self.minor_axis_x.name + ' > 0) {')
        instr.append_initialize('tmp_k=cos(asin(tmp_w2/(2*tmp_b)))/cos(asin(tmp_w1/(2*tmp_b)));')
        instr.append_initialize('} else {')
        instr.append_initialize('tmp_k=cos(asin(tmp_w2/(2*tmp_b)))/cos(PI-asin(tmp_w1/(2*tmp_b)));')
        instr.append_initialize('}')

        instr.add_declare_var("double", "tmp_L1")
        instr.add_declare_var("double", "tmp_L2")
        instr.append_initialize('tmp_L1=tmp_L/(1+tmp_k);')
        instr.append_initialize('tmp_L2=tmp_L-tmp_L1;')

        instr.add_declare_var("double", "tmp_c")
        instr.append_initialize('if (' + self.minor_axis_x.name + ' > 0) {')
        instr.append_initialize('tmp_c=cos(asin(tmp_w1/(2*tmp_b)))*cos(asin(tmp_w1/(2*tmp_b)));')
        instr.append_initialize('} else {')
        instr.append_initialize('tmp_c=cos(PI-asin(tmp_w1/(2*tmp_b)))*cos(PI-asin(tmp_w1/(2*tmp_b)));')
        instr.append_initialize('}')

        Linx_par_name = self.name + "_Linx"
        Loutx_par_name = self.name + "_Loutx"
        instr.add_declare_var("double", Linx_par_name)
        instr.add_declare_var("double", Loutx_par_name)
        instr.append_initialize(Linx_par_name + '=-tmp_L1+sqrt(tmp_L1*tmp_L1*(1/tmp_c)-tmp_b*tmp_b);')
        instr.append_initialize(Loutx_par_name + '=' + Linx_par_name + '+tmp_L1-tmp_L2;')

        instr.append_initialize('')
        instr.add_declare_var("double", "tmp_h1")
        instr.add_declare_var("double", "tmp_h2")
        instr.append_initialize('tmp_h1=' + self.start_height.name + ';')
        instr.append_initialize('tmp_h2=' + self.end_height.name + ';')

        instr.append_initialize('tmp_b=fabs(0.5*' + self.minor_axis_y.name + ');')
        instr.append_initialize('tmp_L=' + length_name + ';')

        instr.append_initialize('if (' + self.minor_axis_y.name + ' > 0) {')
        instr.append_initialize('tmp_k=cos(asin(tmp_h2/(2*tmp_b)))/cos(asin(tmp_h1/(2*tmp_b)));')
        instr.append_initialize('} else {')
        instr.append_initialize('tmp_k=cos( asin(tmp_h2/(2*tmp_b)))/cos(PI-asin(tmp_h1/(2*tmp_b)));')
        instr.append_initialize('}')

        instr.append_initialize('tmp_L1=tmp_L/(1+tmp_k);')
        instr.append_initialize('tmp_L2=tmp_L-tmp_L1;')

        instr.append_initialize('if (' + self.minor_axis_y.name + ' > 0) {')
        instr.append_initialize('tmp_c=cos(asin(tmp_h1/(2*tmp_b)))*cos(asin(tmp_h1/(2*tmp_b)));')
        instr.append_initialize('} else {')
        instr.append_initialize('tmp_c=cos(PI-asin(tmp_h1/(2*tmp_b)))*cos(PI-asin(tmp_h1/(2*tmp_b)));')
        instr.append_initialize('}')

        Liny_par_name = self.name + "_Liny"
        Louty_par_name = self.name + "_Louty"
        instr.add_declare_var("double", Liny_par_name)
        instr.add_declare_var("double", Louty_par_name)
        instr.append_initialize(Liny_par_name + '=-tmp_L1+sqrt(tmp_L1*tmp_L1*(1/tmp_c)-tmp_b*tmp_b);')
        instr.append_initialize(Louty_par_name + '=' + Liny_par_name + '+tmp_L1-tmp_L2;')

        # Add the guide component and use the calculated variables for its properties
        guide = self.current_instrument.add_component(self.name, "Elliptic_guide_gravity", after="Origin")
        guide.set_AT([0, 0, self.start_point_parameter.name])

        guide.l = length_name

        guide.linxw = Linx_par_name
        guide.loutxw = Loutx_par_name
        guide.linyh = Liny_par_name
        guide.loutyh = Louty_par_name

        guide.dimensionsAt = '"mid"'
        guide.xwidth = self.minor_axis_x.name
        guide.yheight = self.minor_axis_y.name

        # Temporary reflectivity model
        guide.R0 = self.R0
        guide.m = self.m
        guide.Qc = self.Qc
        guide.alpha = self.alpha
        guide.W = self.W
        guide.enableGravity = self.enableGravity

