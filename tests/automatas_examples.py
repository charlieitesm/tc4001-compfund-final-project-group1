from state_machine import Automaton, State


def state_machine_1() -> (Automaton, Automaton):
    s1 = State("1", is_initial=True)
    s2 = State("2")
    s3 = State("3")
    s4 = State("4")
    s5 = State("5")
    s6 = State("6", is_final=True)
    s7 = State("7")

    s1.transitions["0"] = [s2]
    s1.transitions["1"] = [s3]

    s2.transitions["0"] = [s4]
    s2.transitions["1"] = [s5]

    s3.transitions["0"] = [s6]
    s3.transitions["1"] = [s7]

    s4.transitions["0"] = [s4]
    s4.transitions["1"] = [s5]

    s5.transitions["0"] = [s6]
    s5.transitions["1"] = [s7]

    s6.transitions["0"] = [s4]
    s6.transitions["1"] = [s5]

    s7.transitions["0"] = [s6]
    s7.transitions["1"] = [s7]

    states = [s1, s2, s3, s4, s5, s6, s7]

    big_automaton = Automaton(s1, states)

    s1 = State("124", is_initial=True)
    s2 = State("357")
    s3 = State("6", is_final=True)

    s1.transitions["0"] = [s1]
    s1.transitions["1"] = [s2]

    s2.transitions["0"] = [s3]
    s2.transitions["1"] = [s2]

    s3.transitions["0"] = [s1]
    s3.transitions["1"] = [s2]

    states = [s1, s2, s3]

    min_automaton = Automaton(s1, states)

    return big_automaton, min_automaton
