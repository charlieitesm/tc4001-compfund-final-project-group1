import sys

from minimizer import minimize_automaton
from utils.file_utils import deserialize_automaton, serialize_automaton, save_str_to_file

VERSION = "0.0.1"
OUTPUT_FILE = "minimized_automaton.txt"


def main():
    _print_project_info()
    args = _parse_args()

    # Read the automaton from file
    input_file_path = args.get("input_file_path")
    print("Reading automaton from {}...".format(input_file_path))
    input_automaton = deserialize_automaton(input_file_path)

    # Minimize the automaton, the automaton will be automatically converted to a DFA if it is a NFA
    print("Minimizing automaton...")
    minimized_automaton = minimize_automaton(input_automaton)

    # Prepare the automata for printing by converting them to Byron TXT format
    original_automaton_str = serialize_automaton(input_automaton)
    mini_automaton_str = serialize_automaton(minimized_automaton)

    # Print the results to stdout
    print_results(original_automaton_str, mini_automaton_str)

    # Save the results to file for later inspection
    print("Saving results to {}...".format(OUTPUT_FILE))
    save_str_to_file(OUTPUT_FILE, mini_automaton_str)

    print("DONE!")


def _print_project_info():
    project_info = """
    ********** ITESM - MCC - Computer Fundamentals **********
            ********** Automata Minimizer v.{} **********
    
                    A program by
                    
                        A01181616
                        A00354827
                        A00354824
                        
                        November 2019
    
    *********************************************************
    """.format(VERSION)

    print(project_info)


def _parse_args() -> dict:

    if len(sys.argv) < 2:
        raise ValueError("The input file path with the automata was not provided")

    input_path = sys.argv[1]

    if not input_path:
        raise ValueError("The input file path is empty!")

    args = {
        "input_file_path": input_path
    }

    return args


def print_results(input_automaton: str, mini_automaton: str):
    results = """
    ####### RESULTS #########
    
    Given the input automata:
    
    {}
    
    The minimized equivalent automata is:
    
    {}
    
    """.format(input_automaton, mini_automaton)

    print(results)


if __name__ == '__main__':
    main()
