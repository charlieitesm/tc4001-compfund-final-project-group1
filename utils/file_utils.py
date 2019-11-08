from automata.state_machine import Automaton
from automata.state_machine import State


def deserialize_automaton(input_file_path: str) -> Automaton:
    errors = getattr(__builtins__, 'FileNotFoundError', IOError)
    try:
        states = []
        initial_state = State()
        file = open(input_file_path, "r")
        for line in file:
            curated_line = line.strip('\n').split("|")
            sInit = curated_line[0]
            transition = curated_line[1]
            eOut = curated_line[2]
            state = None

            if ">" in sInit:
                state = State(sInit.strip(">"), is_initial = True)
                initial_state = state
            elif "*" in sInit:
                state = State(sInit.strip("*"), is_final = True)
            else:
                state = State(sInit)

            states.append(state)
            state.transitions[transition] = eOut

        return Automaton(initial_state, states)
    except errors:
        print("Error: File missing or cannot be opened")


def serialize_automaton(input: Automaton) -> str:
    # TODO: Implement me!
    pass


def save_str_to_file(output_file_path: str, contents: str):
    # TODO: Implement me!
    pass
