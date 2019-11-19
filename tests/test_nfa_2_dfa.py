import unittest

from automata.state_machine import Automaton
from tests.automata_examples import state_machine_nfa_1, state_machine_nfa_2, state_machine_nfa_4
from utils.automata_utils import nfa_2_dfa, is_dfa, automata_are_equivalent


class NFA2DFATest(unittest.TestCase):

    def _check_validity_of_dfa(self, result: Automaton):
        """
        This is just a private helper function that allows the inspection of the DFA after the conversion.
        """
        self.assertIsNotNone(result)

        # Make sure that is_dfa
        self.assertTrue(is_dfa(result))

        # Let's verify that there is nothing wonky with the states, there should be one state for a given state ID only
        unique_state_ids = set([state.state_id for state in result.states])
        self.assertEqual(len(unique_state_ids), len(result.states), "The DFA has more than one state for a State ID!")

    def test_nfa_2_dfa_1(self):
        """
        This test will pass if:
        1. The DFA generated is not None
        2. If the DFA generated IS a DFA
        3. Given the result must be, by Moore's equivalent to an expected DFA that recognizes the same language

        The result doesn't need to be the minimized version.

        This tests relies on the correctness of the following functions, make sure those functions are also correct:
        1. is_dfa()
        2. automata_are_equivalent()
        """
        nfa, expected_dfa = state_machine_nfa_1()

        result = nfa_2_dfa(nfa)

        # Check that the characteristics of the DFA are correct
        self._check_validity_of_dfa(result)

        self.assertIsNotNone(result)
        # Make sure that is_dfa and automata_are_equivalent unit tests pass and that the function is correct
        #  or we'll get skewed results
        # Even if the result of the transformation is no the same automata, it should be equivalent by Moore
        self.assertTrue(automata_are_equivalent(result, expected_dfa))

    def test_nfa_2_dfa_2(self):
        """
        This test will pass if:
        1. The DFA generated is not None
        2. If the DFA generated IS a DFA
        3. Given the result must be, by Moore's equivalent to an expected DFA that recognizes the same language

        The result doesn't need to be the minimized version.

        This tests relies on the correctness of the following functions, make sure those functions are also correct:
        1. is_dfa()
        2. automata_are_equivalent()
        3. clean_epsilon_transitions()
        """
        nfa = state_machine_nfa_2()

        result = nfa_2_dfa(nfa)

        self._check_validity_of_dfa(result)

    def test_nfa_2_dfa_3(self):
        """
        This will test a 6-state NFA with no epsillon transitions that possess a known DFA and a minimized DFA
        """
        nfa = state_machine_nfa_4()
        result = nfa_2_dfa(nfa)

        self._check_validity_of_dfa(result)

        # This particular case, as we saw in the example in class, should output a non-minimized DFA with 9 states
        # 1 Initial
        # 4 Normal
        # 4 Final
        self.assertEqual(9, len(result.states))
        initial_states = []
        normal_states = []
        final_states = []

        for state in result.states:
            if state.is_initial:
                initial_states.append(state)
            elif state.is_final:
                final_states.append(state)
            else:
                normal_states.append(state)

        self.assertEqual(1, len(initial_states))
        self.assertEqual(4, len(normal_states))
        self.assertEqual(4, len(final_states))


if __name__ == '__main__':
    unittest.main()
