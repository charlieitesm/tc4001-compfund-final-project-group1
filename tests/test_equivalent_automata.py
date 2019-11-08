import unittest

from automata_examples import state_machine_1, state_machine_2, state_machine_3
from automata_utils import automata_are_equivalent, states_are_compatible
from state_machine import State


class EquivalentAutomataTest(unittest.TestCase):

    def test_equivalent_automaton_1(self):
        """
        From a given DFA, we'll check if it is equivalent to the expected output using Moore's
        """
        big_automaton, mini_automaton = state_machine_1()

        # An automaton is equivalent to itself and to its minimized version
        self.assertTrue(automata_are_equivalent(big_automaton, big_automaton))
        self.assertTrue(automata_are_equivalent(big_automaton, mini_automaton))
        self.assertTrue(automata_are_equivalent(mini_automaton, mini_automaton))

    def test_equivalent_automaton_2(self):
        """
        From a given DFA, we'll check if it is equivalent to the expected output using Moore's
        """
        big_automaton, mini_automaton = state_machine_2()

        # An automaton is equivalent to itself and to its minimized version
        self.assertTrue(automata_are_equivalent(big_automaton, big_automaton))
        self.assertTrue(automata_are_equivalent(big_automaton, mini_automaton))
        self.assertTrue(automata_are_equivalent(mini_automaton, mini_automaton))

    def test_non_equivalent_automata(self):
        big_1, mini_1 = state_machine_1()
        big_2, mini_2 = state_machine_2()

        result = automata_are_equivalent(big_1, big_2)
        self.assertIsNotNone(result)
        self.assertFalse(result)

        result = automata_are_equivalent(big_1, mini_2)
        self.assertIsNotNone(result)
        self.assertFalse(result)

        result = automata_are_equivalent(mini_1, mini_2)
        self.assertIsNotNone(result)
        self.assertFalse(result)

        result = automata_are_equivalent(mini_1, big_2)
        self.assertIsNotNone(result)
        self.assertFalse(result)

    def test_non_equivalent_automata_different_symbols(self):
        automaton_1, _ = state_machine_2()
        automaton_2, _ = state_machine_3()

        result = automata_are_equivalent(automaton_1, automaton_2)
        self.assertIsNotNone(result)
        self.assertFalse(result)

        result = automata_are_equivalent(automaton_2, automaton_1)
        self.assertIsNotNone(result)
        self.assertFalse(result)

    def test_compatible_states(self):
        # Compatible state are those that, given a pair, both are a final state or a reject state
        #  In other words, if one is final and the other isn't, they are incompatible
        s1 = State("1")
        s2 = State("2")

        result = states_are_compatible(s1, s2)
        self.assertIsNotNone(result)
        self.assertTrue(result)

        s1 = State("1", is_final=True)
        s2 = State("2", is_final=True)

        result = states_are_compatible(s1, s2)
        self.assertIsNotNone(result)
        self.assertTrue(result)

        # Negative cases

        s1 = State("1", is_final=True)
        s2 = State("2")

        result = states_are_compatible(s1, s2)
        self.assertIsNotNone(result)
        self.assertFalse(result)

        s1 = State("1")
        s2 = State("2", is_final=True)

        result = states_are_compatible(s1, s2)
        self.assertIsNotNone(result)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
