import re
from os import linesep
from automata.state_machine import Automaton, State


def deserialize_automaton(input_file_path: str) -> Automaton:
    states = []
    visited_state = set()
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
            initial = ">" in sInit
            final = "*" in sInit

            stateId = re.sub("[>*]", "", sInit)

            if initial:
                initial_state = stateId
            if final:
                final_state = stateId  # at least one final state

            if stateId not in visited_state:
                visited_state.add(stateId)
                state = State(stateId, is_initial=initial, is_final=final)
                state.transitions[transition] = [s_out]
                states.append(StateType(stateId, state))
            else:
                for s in states:
                    if s.stateId == stateId:
                        s.add_transition(transition, s_out)

    if initial_state is None and final_state is None:
        raise ValueError("The provided automata contains no initial or final state")

    return Automaton(initial_state, states)


def serialize_automaton(input: Automaton) -> str:
    # TODO: Implement me!
    automaton = "# Generated string"
    stats = input.states
    state_list = []

    for st in stats:
        stat = st.state
        for val in stat.transitions.items():
            for v in val[1]:
                if stat.is_initial:
                    automaton += _calculate_str(">", stat.state_id + "|" + val[0] + "|" + v)
                if not stat.is_initial and not stat.is_final:
                    automaton += _calculate_str("", stat.state_id + "|" + val[0] + "|" + v)
                if stat.is_final:
                    automaton += _calculate_str("*", stat.state_id + "|" + val[0] + "|" + v)

    #print(automaton)
    return automaton


def _calculate_str(symbol, state):
    return linesep + symbol + state


def save_str_to_file(output_file_path: str, contents: str):
    with open(output_file_path, mode="w", encoding="utf8") as fl:
        print(contents, file=fl)


class StateType:
    def __init__(self, stateId: str, state: State):
        self.stateId = stateId
        self.state = state

    def add_transition(self, transition, s_out):
        self.state.transitions[transition].append(s_out)
