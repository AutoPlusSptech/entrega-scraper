class Node:
    def __init__(self, value, node_type):
        self.value = value
        self.node_type = node_type
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def print_grafo(self, level=0):
        print("  " * level + str(self.value))
        for child in self.children:
            child.print_grafo(level + 1)

def construir_grafo(tokens):
    root = Node("Expressão", "root")
    for token in tokens:
        item, tipo = token
        node = Node(item, tipo)
        root.add_child(node)
    return root
# Constantes
TESTE   = False

# caracteres usados em operadores
OPERADORES = "%*/+-!^="

# caracteres usados em números inteiros
DIGITOS = "0123456789"

# ponto decimal
PONTO = "."

# todos os caracteres usados em um números float
FLOATS = DIGITOS + PONTO

# caracteres usados em nomes de variáveis
LETRAS  = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

# abre e fecha parenteses
ABRE_FECHA_PARENTESES = "()"

# categorias
OPERADOR   = 1 # para operadores aritméticos e atribuição
NUMERO     = 2 # para números: todos são considerados float
VARIAVEL   = 3 # para variáveis
PARENTESES = 4 # para '(' e ')

# Whitespace characters: space, newline, horizontal tab,
# vertical tab, form feed, carriage return
BRANCOS    = [' ', '\n', '\t', '\v', '\f', '\r']

# caractere que indica comentário
COMENTARIO = "#"


#------------------------------------------------------------
def tokeniza(exp):
    """(str) -> list

    Recebe uma string exp representando uma expressão e cria 
    e retorna uma lista com os itens léxicos que formam a
    expressão.

    Cada item léxico (= token) é da forma
       
        [item, tipo]

    O componente item de um token é 

        - um float: no caso do item ser um número; ou 
        - um string no caso do item ser um operador ou 
             uma variável ou um abre/fecha parenteses.

    O componente tipo de um token indica a sua categoria
    (ver definição de constantes acima). 

        - OPERADOR;
        - NUMERO; 
        - VARIAVEL; ou 
        - PARENTESES

    A funçao ignora tuo que esta na exp apos o caractere
    COMENTARIO (= "#").
    """
    # escreva o seu código abaixo
    
    
    
    tokens = []
    i = 0
    while i < len(exp):
        if exp[i] in BRANCOS:
            i += 1
        elif exp[i] in OPERADORES:
            tokens.append([exp[i], OPERADOR])
            i += 1
        elif exp[i] in DIGITOS:
            j = i
            while j < len(exp) and exp[j] in FLOATS:
                j += 1
            tokens.append([float(exp[i:j]), NUMERO])
            i = j
        elif exp[i] in LETRAS:
            j = i
            while j < len(exp) and exp[j] in LETRAS + DIGITOS:
                j += 1
            tokens.append([exp[i:j], VARIAVEL])
            i = j
        elif exp[i] in ABRE_FECHA_PARENTESES:
            tokens.append([exp[i], PARENTESES])
            i += 1
        else:
            i += 1
            
            
            
    grafo = construir_grafo(tokens)
    
    

    grafo.print_grafo()
    
    
    return tokens


print(tokeniza("a = 2 + 3 * 4 # isto e um comentario"))