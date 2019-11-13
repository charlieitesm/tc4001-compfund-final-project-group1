import unittest

from automata_examples import state_machine_nfa_1
from automata_utils import nfa_2_dfa, is_dfa, automata_are_equivalent


class NFA2DFATest(unittest.TestCase):

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

        self.assertIsNotNone(result)
        # Make sure that is_dfa and automata_are_equivalent unit tests pass and that the function is correct
        #  or we'll get skewed results
        self.assertTrue(is_dfa(result))
        # Even if the result of the transformation is no the same automata, it should be equivalent by Moore
        self.assertTrue(automata_are_equivalent(result, expected_dfa))


if __name__ == '__main__':
    unittest.main()
