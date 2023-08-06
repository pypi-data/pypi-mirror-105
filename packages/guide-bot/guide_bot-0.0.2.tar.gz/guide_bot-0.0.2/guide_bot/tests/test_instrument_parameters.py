import io
import unittest
import unittest.mock

from guide_bot.parameters.instrument_parameters import InstrumentParameter
from guide_bot.parameters.instrument_parameters import FreeInstrumentParameter
from guide_bot.parameters.instrument_parameters import FixedInstrumentParameter
from guide_bot.parameters.instrument_parameters import DependentInstrumentParameter


class TestInstrumentParameters(unittest.TestCase):

    def test_basic_InstrumentParameter(self):
        """
        Testing a InstrumentParameter can be made and manipulated
        """

        A = InstrumentParameter("test_par")
        self.assertEqual(A.name, "test_par")

        A.set_category("testing")
        self.assertEqual(A.category, "testing")

        A.value = 29
        A.clear()
        self.assertEqual(A.value, None)

        string = A.__repr__() # ensure __repr__ doesnt fail

    def test_Basic_FreeInstrumentParameter(self):
        """
        Testing basic properties of FreeInstrumentParameter class
        """

        free = FreeInstrumentParameter("test_free", -0.2, 1.2)

        self.assertEqual(free.lower_bound, -0.2)
        self.assertEqual(free.upper_bound, 1.2)
        self.assertEqual(free.value, None)

        limits = free.get_limits()
        self.assertEqual(limits[0], -0.2)
        self.assertEqual(limits[1], 1.2)

        self.assertEqual(free.get_lower_bound(), -0.2)
        self.assertEqual(free.get_upper_bound(), 1.2)

        string = free.__repr__()  # ensure __repr__ doesnt fail

    def test_Value_FreeInstrumentParameter(self):
        """
        Testing basic properties of FreeInstrumentParameter class
        """

        free = FreeInstrumentParameter("test_free", None, 1.2)

        self.assertEqual(free.lower_bound, None)
        self.assertEqual(free.upper_bound, 1.2)
        self.assertEqual(free.get_value(), None)
        self.assertEqual(free.ready_for_optimization(), False)

        free.set_value(1.1)
        self.assertEqual(free.get_value(), 1.1)

        free.clear()
        self.assertEqual(free.get_value(), None)

    def test_eq_FreeInstrumentParameter(self):
        """
        Testing basic properties of FreeInstrumentParameter class
        """

        free1 = FreeInstrumentParameter("test_free", None, 1.2)
        free2 = FreeInstrumentParameter("test_free", None, 1.2)

        self.assertEqual(free1, free2)

        free2.set_value(1.0)

        self.assertEqual(free1, free2)

        free2.upper_bound = 0.0

        self.assertNotEqual(free1, free2)

    def test_Basic_FixedInstrumentParameter(self):
        """
        Testing basic properties of FixedInstrumentParameter class
        """

        fixed = FixedInstrumentParameter("test_fixed", 3.0)

        self.assertEqual(fixed.get_value(), 3.0)

        fixed.clear()  # Fixed parameters ignores clear

        self.assertEqual(fixed.get_value(), 3.0)

        string = fixed.__repr__()  # ensure __repr__ doesnt fail

    def test_Basic_DependentInstrumentParameter(self):
        """
        Testing basic properties of DependentInstrumentParameter class

        Using a free and fixed parameter as dependents
        """

        free = FreeInstrumentParameter("test_free", -0.2, 1.2)
        free.set_value(0.5)

        fixed = FixedInstrumentParameter("test_fixed", 3.0)

        dependent = DependentInstrumentParameter("test_dependent", [free, fixed],
                                                 lambda x,y : 2*x + y)

        self.assertEqual(dependent.get_value(), None)
        self.assertTrue(dependent.depends_on_free())

        dependent.calculate()

        self.assertEqual(dependent.get_value(), 4.0)

        string = dependent.__repr__()  # ensure __repr__ doesnt fail

    def test_no_free_DependentInstrumentParameter(self):
        """
        Testing DependentInstrumentParameter with fixed dependents
        """

        fixed1 = FixedInstrumentParameter("test_fixed", 5.0)
        fixed2 = FixedInstrumentParameter("test_fixed", 3.0)

        dependent = DependentInstrumentParameter("test_dependent", [fixed1, fixed2],
                                                 lambda x, y: x - y)

        self.assertEqual(dependent.get_value(), None)
        self.assertFalse(dependent.depends_on_free())

        dependent.calculate()

        self.assertEqual(dependent.get_value(), 2.0)

    def test_Constant_DependentInstrumentParameter(self):
        """
        Testing DependentInstrumentParameter with the constants keyword argument
        """

        free = FreeInstrumentParameter("test_free", -0.2, 1.2)
        free.set_value(0.5)

        fixed = FixedInstrumentParameter("test_fixed", 3.0)

        dependent = DependentInstrumentParameter("test_dependent", [free, fixed],
                                                 lambda x, y, a, b: 2*x + y*a + b,
                                                 constants=[4.0, -1.0])

        self.assertEqual(dependent.get_value(), None)
        self.assertTrue(dependent.depends_on_free())

        dependent.calculate()

        self.assertEqual(dependent.get_value(), 12.0)

    def test_dependent_DependentInstrumentParameter(self):
        """
        Testing DependentInstrumentParameter dependent on another dependent
        """

        fixed1 = FixedInstrumentParameter("test_fixed", 5.0)
        fixed2 = FixedInstrumentParameter("test_fixed", 3.0)

        dependent = DependentInstrumentParameter("test_dependent", [fixed1, fixed2],
                                                 lambda x, y: x - y)

        free = FreeInstrumentParameter("new_free", 0.0, 1.0)
        free.set_value(100)

        dep_dep = DependentInstrumentParameter("dep_dep", [free, dependent],
                                               lambda x, y: x - 10*y)

        self.assertEqual(dep_dep.get_value(), None)
        self.assertTrue(dep_dep.depends_on_free())

        dep_dep.calculate()

        self.assertEqual(dep_dep.get_value(), 80.0)






