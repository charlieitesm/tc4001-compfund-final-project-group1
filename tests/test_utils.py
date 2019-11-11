import unittest

from automata.state_machine import Automaton
from utils.file_utils import deserialize_automaton, serialize_automaton, save_str_to_file


class MyTestCase(unittest.TestCase):

    # Test case when there are invalid uploads
    def test_error(self) -> None:
        with self.assertRaisesRegex(ValueError, 'The provided automata contains no initial or final state'):
            self.test_automaton = self.load_automaton("../resources/state_machine02.txt")

    # test calse to validate everything is ok
    def test_good_file(self) -> None:
        self.test_automaton = self.load_automaton("../resources/state_machine01.txt")
        self.assertTrue(self.test_automaton)

    # test to check initial
    def test_initial_only(self) -> None:
        self.test_automaton = self.load_automaton("../resources/state_machine01.txt")
        for state in self.test_automaton.states:
            if state.is_final and state.is_initial:
                self.assertNotEqual("q0", state.state_id)
            if state.is_initial and not state.is_final:
                self.assertEqual("q0", state.state_id)
            if state.is_final and not state.is_initial:
                self.assertEqual("q2", state.state_id)
            if not state.is_final and not state.is_initial:
                self.assertEqual("q1", state.state_id)

    # test to check final
    def test_final_only(self) -> None:
        self.test_automaton = self.load_automaton("../resources/state_machine01.txt")


    # test to check both initial and final
    def test_final_only(self) -> None:
        self.test_automaton = serialize_automaton(self.load_automaton("../resources/state_machine01.txt"))

    # test to check both initial and final
    def test_write_file(self) -> None:
        self.test_automaton = save_str_to_file('automata.txt',serialize_automaton(self.load_automaton("../resources/state_machine01.txt")))

    @staticmethod
    def load_automaton(file) -> Automaton:
        return deserialize_automaton(file)


if __name__ == '__main__':
    unittest.main()
