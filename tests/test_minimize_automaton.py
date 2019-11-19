import unittest

from tests.automata_examples import state_machine_1
from utils.automata_utils import automata_are_equivalent
from utils.minimizer import minimize_automaton


class MinimizedAutomataTest(unittest.TestCase):

    def test_minimized_dfa_1(self):
        """
        From a given DFA, we'll check if it is equivalent to the expected output
        """
        big_automaton, mini_automaton = state_machine_1()
        result = minimize_automaton(big_automaton)

        # In order to determine if two automata are the same, we can say that: if they are equivalent and they have the
        #  same number of states, then the two automata are, in fact, the same automata
        self.assertTrue(automata_are_equivalent(result, mini_automaton),
                        "Expected automaton is not equivalent to result automaton")
        self.assertEqual(len(mini_automaton.states), len(result.states))

    def test_already_minimized_dfa(self):
        """
        If we are to provide an already minimized DFA, the result should be the same DFA
        """
        _, mini_automaton = state_machine_1()
        result = minimize_automaton(mini_automaton)

        # In order to determine if two automata are the same, we can say that: if they are equivalent and they have the
        #  same number of states, then the two automata are, in fact, the same automata
        self.assertTrue(automata_are_equivalent(result, mini_automaton),
                        "Expected automaton is not equivalent to result automaton")
        self.assertEqual(len(mini_automaton.states), len(result.states))


if __name__ == '__main__':
    unittest.main()
