import unittest

from state_machine import Automaton, State


class AutomatonTest(unittest.TestCase):

    def setUp(self) -> None:
        self.under_test = self.build_test_state_machine()

    def test_acceptedValue(self):
        result = self.under_test.is_string_valid("aab")
        self.assertTrue(result)

    def test_notAcceptedValues(self):
        test_str = "bba"
        result = self.under_test.is_string_valid(test_str)
        self.assertFalse(result)

        test_str = "a"
        result = self.under_test.is_string_valid(test_str)
        self.assertFalse(result)

        test_str = "b"
        result = self.under_test.is_string_valid(test_str)
        self.assertFalse(result)

    @staticmethod
    def build_test_state_machine() -> Automaton:
        s0 = State("S0", is_initial=True, is_final=False)
        s1 = State("S1")
        s2 = State("S2")
        s3 = State("S3", is_final=True)

        s0.transitions["a"] = [s1]
        s1.transitions["a"] = [s2]
        s2.transitions["b"] = [s3]

        states = [s0, s1, s2, s3]

        return Automaton(states)

    def test_comparing_of_states(self):
        s1 = State("1", is_initial=True)
        s2 = State("2")
        s3 = State("3")
        s4 = State("4", is_final=True)
        s5 = State("5", is_final=True)

        self.assertFalse(s1 == s2)
        clone = State("1", is_initial=True)

        # Even though they are different objects, they represent the same state
        self.assertFalse(s1 is clone)
        self.assertTrue(s1 == clone)

        self.assertTrue(s1 < s2)
        self.assertTrue(s2 > s1)
        self.assertTrue(s2 < s3)
        self.assertTrue(s3 > s2)
        self.assertTrue(s3 < s4)
        self.assertTrue(s4 > s3)
        self.assertTrue(s1 < s4)
        self.assertFalse(s1 > s4)
        self.assertTrue(s4 < s5)
        self.assertFalse(s4 > s5)

    def test_ordering_of_states(self):
        s1 = State("1", is_initial=True, is_final=True)
        s2 = State("2")
        s3 = State("3")
        s4 = State("4", is_final=True)
        s5 = State("5", is_final=True)

        states = [s5, s4, s3, s2, s1]
        ordered = sorted(states)

        self.assertIsNotNone(ordered)
        self.assertTrue(ordered[0] is s1)
        self.assertTrue(ordered[1] is s2)
        self.assertTrue(ordered[2] is s3)
        self.assertTrue(ordered[3] is s4)
        self.assertTrue(ordered[4] is s5)


if __name__ == '__main__':
    unittest.main()
