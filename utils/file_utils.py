from automata.state_machine import Automaton, State


def deserialize_automaton(input_file_path: str) -> Automaton:
    states = []
    initial_state = State()
    file = open(input_file_path, "r")
    initial = False
    final = False
    for line in file:
        if line.startswith("#") or line.strip() == '':
            continue
        curated_line = line.strip('\n').split("|")
        sInit = curated_line[0]
        transition = curated_line[1]
        s_out = curated_line[2]
        state = None

        # initial and acceptor
        if ">*" in sInit:
            state = State(sInit.strip(">*"), is_initial=True, is_final=True)
            initial_state = state
            initial = True
            final = True
        # initial
        if ">" in sInit:
            state = State(sInit.strip(">"), is_initial=True)
            initial_state = state
            initial = True
        # acceptor
        if "*" in sInit:
            state = State(sInit.strip("*"), is_final=True)
            final = True
        # state has not been assigned yet, so that means
        # that it is a "regular" state.
        if state is None:
            state = State(sInit)

        states.append(state)
        state.transitions[transition] = s_out

    file.close()

    if not initial and not final:
        raise ValueError("The provided automata contains no initial or final state")

    return Automaton(initial_state, states)


def serialize_automaton(input: Automaton) -> str:
    # TODO: Implement me!
    pass


def save_str_to_file(output_file_path: str, contents: str):
    # TODO: Implement me!
    pass
