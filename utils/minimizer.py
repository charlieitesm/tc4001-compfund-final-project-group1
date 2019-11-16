from automata.state_machine import Automaton, State
from utils.automata_utils import states_are_compatible, is_dfa, nfa_2_dfa


def minimize_automaton(input_automaton: Automaton) -> Automaton:
    """
    Minimizes an input Automaton and returns it as a new Automaton.

    This method supports DFA only, NFA need to be transformed first.
    :param input_automaton: an Automaton to minimize
    :return: a new minimized Automaton
    """
    if not is_dfa(input_automaton):
        input_automaton = nfa_2_dfa(input_automaton)

    # Build a table with all the states, we'll use a map for that, here we'll keep track of inconsistent states
    state_map = _build_state_map(input_automaton)

    # With the state map formed, we need to loop over the map until we have crossed out all transitions with
    # non-equivalent states
    state_map = _cross_out_redundant_states(state_map)

    # Merged the states to prepare for the new automaton
    merged_states = _merge_non_redundant_states(state_map, input_automaton.states)
    new_initial_state = [state for state in merged_states if state.is_initial][0]

    # With the crossed-out redundant states out, we can build our automaton
    return Automaton(merged_states)


def _build_state_map(input_automaton: Automaton):
    state_map = {}

    for p in input_automaton.states:
        for q in input_automaton.states:
            if p == q:  # Skip pairing a state with itself
                continue

            # We should add a pair only once, (p,q) == (q,p)
            if (p, q) not in state_map and (q, p) not in state_map:
                pair_record = {
                    "isDiscarded": not states_are_compatible(p, q),  # Mark it out if p,q are incompatible
                    "symbols": {}
                }

                # Fill out the transitions for all symbols as tuples of (State, State)
                for symbol in p.transitions.keys():
                    # Remember that transitions are a list, for DFA is of length == 1
                    pair_record["symbols"][symbol] = (p.transitions.get(symbol)[0], q.transitions.get(symbol)[0])

                state_map[(p, q)] = pair_record
    return state_map


def _cross_out_redundant_states(state_map: dict) -> dict:

    while True:
        record_was_crossed_out = False

        for key, pair_record in state_map.items():
            if pair_record["isDiscarded"]:
                continue

            for symbol, (p, q) in pair_record["symbols"].items():
                # (p,q) == (q,p) so we need to cross out both records, if found to be inconsistent
                transition_pair_record = state_map.get((p, q)) or state_map.get((q, p))

                # If we find a reference to a discarded record, this record must be discarded too
                if transition_pair_record is not None and transition_pair_record["isDiscarded"]:
                    pair_record["isDiscarded"] = True
                    record_was_crossed_out = True

        if not record_was_crossed_out:
            break  # We are done now
    return state_map


def _merge_non_redundant_states(state_map: dict, original_states: list) -> list:
    # Filter out the discarded states and store them in a map (m,p): dict{}
    non_redundant_states = {pairs: record for pairs, record in state_map.items() if not record["isDiscarded"]}

    """
    We'll build a map for each of the individual states that will contain a reference to a new merged state object
    map = {
        1: State123
        2: State123
        3: State123
        4: State124
    }
    This will help us to merge all of the related IDs in a single State
    """
    merged_states = {}

    for pairs, record in non_redundant_states.items():
        p, q = pairs
        # If neither p nor q have a merged state, we need to create one
        merged_state_p = merged_states.get(p)
        merged_state_q = merged_states.get(q)

        if merged_state_p is None and merged_state_q is None:
            # Create a new merged state
            is_initial = p.is_initial or q.is_initial
            is_final = p.is_final or q.is_final
            new_state = State("{}{}".format(p.state_id, q.state_id), is_initial=is_initial, is_final=is_final)
            merged_states[p] = new_state
            merged_states[q] = new_state

        elif merged_state_p is not None and merged_state_q is None:
            # We need to append the ID of Q to the already merged state and update Q's record
            merged_state_p.state_id += q.state_id
            merged_states[q] = merged_state_p
        elif merged_state_p is None and merged_state_q is not None:
            # We need to append the ID of P to the already merged state and update P's record
            merged_state_q.state_id += p.state_id
            merged_states[p] = merged_state_q

    # After merging the states, we need to add those original states that were not paired up with anyone as a new State
    for old_state in [state for state in original_states if state not in merged_states]:
        new_state = State(old_state.state_id, is_initial=old_state.is_initial, is_final=old_state.is_final)
        merged_states[old_state] = new_state

    return _calculate_new_transitions(merged_states)


def _calculate_new_transitions(merged_states: dict) -> list:
    final_states = []

    for old_state, new_state in merged_states.items():
        # Don't add update the new state more than once
        if new_state in final_states:
            continue

        for symbol, transition_state in old_state.transitions.items():
            transition_state = transition_state[0]  # DFA have only one transition state
            new_transition_state = merged_states.get(transition_state)
            new_state.transitions[symbol] = [new_transition_state]

        final_states.append(new_state)

    return final_states
