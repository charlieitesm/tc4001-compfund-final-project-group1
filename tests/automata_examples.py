from automata.state_machine import Automaton, State


def state_machine_1() -> (Automaton, Automaton):
    s1 = State("1", is_initial=True)
    s2 = State("2")
    s3 = State("3")
    s4 = State("4")
    s5 = State("5")
    s6 = State("6", is_final=True)
    s7 = State("7")

    symbols = ["0", "1"]

    transitions = (
        # ID   0      1
        (s1, ([s2], [s3])),
        (s2, ([s4], [s5])),
        (s3, ([s6], [s7])),
        (s4, ([s4], [s5])),
        (s5, ([s6], [s7])),
        (s6, ([s4], [s5])),
        (s7, ([s6], [s7]))
    )

    _set_transitions(transitions, symbols)

    big_automaton = Automaton([s1, s2, s3, s4, s5, s6, s7])

    s1 = State("124", is_initial=True)
    s2 = State("357")
    s3 = State("6", is_final=True)

    transitions = (
        # ID   0      1
        (s1, ([s1], [s2])),
        (s2, ([s3], [s2])),
        (s3, ([s1], [s2]))
    )

    _set_transitions(transitions, symbols)

    min_automaton = Automaton([s1, s2, s3])

    return big_automaton, min_automaton


def state_machine_2() -> (Automaton, Automaton):
    s6 = State("6", is_initial=True, is_final=True)
    s7 = State("7", is_final=True)
    s8 = State("8", is_final=True)
    s9 = State("9", is_final=True)
    s10 = State("10", is_final=True)
    s11 = State("11", is_final=True)
    s12 = State("12")

    symbols = ["0", "1"]

    transitions = (
        # ID   S0   S1
        (s6, ([s7], [s9])),
        (s7, ([s7], [s8])),
        (s8, ([s7], [s10])),
        (s9, ([s7], [s10])),
        (s10, ([s11], [s10])),
        (s11, ([s12], [s10])),
        (s12, ([s12], [s12]))
    )

    _set_transitions(transitions, symbols)

    big_automaton = Automaton([s6, s7, s8, s9, s10, s11, s12])

    s_a = State("A", is_initial=True, is_final=True)
    s_b = State("B", is_final=True)
    s_c = State("C", is_final=True)
    s_d = State("D", is_final=True)
    s_e = State("E")

    transitions = (
        # ID   S0   S1
        (s_a, ([s_a], [s_b])),
        (s_b, ([s_a], [s_c])),
        (s_c, ([s_d], [s_c])),
        (s_d, ([s_e], [s_c])),
        (s_e, ([s_e], [s_e]))
    )

    _set_transitions(transitions, symbols)

    mini_automaton = Automaton([s_a, s_b, s_c, s_d, s_e])

    return big_automaton, mini_automaton


def state_machine_3() -> (Automaton, Automaton):
    s3 = State("3", is_initial=True, is_final=True)
    s4 = State("4")
    s5 = State("5", is_final=True)

    symbols = ["a", "b"]
    transitions = (
        # ID   a     b
        (s3, ([s4], [s3])),
        (s4, ([s5], [s4])),
        (s5, ([s5], [s4]))
    )
    _set_transitions(transitions, symbols)

    automaton = Automaton([s3, s4, s5])

    # Since we don't have an equivalent "big automaton" we'll return the same automaton as both the mini and big
    return automaton, automaton


def state_machine_4() -> (Automaton, Automaton):
    s1 = State("1", is_initial=True, is_final=True)
    s2 = State("2")

    symbols = ["a", "b"]
    transitions = (
        # ID   a     b
        (s1, ([s2], [s1])),
        (s2, ([s1], [s2]))
    )
    _set_transitions(transitions, symbols)

    automaton = Automaton([s1, s2])

    # Since we don't have an equivalent "big automaton" we'll return the same automaton as both the mini and big
    return automaton, automaton


def state_machine_nfa_1() -> (Automaton, Automaton):
    """
    Returns a NFA that describes the Language over {0,1} where the third-to-last char is 1.
    No Epsillon-transitions
    :return: a NF Automaton
    """
    s1 = State("A", is_initial=True)
    s2 = State("B")
    s3 = State("C")
    s4 = State("D", is_final=True)

    symbols = ["0", "1"]
    transitions = (
        # ID   0     1
        (s1, ([s1], [s1, s2])),
        (s2, ([s3], [s3])),
        (s3, ([s4], [s4])),
    )

    _set_transitions(transitions, symbols)

    nfa = Automaton([s1, s2, s3, s4])

    # Let's build the equivalent DFA to this NFA
    dfaS_A = State("A", is_initial=True)
    dfaS_AB = State("AB")
    dfaS_ABC = State("ABC")
    dfaS_ABCD = State("ABCD", is_final=True)
    dfaS_ACD = State("ACD", is_final=True)
    dfaS_ABD = State("ABD", is_final=True)
    dfaS_AC = State("AC")
    dfaS_AD = State("AD", is_final=True)

    transitions = (
        # ID           0            1
        (dfaS_A,    ([dfaS_A],   [dfaS_AB])),
        (dfaS_AB,   ([dfaS_AC],  [dfaS_ABC])),
        (dfaS_ABC,  ([dfaS_ACD], [dfaS_ABCD])),
        (dfaS_ABCD, ([dfaS_ACD], [dfaS_ABCD])),
        (dfaS_ACD,  ([dfaS_AD],  [dfaS_ABD])),
        (dfaS_ABD,  ([dfaS_AC],  [dfaS_ABC])),
        (dfaS_AC,   ([dfaS_AD],  [dfaS_ABD])),
        (dfaS_AD,   ([dfaS_A],   [dfaS_AB])),
    )

    _set_transitions(transitions, symbols)

    dfa = Automaton([dfaS_A, dfaS_AB, dfaS_ABC, dfaS_ABCD, dfaS_ACD, dfaS_ABD, dfaS_AC, dfaS_AD])

    return nfa, dfa


def state_machine_nfa_2() -> Automaton:
    """
    Returns a NFA that has Epsillon transitions
    :return: a NFAutomaton with Epsillon transition
    """
    s1 = State("A", is_initial=True)
    s2 = State("B")
    s3 = State("C")
    s4 = State("D", is_final=True)

    symbols = ["0", "1", " "]
    transitions = (
        # ID   0     1    Epsillon
        (s1, ([s1], [s2], [])),
        (s2, ([s3], [s2], [s1])),
        (s3, ([],   [s4], [s2])),
        (s4, ([s3], [],   [s2])),
    )

    _set_transitions(transitions, symbols)

    return Automaton([s1, s2, s3, s4])


def state_machine_nfa_3() -> Automaton:
    """
    Returns a NFA that has Epsillon transitions and one and only one transition for each symbol.
    Even though it might look like a DFA, the fact that this automata has epsillon transitions
    makes it a NFA
    :return: a NFAutomaton with Epsillon transition
    """
    s1 = State("A", is_initial=True)
    s2 = State("B")
    s3 = State("C")
    s4 = State("D", is_final=True)

    symbols = ["0", "1", " "]
    transitions = (
        # ID   0     1    Epsillon
        (s1, ([s2], [s2], [s4])),
        (s2, ([s3], [s3], [s1])),
        (s3, ([s4], [s4], [s2])),
        (s4, ([s4], [s4], [s3])),
    )

    _set_transitions(transitions, symbols)

    return Automaton([s1, s2, s3, s4])


def state_machine_nfa_4() -> Automaton:
    """
    Creates a 6-state NFA with no epsillon transitions that possess a known DFA and a minimized DFA

    We saw this one during class on the AFN - DFA lecture
    :return: a NFAutomaton with no Epsillon transitions
    """
    s_a = State("A", is_initial=True)
    s_b = State("B")
    s_c = State("C")
    s_d = State("D")
    s_e = State("E")
    s_f = State("F", is_final=True)

    symbols = ["0", "1"]
    transitions = (
        # ID   0            1
        (s_a, ([s_a, s_b],  [s_a, s_d])),
        (s_b, ([s_c],       [])),
        (s_c, ([s_f],       [])),
        (s_d, ([],          [s_e])),
        (s_e, ([],          [s_f])),
        (s_f, ([s_f],       [s_f])),
    )

    _set_transitions(transitions, symbols)

    return Automaton([s_a, s_b, s_c, s_d, s_e, s_f])


def _set_transitions(transitions: tuple, symbols: list):
    # transitions should be in the form (state, ((states_for_symbol1), (states_for_symbol2)))
    #  where len(tuple[1]) == len(symbols)

    for state_conf in transitions:
        state = state_conf[0]

        for symbol_idx in range(len(symbols)):
            symbol = symbols[symbol_idx]
            states_to_transition_to = list(state_conf[1][symbol_idx])
            state.transitions[symbol] = states_to_transition_to
