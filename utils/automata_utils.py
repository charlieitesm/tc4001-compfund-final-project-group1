from collections import deque

from automata.state_machine import Automaton, State


def minimize_automaton(input: Automaton) -> Automaton:
    # TODO: Implement me!
    pass


def nfa_2_dfa(input: Automaton) -> Automaton:
    # TODO: Implement me!
    pass


def is_dfa(input: Automaton) -> bool:
    # TODO: Implement this. It is not essential for converting from NFA to DFA, but
    #  it is desirable
    pass


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
