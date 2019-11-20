import re
from os import linesep

from automata.state_machine import Automaton, State


def deserialize_automaton(input_file_path: str) -> Automaton:
    states = []
    visited_state = {}

    with open(input_file_path, "r") as file:
        for line in file:

            if line.startswith("#") or line.strip() == '':
                continue

            curated_line = line.strip('\n').split("|")
            s_init = curated_line[0]
            transition = curated_line[1]
            s_out = curated_line[2]

            is_in_initial = is_init(s_init)
            is_in_final = is_final(s_init)
            in_id = remove_char(s_init)

            out_initial_tag = is_init(s_out)
            out_final_tag = is_final(s_out)
            out_id = remove_char(s_out)

            if out_id in visited_state.keys():
                out_tmp_state = visited_state[out_id]
                if out_initial_tag and not out_tmp_state.is_initial:
                    out_tmp_state.is_initial = out_initial_tag
                if out_final_tag and not out_tmp_state.is_final:
                    out_tmp_state.is_final = out_final_tag
            else:
                out_tmp_state = State(out_id, out_initial_tag, out_final_tag)
                visited_state[out_id] = out_tmp_state
                states.append(out_tmp_state)

            if in_id not in visited_state.keys():
                state = State(in_id, is_initial=is_in_initial, is_final=is_in_final)
                visited_state[in_id] = state
                state.transitions[transition] = [out_tmp_state]
                states.append(state)
            else:
                state = visited_state[in_id]
                state.transitions[transition].append(out_tmp_state)

            if is_in_initial:
                state.is_initial = True

    return Automaton(states)


def is_init(state):
    return ">" in state


def is_final(state):
    return "*" in state


def remove_char(tag):
    return re.sub("[>*]", "", tag)


def serialize_automaton(input_automaton: Automaton) -> str:
    output_str_elements = []

    for st in input_automaton.states:
        state_id = st.state_id

        for symbol, states_to_transition_to in st.transitions.items():

            for destination_state in states_to_transition_to:
                line = [linesep]

                if st.is_initial:
                    line.append(">")

                if st.is_final:
                    line.append("*")
                line.extend([state_id, "|", symbol, "|"])

                if destination_state.is_initial:
                    line.append(">")

                if destination_state.is_final:
                    line.append("*")

                line.append(destination_state.state_id)
                output_str_elements.extend(line)

    return "".join(output_str_elements)


def save_str_to_file(output_file_path: str, contents: str):
    with open(output_file_path, mode="w", encoding="utf8") as fl:
        print(contents, file=fl)

