from typing import Tuple
from regex_to_nfa import regex_to_nfa
from nfa_to_dfa import set_contruction, consume


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
    for token_name, regex_token in parse_archivo_tokens(archivo_tokens):
        nfa = regex_to_nfa(regex_token)
        dfa = set_contruction(nfa)
        dfa["token_name"] = token_name
        dfas.append(dfa)

    # tokenización
    with open(archivo_programa, mode="r") as texto:
        buffer = texto.read().strip()
        print(buffer, end="\n")

        start_pos = 1
        while buffer:
            token_name, longest_match = "", 0
            for dfa in dfas:
                possible_longest_match = consume(buffer, dfa)

                if possible_longest_match > longest_match:
                    longest_match = possible_longest_match
                    token_name = dfa["token_name"]
            final_pos = start_pos + longest_match - 1
            value = buffer[:longest_match]
            print(
                f'Tipo de token: {token_name} - Posición inicial: {start_pos} - Posición final: {final_pos} - Valor: "{value}"'
            )

            start_pos = final_pos + 1
            buffer = buffer[longest_match:]


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
