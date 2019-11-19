import unittest

from tests.automata_examples import *
from utils.automata_utils import is_dfa


class EquivalentAutomataTest(unittest.TestCase):

    def test_is_dfa_positive(self):
        """
        A DFA is one that has one and only one transition for all of the symbols (excluding epsillon) in the alphabet.
        """

        # A DFA and its minimized version must be DFA
        big_automaton, mini_automaton = state_machine_1()
        self.assertTrue(is_dfa(big_automaton))
        self.assertTrue(is_dfa(mini_automaton))

        big_automaton, mini_automaton = state_machine_2()
        self.assertTrue(is_dfa(big_automaton))
        self.assertTrue(is_dfa(mini_automaton))

        # We only have the minimized DFA for cases 3 and 4

        _, mini_automaton = state_machine_3()
        self.assertTrue(is_dfa(mini_automaton))

        _, mini_automaton = state_machine_4()
        self.assertTrue(is_dfa(mini_automaton))

    def test_is_not_dfa(self):
        error_msg = "An NFA was determined to be a DFA!"

        # Case 1 doesn´t contain epsillon transitions but case 2 does
        # We are ignoring the equivalent DFA that the state_machine_nfa functions return
        nf_automaton, _ = state_machine_nfa_1()
        result = is_dfa(nf_automaton)
        self.assertIsNotNone(result)
        self.assertFalse(result, error_msg)

        nf_automaton = state_machine_nfa_2()
        result = is_dfa(nf_automaton)
        self.assertIsNotNone(result)
        self.assertFalse(result, error_msg)

        # The following looks like a DFA, but it is a NFA because it has epsillon transitions
        nf_automaton = state_machine_nfa_3()
        result = is_dfa(nf_automaton)
        self.assertIsNotNone(result)
        self.assertFalse(result, error_msg + " One with epsillon transitions!")


if __name__ == '__main__':
    unittest.main()
