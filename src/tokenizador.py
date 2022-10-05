from typing import Tuple
# from automata.regex_to_postfix import parse_clases_chars, regex_to_postfix, add_concat_symbol
# from automata.regex_to_nfa import regex_to_nfa
# from automata.nfa_to_dfa import nfa_to_dfa


# from sys import argv

# if len(argv) < 3:
#     raise SystemExit("Introduzca el número de argumentos adecuado.")

# tokens_txt: str = argv[1]
# program_txt: str = argv[2]

archivo_tokens = "../input/tokens.txt"
archivo_programa = "../input/program.txt"
dfas = []


def main():

    # pasa de expresion regular a AFD
    for nombre_token, regex_token in parse_archivo_tokens(archivo_tokens):
        print(regex_token)
        # regex_token = regex_to_postfix(regex_token)
        # nfa = regex_to_nfa(regex_token)
        # dfa = nfa_to_dfa(nfa)
        # dfa["token"] = nombre_token
        # dfas.append(dfa)


    # tokenización
    # with open(archivo_programa, mode="r") as texto:
    #     buffer = texto.read()
    #     for dfa in dfas:
    #         nombre_token, pos_match_mas_largo = "", 0
    #         posible_match_mas_largo = consumir(buffer, dfa)

    #         if posible_match_mas_largo > pos_match_mas_largo:
    #             pos_match_mas_largo = posible_match_mas_largo
    #             nombre_token = dfa["token"]


def consumir(input, dfa):
    """
    Consume la cadena `buffer` con el AFD `dfa` y retorna la posición en la cadena
    del match mas largo.
    """
    pos_match = 0

    current_state = dfa["initial_state"]
    for char, pos in enumerate(input):
        current_state = dfa["transition_function"][current_state][char]
        if current_state in dfa["final_states"]:
            pos_match = pos + 1

    return pos_match


def parse_archivo_tokens(nombre_archivo: str) -> list[Tuple[str, str]]:
    """
    Se toma el nombre del archivo para;
    generar una lista de tuplas, almacenar
    el token y su respectiva expresión regular
    """
    tokens = []

    with open(nombre_archivo, "r") as archivo_tokens:
        for linea in archivo_tokens.read().split("\n"):
            if linea:
                linea = linea.split("->")
                nombre_token = linea[0].strip()
                regex_token = linea[1].strip()
                tokens.append((nombre_token, regex_token))

    return tokens

if __name__ == "__main__":
    main()
