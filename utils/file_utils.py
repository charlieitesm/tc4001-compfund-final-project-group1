import re
from os import linesep
from automata.state_machine import Automaton, State


def deserialize_automaton(input_file_path: str) -> Automaton:
    states = []
    visited_state = {}
    initial_state = None
    final_state = None

    with open(input_file_path, "r") as file:
        for line in file:
            if line.startswith("#") or line.strip() == '':
                continue
            curated_line = line.strip('\n').split("|")
            sInit = curated_line[0]
            transition = curated_line[1]
            s_out = curated_line[2]


            initial_tag = is_init(sInit)
            final_tag = is_final(sInit)
            initial_id = remove_char(sInit)

            out_initial_tag = is_init(s_out)
            out_final_tag = is_final(s_out)
            out_id = remove_char(s_out)
            #out_tmp_state = None

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

            if initial_id not in visited_state.keys():
                state = state_creation(initial_id, initial_tag, final_tag)
                visited_state[initial_id] = state
                state.transitions[transition] = [out_tmp_state]
                states.append(state)
            else:
                state = visited_state[initial_id]
                state.transitions[transition].append(out_tmp_state)


            if initial_tag:
                initial_state = state
                state.is_initial = True

    if initial_state is None and final_state is None:
        raise ValueError("The provided automata contains no initial or final state")

    return Automaton(initial_state, states)


def is_init(state):
    return ">" in state


def is_final(state):
    return "*" in state


def remove_char(tag):
    return re.sub("[>*]", "", tag)


def state_creation(stateId, is_inital, is_final) -> State:
    return State(stateId, is_initial=is_inital, is_final=is_final)

def serialize_automaton(input: Automaton) -> str:
    automaton = "# Generated string"
    stats = input.states

    for st in stats:
        state_id = st.state_id
        is_init = st.is_initial
        is_fin = st.is_final
        already_processed = None
        for val in st.transitions.keys():
            trans_name = val
            vals = st.transitions[trans_name]
            for v in vals:
                if is_init and is_fin:
                    if not already_processed:
                        automaton += _calculate_str(">*", state_id + "|" + trans_name + "|" + v.state_id)
                        already_processed = True
                    else:
                        automaton += _calculate_str("", state_id + "|" + trans_name + "|" + v.state_id)
                if is_init and not is_fin:
                    automaton += _calculate_str(">", state_id + "|" + trans_name + "|" + v.state_id)
                if not st.is_initial and not st.is_final:
                    automaton += _calculate_str("", state_id  + "|" + trans_name + "|" + v.state_id)
                if is_fin and not is_init:
                    if not already_processed:
                        automaton += _calculate_str("*", state_id  + "|" + trans_name + "|" + v.state_id)
                        already_processed = True
                    else:
                        automaton += _calculate_str("", state_id + "|" + trans_name + "|" + v.state_id)

    return automaton


def _calculate_str(symbol, state):
    return linesep + symbol + state


def save_str_to_file(output_file_path: str, contents: str):
    with open(output_file_path, mode="w", encoding="utf8") as fl:
        print(contents, file=fl)

