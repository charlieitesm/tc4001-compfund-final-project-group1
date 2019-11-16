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


if __name__ == '__main__':
    unittest.main()
