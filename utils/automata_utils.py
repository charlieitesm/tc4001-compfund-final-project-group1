
from collections import deque

from automata.state_machine import Automaton, State


def nfa_2_dfa(input: Automaton) -> Automaton:
    """
           Function to convert from a non deterministic finite automaton to a deterministic one
     """
    states_list = []
    initial = None
    existing_state = {}
    alphabet = get_alphabet(input)

    if ' ' in alphabet:
        input = clean_epsilon_transition(input)
        alphabet.remove(' ')

    nfa_transitions = {}
    for nfa_state in input.states:
        for symbol in alphabet:

            if nfa_state.state_id not in nfa_transitions:
                nfa_transitions[nfa_state.state_id] = {}

            nfa_transitions[nfa_state.state_id][symbol] = nfa_state.transitions.get(symbol)

    # With the AFN transitions mapped in a table, let's create the new states

    # We'll use this queue later for deriving the new DFA transition table from new states
    new_state_deriving_queue = deque()

    # The first new state is the initial and it shares the ID with the original NFA
    nfa_initial = input.initial_state
    dfa_initial = State(nfa_initial.state_id, is_initial=nfa_initial.is_initial, is_final=nfa_initial.is_final)

    states_already_created = {
        dfa_initial.state_id: dfa_initial
    }

    dfa_transitions = {
        dfa_initial: {}
    }

    # Build the DFA transitions for the initial first from which we will derive the rest of the new states
    initial_transitions = nfa_transitions[nfa_initial.state_id]

    for symbol, state_combination in initial_transitions.items():
        # Get the state IDs first and sort them alphabetically so that we never repeat the same combination of IDs
        old_state_ids = sorted([state.state_id for state in state_combination])
        new_id = "".join(old_state_ids)
        new_state = states_already_created.get(new_id, None)

        if new_state is None:
            # If at least one final state is in this combination, the new state will inherit this property
            is_final = any([old_state.is_final for old_state in state_combination])
            new_state = State(new_id, is_final=is_final)

            # Save this new state in the cache for later reuse if needed
            states_already_created[new_id] = new_state
            # Add it to the state deriving queue
            new_state_deriving_queue.append(new_state)

        dfa_transitions[dfa_initial][symbol] = new_state

    # Get the IDs of the final states
    final_states_ids = [state.state_id for state in input.states if state.is_final]

    # Start deriving the rest of the states from the dfa_transitions we already have
    dfa_transitions, states_already_created = _derive_new_dfa_states_from_intial(dfa_transitions,
                                                         nfa_transitions,
                                                         states_already_created,
                                                         alphabet,
                                                         final_states_ids,
                                                         new_state_deriving_queue)

    # With the transition map for the DFA and the cache of states created, we can link the states correctly
    for state, transition_map in dfa_transitions.items():
        states_list.append(state)

        if state.is_initial:
            initial = state

        for symbol, destination_state in transition_map.items():
            state.transitions[symbol] = [destination_state]  # The transitions are encoded in lists

    return Automaton(initial_state=initial, states=states_list)


def _derive_new_dfa_states_from_intial(dfa_transitions: dict,
                                       nfa_transitions: dict,
                                       states_already_created: dict,
                                       alphabet: list,
                                       final_state_ids: list,
                                       new_state_deriving_queue: deque) -> (dict, dict):

    while new_state_deriving_queue:
        new_state_entry = new_state_deriving_queue.popleft()

        if new_state_entry not in dfa_transitions:
            new_state_transitions = {}

            for symbol in alphabet:
                # Break the ID of the new state entry into individual chars to look them up in the original
                # nfa_transitions ABC -> A,B,C
                potential_new_id_digits = []  # A set of unique characters that will help us create the new state ID

                for char_in_id in [c for c in new_state_entry.state_id]:
                    # Get the ID for this symbol in the old NFA transition map
                    old_nfa_transitions = nfa_transitions[char_in_id][symbol]

                    if not old_nfa_transitions: # If this state doesn't have a transition, skip its lookup
                        continue
                    potential_new_id_digits.extend([state.state_id for state in old_nfa_transitions])

                # We order the portions in alphabetical order (to avoid duplicates) of the new ID and remove
                # any repeated ID and transform it to a single string
                potential_new_id_digits = sorted(list(set(potential_new_id_digits)))
                potential_new_id = "".join(potential_new_id_digits)

                # Have we already created a state for this ID?
                state_to_transition_to = states_already_created.get(potential_new_id, None)

                if state_to_transition_to is None:
                    # We haven't seen this one yet, let's create it, add it to the deriving queue
                    is_final = any([True for st_id in potential_new_id_digits if st_id in final_state_ids])
                    state_to_transition_to = State(potential_new_id, is_final=is_final)
                    new_state_deriving_queue.append(state_to_transition_to)

                    # Add it to the cache for potential reuse
                    states_already_created[potential_new_id] = state_to_transition_to

                # Map it in the new transitions map to be added to dfa_transitions for the state
                new_state_transitions[symbol] = state_to_transition_to

            dfa_transitions[new_state_entry] = new_state_transitions

    return dfa_transitions, states_already_created


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

