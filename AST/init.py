import ast

def T_AST():
    """
    Transforma el archivo en un AST
    """
    with open("caracteres_repetidos", "r") as source:
        tree = ast.parse(source.read()) 
