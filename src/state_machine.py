from collections import defaultdict


class State:
    def __init__(self, state_id: str = None, is_initial: bool = False, is_final: bool = False):
        self.state_id = state_id
        self.is_initial = is_initial
        self.is_final = is_final
        self.transitions = defaultdict(lambda: [])


class StateMachine:
    def __init__(self, initial_state: State, states: list):

        if not all([initial_state, *states]):
            raise ValueError("The initial state or the states are None")

        self.initial_state = initial_state
        self.states = states
        self.heads = [initial_state]
        self._initial_heads = [initial_state]

    def is_string_valid(self, candidate: str) -> bool:
        # Reset the heads first
        self.heads = self._initial_heads.copy()

        string_queue = [c for c in candidate]

        while string_queue:
            symbol = string_queue.pop(0)
            current_head_count = len(self.heads)

            # Follow and transition for the current heads pointing to different states
            for i in range(current_head_count):
                head = self.heads.pop(0)
                new_states = head.transitions.get(symbol)

                if new_states:
                    # Replace the head with the new list of states to follow, for DFA this will be one state only, for
                    #  NFA, they could be more than one state
                    self.heads.extend(new_states)

        return self._are_heads_in_accepting_states()

    def _are_heads_in_accepting_states(self):

        for head in self.heads:
            if head.is_final:
                return True

        return False


class StateMachineBuilder:
    @staticmethod
    def build_state_machine(file_location: str) -> StateMachine:
        pass
