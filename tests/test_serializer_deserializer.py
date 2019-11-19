import unittest

from tests.automata_examples import state_machine_1
from utils.automata_utils import automata_are_equivalent
from utils.file_utils import deserialize_automaton


class TestSerializer(unittest.TestCase):
    def test_dfa(self):
        automata1, _ = state_machine_1()
        result = deserialize_automaton("./resources/state_machine03.txt")

        self.assertEqual(len(automata1.states), len(result.states))
        self.assertTrue(automata_are_equivalent(automata1, result))


if __name__ == '__main__':
    unittest.main()
