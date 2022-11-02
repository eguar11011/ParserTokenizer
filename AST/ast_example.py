import ast
from pprint import pprint
from string import ascii_letters
import math

def main():

    #transforma el archivo en un AST
    with open("ast_example.py", "r") as source:
        tree = ast.parse(source.read()) 

    analyzer = Analyzer() #extraer información del árbol
    analyzer.visit(tree) 
    analyzer.report()


class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.stats = {"import": [], "from": []}

    def visit_Import(self, node):
        for alias in node.names:
            self.stats["import"].append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.stats["from"].append(alias.name)
        self.generic_visit(node)

    def report(self):
        pprint(self.stats)


if __name__ == "__main__":
    main()