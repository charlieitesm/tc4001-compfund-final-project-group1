import unittest

from automata.state_machine import Automaton
from utils.file_utils import deserialize_automaton


class MyTestCase(unittest.TestCase):

    # Test case when there are invalid uploads
    def test_error(self) -> None:
        with self.assertRaisesRegex(ValueError, 'The provided automata contains no initial or final state'):
            self.test_automaton = self.load_automaton("../resources/state_machine02.txt")

    # test calse to validate everything is ok
    def test_good_file(self) -> None:
        self.test_automaton = self.load_automaton("../resources/state_machine01.txt")
        self.assertTrue(self.test_automaton)

    @staticmethod
    def load_automaton(file) -> Automaton:
        return deserialize_automaton(file)


if __name__ == '__main__':
    unittest.main()
