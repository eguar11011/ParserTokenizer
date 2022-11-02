from init import T_AST
import ast

def main():

    #transforma el archivo en un AST
    with open("caracteres_repetidos.py", "r") as source:
        tree = ast.parse(source.read()) 


def contar_caracteres_repetidos ( palabra : str ) -> int :
    pal = palabra . lower ()
    rep = 0
    ultimo = len ( pal )
    v = []
    for a in range ( ultimo ) :
        for b in range ( ultimo ) :
            if a != b :
                if ( pal [ a ] == pal [ b ]) and ( pal [ a ] not in v ) :
                    rep += 1
                    v.append ( pal [ a ])
    return rep

if __name__ == "__main__":
    main()