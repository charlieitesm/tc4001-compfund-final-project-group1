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
    # TODO: Implement me! This is a nice-to-have but we may want to implement it for
    #  verification purposes
    pass


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
