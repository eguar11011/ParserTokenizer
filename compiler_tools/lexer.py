from typing import Tuple
from compiler_tools.regex_to_nfa import regex_to_nfa
from compiler_tools.nfa_to_dfa import set_construction, consume
from compiler_tools.visual_utils import draw_dfa


def get_dfas(tokens_file):
    dfas = []

    for token_name, regex_token in parse_archivo_tokens(tokens_file):
        nfa = regex_to_nfa(regex_token)
        dfa = set_construction(nfa)

        dfa["token_name"] = token_name
        dfas.append(dfa)

    return dfas

def lexical_analysis(tokens_file, program_file):
    """
    Perfoms a lexical analysis of the file with `pogram_file` path, with respect
    to the tokens defined in the file with path`tokens_file`. Returns a list
    with relevant token related information.
    """
    token_info = []

    # pasa de expresiones regulares a AFDs
    dfas = get_dfas(tokens_file)

    # tokenización
    with open(program_file, mode="r") as texto:

        buffer = texto.read().strip()
        start_pos = 1

        while buffer:
            token_name, longest_match = "", 0

            # prueba hacer match con todos los tokens
            for dfa in dfas:
                possible_longest_match = consume(buffer, dfa)

                if possible_longest_match > longest_match:
                    longest_match = possible_longest_match
                    token_name = dfa["token_name"]

            if token_name == "":
                # si los espacios en blanco no son tokens, entonces se ignoran
                ws_match = consume_whitespace(buffer)
                if ws_match != 0:
                    start_pos += ws_match
                    buffer = buffer[ws_match:]
                    continue
                else:
                    raise Exception("El input no coincide con ningun token.")

            final_pos = start_pos + longest_match - 1
            value = buffer[:longest_match]

            token_info.append(
                f"Tipo de token: {token_name} - Posición inicial: {start_pos} - Posición final: {final_pos} - Valor: {value}"
            )

            start_pos = final_pos + 1
            buffer = buffer[longest_match:]

    return token_info


def consume_whitespace(buffer):
    """
    Consume los caracteres en blanco del buffer
    """
    ws_regex = "[ \t\n][ \t\n]*"
    nfa = regex_to_nfa(ws_regex)
    dfa = set_construction(nfa)

    return consume(buffer, dfa)


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
