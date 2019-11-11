from automata.state_machine import Automaton
from automata.state_machine import State


def minimize_automaton(input: Automaton) -> Automaton:
    # TODO: Implement me!
    pass


def nfa_2_dfa(input: Automaton) -> Automaton:
    """
           Function to convert from a non deterministic finite automaton to a deterministic one
     """
    states_list = []
    initial = State()
    existing_state = {}
    alphabet = get_alphabet(input)
    input = clean_epsilon_transition(input)
    states_queue = [input.initial_state]
    limbo_state = State(state_id='limbo')
    for symbol in alphabet:
        limbo_state.transitions[symbol] = [limbo_state]

    while len(states_queue) > 0:
        current_state = states_queue.pop(0)
        existing_state[current_state.state_id] = True
        for symbol in alphabet:
            to_state = State(state_id='')
            if current_state.transitions.get(symbol, None) is None:
                to_state.transitions[symbol].append(limbo_state)
                if not existing_state.get(limbo_state.state_id, False):
                    existing_state[limbo_state.state_id] = True
                    states_list.append(limbo_state)
            else:
                for transition in current_state.transitions[symbol]:
                    to_state.state_id += transition.state_id
                    to_state.is_final = to_state.is_final or transition.is_final
                    to_state.is_initial = to_state.is_initial or transition.is_initial

            current_state.transitions[symbol] = [to_state]
            if not existing_state.get(to_state.state_id, False):
                states_queue.append(to_state)

        states_list.append(current_state)
        if current_state.is_initial:
            initial = current_state

    return Automaton(initial_state=initial, states=states_list)


def clean_epsilon_transition(input: Automaton) -> Automaton:
    """
          Function to calculate the epsilon lock for each state, hence it removes all of the epsilon transitions from
          the automaton
    """
    reachable_states = {}

    for state in input.states:
        current_states = []
        next_states = []
        is_epsilon_connected = False
        reachable_states[state] = set()
        for value in state.transitions.get(' ', []):
            current_states.append(value)
            is_epsilon_connected = True

        while is_epsilon_connected:
            for current in current_states:
                for value in current.transitions.get(' ', []):
                    next_states.append(value)
                reachable_states[state].add(current)

            if len(next_states) > 0:
                current_states = next_states
                next_states = []
                print(next_states)
            else:
                break

    for state in input.states:
        for each in reachable_states[state]:
            state.transitions.update(each.transitions)
            if ' ' in state.transitions.keys():
                state.transitions.pop(' ')

    return input


def get_alphabet(input: Automaton) -> list:
    """
           Function to creates a unique set of the symbols of the alphabet being used in the automaton
     """
    alphabet = set()

    for state in input.states:
        for key in state.transitions.keys():
            alphabet.add(key)

    return list(alphabet)


def is_dfa(input: Automaton) -> bool:
    """
           function to check if a given automaton is deterministic or not
     """
    for state in input.states:
        for k, v in state.transitions.items():
            if len(v) != 1:
                return False

    return True


def are_equivalent(automatonA: Automaton, automatonB: Automaton) -> bool:
    # TODO: Implement me! This is a nice-to-have but we may want to implement it for
    #  verification purposes
    pass
