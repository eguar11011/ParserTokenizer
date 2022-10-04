from string import ascii_uppercase, ascii_lowercase

priority = {"*": 3, ".": 2, "|": 1}


def is_alphabet(c):
    return c not in priority.keys() and c not in ["(", ")"]


def chartype(char):
    if char.isdigit():
        return "digit"
    elif char in ascii_lowercase:
        return "locase"
    elif char in ascii_uppercase:
        return "upcase"
    else:
        return "other"


def parse_clases_chars(reg_exp: str):
    pos_bracket_izq = reg_exp.find("[")
    pos_bracket_der = reg_exp.find("]")

    while pos_bracket_izq != -1:

        if pos_bracket_der == -1 or pos_bracket_der <= pos_bracket_izq:
            raise Exception("expresión regular invalida.")

        bracket_exp = reg_exp[pos_bracket_izq + 1 : pos_bracket_der]
        union_exp = f"({bracket_exp[0]}"

        # pasar la expresion a uniones
        for idx, char in enumerate(bracket_exp[1:]):
            idx += 1
            # expresiones con rango
            if char == "-" and idx + 1 < len(bracket_exp):
                prev = bracket_exp[idx - 1]
                next = bracket_exp[idx + 1]
                if chartype(prev) == chartype(next) and chartype(prev) != "other":
                    union_exp += "|" + "|".join(
                        [chr(i) for i in range(ord(prev) + 1, ord(next))]
                    )
            else:
                union_exp += f"|{char}"
        union_exp += ")"

        reg_exp = reg_exp[:pos_bracket_izq] + union_exp + reg_exp[pos_bracket_der + 1 :]

        pos_bracket_izq = reg_exp.find("[")
        pos_bracket_der = reg_exp.find("]")

    if pos_bracket_der != -1:
        raise Exception("expresión regular invalida.")

    return reg_exp


def add_concat_symbol(reg_exp):
    """
    Adds the concatenation symbol . to the expression
    """
    new_reg_exp = ""
    for current_char in reg_exp:
        if len(new_reg_exp) > 0:
            prev_char = new_reg_exp[len(new_reg_exp) - 1]
            if (prev_char == ")" or is_alphabet(prev_char) or prev_char == "*") and (
                current_char == "(" or is_alphabet(current_char)
            ):
                new_reg_exp += "."
        new_reg_exp += current_char
    return new_reg_exp


def regex_to_postfix(reg_exp):
    postfix_exp = ""
    operator_stack = []

    reg_exp = add_concat_symbol(reg_exp)

    # shunting yard algorithm
    for current_char in reg_exp:
        if is_alphabet(current_char):
            postfix_exp += current_char
        elif current_char == "(":
            operator_stack.append(current_char)
        elif current_char == ")":
            top = operator_stack.pop()
            while top != "(":
                postfix_exp += top
                top = operator_stack.pop()
        else:
            if len(operator_stack) == 0:
                operator_stack.append(current_char)
            else:
                top = operator_stack[len(operator_stack) - 1]
                while top != "(" and priority[top] >= priority[current_char]:
                    postfix_exp += top
                    operator_stack.pop()
                    if len(operator_stack) > 0:
                        top = operator_stack[len(operator_stack) - 1]
                    else:
                        break
                operator_stack.append(current_char)
    while len(operator_stack) != 0:
        postfix_exp += operator_stack.pop()

    return postfix_exp

def regex_to_dfa():
    pass


if __name__ == "__main__":
    pass
    # reg_exp = "a(a|b)*b"
    # reg_exp = "[0-9][0-9]*"
    # print(reg_exp)
    # postfix_exp = regex_to_postfix(reg_exp)

    # parse_clases_chars(reg_exp)
