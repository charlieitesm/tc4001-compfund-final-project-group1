import unittest

from state_machine import State, StateMachine, StateMachineBuilder


class StateMachineBuilderTest(unittest.TestCase):

    def _verify_expected_sm(self, expected: StateMachine, actual: StateMachine):
        self.assertIsNotNone(actual, "Actual is None")
        self.assertEquals(expected.initial_state.state_id, actual.initial_state.state_id, "The initial State ID differs")
        self.assertTrue(actual.initial_state.is_initial, "The initial state is not marked as such")

        self.assertEquals(len(expected.heads), len(actual.heads), "Different number of heads")
        self.assertEquals(len(expected.states), len(actual.states), "Different number of states")

    def test_state_machine01(self):
        s0 = State("S0", is_initial=True, is_final=False)
        s1 = State("S1")
        s2 = State("S2")
        s3 = State("S3", is_final=True)

        s0.transitions["a"] = [s1]
        s1.transitions["a"] = [s2]
        s2.transitions["b"] = [s3]

        states = [s0, s1, s2, s3]

        expected = StateMachine(s0, states)
        actual = StateMachineBuilder.build_state_machine("resources/state_machine01.sm")

        self._verify_expected_sm(expected=expected, actual=actual)

        test_str = "aab"
        self.assertEquals(expected.is_string_valid(test_str), actual.is_string_valid(test_str))

        test_str = "a"
        self.assertEquals(expected.is_string_valid(test_str), actual.is_string_valid(test_str))


if __name__ == '__main__':
    unittest.main()
