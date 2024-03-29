from collections import defaultdict


class State:
    """
    Models a State in a state machine/automaton.

    A State is comprised of:
    1. An ID
    2. A flag to determine whether the state is initial or not
    3. A flag to determine whether the state is final or not
    4. A dict (map) of transitions where:
       a. The key is the symbol used to transition (including epsillon)
       b. The value is a list of references to States. In a DFA, this list must be of length 1 per symbol,
          but on NFAs this list can be of an arbitrary lenght >= 1, this is because one symbol can lead
          to more than one state
    """
    def __init__(self, state_id: str = None, is_initial: bool = False, is_final: bool = False):

        self.state_id = state_id
        self.is_initial = is_initial
        self.is_final = is_final
        self.transitions = defaultdict(lambda: [])

    def __str__(self):
        return "s{}".format(self.state_id)

    def __eq__(self, other):
        is_equal = self.state_id == other.state_id
        is_equal = is_equal and self.is_initial == other.is_initial
        is_equal = is_equal and self.is_final == other.is_final
        return is_equal

    def __lt__(self, other):
        if self.is_initial and other.is_initial:
            return self.state_id < other.state_id   # Tie breaker on the state ID

        elif self.is_initial and not other.is_initial:
            return True     # The initial state should stay at the beginning of the order

        elif not self.is_initial and other.is_initial:
            return False

        else:
            return self.state_id < other.state_id

    def __gt__(self, other):
        if self.is_final and other.is_final:
            return self.state_id > other.state_id  # Tie breaker on the state ID

        elif self.is_final and not other.is_final:
            return True  # The final state should stay at the end of the order

        elif not self.is_final and other.is_final:
            return False

        else:
            return self.state_id > other.state_id

    def __hash__(self):
        return id(self)


class Automaton:
    """
    An automaton or state machine.

    An automaton works much like a linked list would: It has an initial state from which we can transition
    to other states.

    It has a list of all the States, so that it can keep track of all of them at all times.

    It has a list of reading heads. A reading head is a pointer to the State in which the state machine is
    at any point in time. For DFA, this list will be of length 1 as there can only be one reading head at
    a time. For NFA, this list of heads may be bigger than one since a state can transition to one or more
    states at a time.

    The list of heads must always be initialized to a list with the initial_state only

    When traversing, the heads will be popped (in a stack-manner) and inspected to calculate all of the
    possible transitions.

    A string is recognized by the automata when, after processing each character in it, at least one head
    of the automata is pointing to a State that is a final state.

    """
    def __init__(self, states: list, initial_state: State = None):

        # No state must be null
        if not all(states):
            raise ValueError("The initial state or the states are None")

        # Being validation of states
        unique_state_ids = set()    # Each state must have a unique ID
        initial_state_found = []    # We should have only one initial state per automaton
        alphabet = set()            # The automaton should tell us all of the symbols in its alphabet
        for state in states:
            if not state.state_id:
                raise ValueError("A State was given an empty ID but it is mandatory!")

            state.state_id = state.state_id.upper()
            unique_state_ids.add(state.state_id)

            if state.is_initial:
                initial_state_found.append(state)

            # Add unique symbols to the alphabet
            for symbol in state.transitions.keys():
                alphabet.add(symbol)

        if len(unique_state_ids) < len(states):
            raise ValueError("More than one state has the same ID, they should be unique!")

        num_initial_states_found = len(initial_state_found)
        if num_initial_states_found != 1:
            raise ValueError("{} states found, but the Automaton must have 1 and only 1 initial state"
                             .format(num_initial_states_found))

        # We are good to continue building the Automaton
        self.initial_state = initial_state if initial_state is not None else initial_state_found[0]

        # Let's keep an order where the initial state is at the beginning and the final states at the end
        self.states = sorted(states)
        self.alphabet = tuple(sorted(alphabet))

        # The heads list will act more like a stack than a list. Python uses lists to simulate stacks too
        self.heads = [self.initial_state]

        # A Helper list that will allow us to reset the heads back to the start, once initialized, it should not be
        #  modified
        self._initial_heads = [self.initial_state]

    def is_string_valid(self, input_string: str) -> bool:
        # Reset the heads first
        self.heads = self._initial_heads.copy()

        string_queue = [c for c in input_string]

        while string_queue:
            symbol = string_queue.pop(0)
            current_head_count = len(self.heads)

            # Follow and transition for the current heads pointing to different states
            for i in range(current_head_count):
                head = self.heads.pop(0)
                new_states = head.transitions.get(symbol)

                if new_states:
                    # If there is a transition for the symbol, replace the head with the new list of states to follow,
                    #  for DFA this will be one state only, for NFA, they could be more than one state
                    self.heads.extend(new_states)

        return self._are_heads_in_accepting_states()

    def _are_heads_in_accepting_states(self):

        for head in self.heads:
            if head.is_final:
                return True

        return False
