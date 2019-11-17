from collections import deque

from automata.state_machine import Automaton, State


def nfa_2_dfa(input: Automaton) -> Automaton:
    """
           Function to convert from a non deterministic finite automaton to a deterministic one
     """
    states_list = []
    existing_state = {}
    alphabet = get_alphabet(input)
    if ' ' in alphabet:
        input = clean_epsilon_transition(input)
        alphabet.remove(' ')
    states_queue = [input.initial_state]
    limbo_state = State(state_id='limbo')
    for symbol in alphabet:
        limbo_state.transitions[symbol] = [limbo_state]

    while len(states_queue) > 0:
        current_state = states_queue.pop(0)
        existing_state[current_state.state_id] = True
        for symbol in alphabet:
            to_state = State(state_id='')
            for id in current_state.state_id.split('-'):
                for node in input.states:
                    if id == node.state_id:
                        element = node
                        break
                if element.transitions.get(symbol, None) is None:
                    to_state.transitions[symbol].append(limbo_state)
                    if not existing_state.get(limbo_state.state_id, False):
                        existing_state[limbo_state.state_id] = True
                        states_list.append(limbo_state)
                else:
                    for transition in element.transitions[symbol]:
                        if transition.state_id not in to_state.state_id.split('-'):
                            to_state.state_id = to_state.state_id + '-' + transition.state_id
                            to_state.is_final = to_state.is_final or transition.is_final
            to_state.state_id = to_state.state_id[1:]

            current_state.transitions[symbol] = [to_state]
            if not existing_state.get(to_state.state_id, False):
                states_queue.append(to_state)

            states_list = add_state(states_list, current_state)

        if current_state.is_initial:
            initial = current_state

    return Automaton(states=states_list)


def add_state(states_list, current_state):
    """
               Function to add state to automaton if it is not already added
    """
    for state in states_list:
        if state.state_id == current_state.state_id:
            return states_list

    states_list.append(current_state)
    return states_list


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
            else:
                break

    for state in input.states:
        for each in reachable_states[state]:
            for k, v in each.transitions.items():
                if k in state.transitions.keys():
                    state.transitions[k].extend(v)
                    temp_set = set(state.transitions[k])
                    state.transitions[k] = list(temp_set)
                else:
                    state.transitions[k] = v
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


def print_automaton(input: Automaton):
    """
        Helper function to print the automaton
    """
    for state in input.states:
        for symbol, go_to in state.transitions.items():
            if state.is_initial:
                print("initial " + state.state_id + " with " + symbol + ": ")
            elif state.is_final:
                print("final " + state.state_id + " with " + symbol + ": ")
            else:
                print(state.state_id + " with " + symbol + ": ")
            for each in go_to:
                print(each.state_id, end=' ')
            print('')
        print('')


def is_dfa(input: Automaton) -> bool:
    """
           Function to check if a given automaton is deterministic or not
    """
    alphabet = get_alphabet(input)
    if ' ' in alphabet:
        return False

    for state in input.states:
        for symbol in alphabet:
            if len(state.transitions.get(symbol, [])) != 1:
                return False

    return True


def automata_are_equivalent(automaton_a: Automaton, automaton_b: Automaton) -> bool:
    """
    Calculates if two DFA are equivalent by using Moore's algorithm.
    Two automata are equivalent if the recognize the same language, regardless of their number of states.
    Doesn't support NFA, for them, convert them to DFA first

    :param automaton_a: a DF Automaton to compare
    :param automaton_b: another DF Automaton to compare
    :return: True if they are equivalent, False if otherwise
    """
    # Check if s0 and s0' are compatible, if they are not, don't do anything else
    if not states_are_compatible(automaton_a.initial_state, automaton_b.initial_state) :
        return False

    # Create a table for the transitions of each symbol

    p = automaton_a.initial_state
    q = automaton_b.initial_state

    # So that we don't process a pair more than once, initialize to the initial states
    processed_pairs = {
        "{},{}".format(p.state_id, q.state_id): True
    }

    # A queue of pair of states to follow
    states_to_follow_queue = deque([(p, q)])

    # Repeat until we find an incompatible state or we loop through all states
    while states_to_follow_queue:
        p, q = states_to_follow_queue.popleft()

        if not states_are_compatible(p, q):
            return False

        # Check where to transition, and check if both states have transitions for the symbol, if not, return False
        for symbol in p.transitions.keys():

            if symbol not in q.transitions:
                return False

            new_p = p.transitions.get(symbol)[0]    # Transitions are lists, for DFA, they are of length == 1
            new_q = q.transitions.get(symbol)[0]

            # Check if we have not already visited this pair, if we have, skip it
            str_pair = "{},{}".format(new_p.state_id, new_q.state_id)

            if str_pair not in processed_pairs:
                # Add it to the states to visit queue
                processed_pairs[str_pair] = True
                states_to_follow_queue.append((new_p, new_q))

    # If, after iterating over all states, there were no incompatible pairs, the automata are equivalent
    return True


def states_are_compatible(state_a: State, state_b: State) -> bool:
    """
    Calculates if two states are compatible.

    Compatible state are those that, given a pair, both are a final state or a reject state
    In other words, if one is final and the other isn't, they are incompatible
    :param state_a: a State to compare
    :param state_b: another State to compare
    :return: True if state_a is compatible with state_b, False otherwise
    """
    return state_a.is_final == state_b.is_final

