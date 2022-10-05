from lexer.nfa_to_dfa import set_contruction, consume
from lexer.regex_to_nfa import regex_to_nfa

def test_tokenizer():
    reg_exp = "[_a-z][_0-9a-z]*"
    nfa = regex_to_nfa(reg_exp)
    dfa = set_contruction(nfa)

    inputs = ["carro", "_hola", "", "ab012a", "ab012a+***", "for a = 1\n"]
    matchs = [5, 5, 0, 6, 6, 3]

    for input, match in zip(inputs, matchs):
        assert consume(input, dfa) == match

