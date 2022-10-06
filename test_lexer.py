from compiler_tools.nfa_to_dfa import set_construction, consume
from compiler_tools.regex_to_nfa import regex_to_nfa
from compiler_tools.lexer import lexical_analysis


def test_identifier():
    reg_exp = "[_a-z][_0-9a-z]*"
    nfa = regex_to_nfa(reg_exp)
    dfa = set_construction(nfa)

    inputs = ["carro", "_hola", "", "ab012a", "ab012a+***", "for a = 1\n"]
    matchs = [5, 5, 0, 6, 6, 3]

    for input, match in zip(inputs, matchs):
        assert consume(input, dfa) == match


def test_digit():
    reg_exp = "0|[1-9][0-9]*"
    nfa = regex_to_nfa(reg_exp)
    dfa = set_construction(nfa)

    inputs = ["0", "0123", "123", "3", "1234900", "0001123", "avion", "123avion"]
    matchs = [1, 1, 3, 1, 7, 1, 0, 3]

    for input, match in zip(inputs, matchs):
        assert consume(input, dfa) == match


def test_whitespace():
    reg_exp = "[ \t\n][ \t\n]*"
    nfa = regex_to_nfa(reg_exp)
    dfa = set_construction(nfa)

    inputs = [
        " ",
        "    ",
        """
             """,
        "\n ",
        "\t\n",
    ]
    matchs = [1, 4, 14, 2, 2]

    for input, match in zip(inputs, matchs):
        assert consume(input, dfa) == match


def test_lexer():
    token_info = [
        "Tipo de token: for - Posición inicial: 1 - Posición final: 3 - Valor: for",
        "Tipo de token: space - Posición inicial: 4 - Posición final: 4 - Valor:  ",
        "Tipo de token: identifier - Posición inicial: 5 - Posición final: 5 - Valor: a",
        "Tipo de token: space - Posición inicial: 6 - Posición final: 6 - Valor:  ",
        "Tipo de token: equal - Posición inicial: 7 - Posición final: 7 - Valor: =",
        "Tipo de token: space - Posición inicial: 8 - Posición final: 8 - Valor:  ",
        "Tipo de token: digit - Posición inicial: 9 - Posición final: 9 - Valor: 1",
    ]
    tokens_file = "input/tokens_example.txt"
    program_file = "input/program_example.txt"

    assert lexical_analysis(tokens_file, program_file) == token_info
