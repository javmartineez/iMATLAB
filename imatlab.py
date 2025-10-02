"""
imatlab.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP09B
Integrantes:
    - Javier Mochales López
    - Javier Martínez Berenguer 

Descripción:
Sistema interactivo IMAT-LAB de resolución de ecuaciones en aritmética modular.

Interfaz de acceso interactivo o por lotes a la librería modular.py. Si este script se ejecuta sin par´ametros,
lanzar´a la interfaz de usuario para el modo interactivo.
"""

import re
import sys
import argparse
import modular as mod
from typing import TextIO

CMD_RE = re.compile(r'\s*([A-Za-z_]\w*)\s*\(\s*(.*?)\s*\)\s*$') #expresion regular para identificar el comando 
INT_RE = re.compile(r'[+-]?\d+') #expresion regular para identificar los numeros
LIST_RE = re.compile(r'\[[^\]]+\]')

# Diccionario con el minimo y maximo de argumentos que puede admitir cada funcion
N_ARGS = {
    "primo": (1, 1),
    "primos": (2, 2),
    "factorizar": (1, 1),
    "mcd": (1, float('inf')),  
    "coprimos": (2, 2),
    "pow": (3, 3),
    "inv": (2, 2),
    "euler": (1, 1),
    "legendre": (2, 2),
    "raiz": (2,2),
    "resolverSistema": (1, float('inf'))
}

def check_function(function: str, argumentos: list):
    if function not in FUNCTIONS:
        raise mod.ArgumentError()

    # valida nº de argumentos (antes de llamar)
    min_a, max_a = N_ARGS.get(function, (0, None))
    n = len(argumentos)
    if n < min_a or n > max_a:
        raise mod.ArgumentError

    fn = FUNCTIONS[function]
    return fn(*argumentos)  
 
def check_argument(args: list):
    """
    Comprueba que todos los argumentos sean enteros y no vacíos.
    """
    for a in args:
        if type(a) is not int:
            raise mod.ArgumentError

def extraer_comando(linea:str) -> tuple[str, list[int]]: 
    """
    Extrae el nombre del comando y sus argumentos enteros desde una línea tipo:
        'mcd(6, 9)'  -> ('mcd', [6, 9])
        'primo(7)'   -> ('primo', [7])
        'factorizar(-10)' -> ('factorizar', [-10])

    Si la línea NO cumple el patrón comando(args), lanza NOP().
    Nota: la línea vacía debe tratarse FUERA (p. ej. en run_commands).
    """
    s = linea.strip()
    m = CMD_RE.fullmatch(s)

    if not m:
        # Formato incorrecto: comando desconocido, paréntesis mal, basura al final, etc.
        raise mod.ArgumentError

    nombre = m.group(1)
    argstr = m.group(2)
    VALID_ARG = re.compile(r"^[+-]?\d+(?:\s*,\s*[+-]?\d+)*\s*$") #Condición para no incluir letras y puntos en los args
    if not bool(VALID_ARG.fullmatch(argstr)):
        VALID_SIST = re.compile(r"^\[[+-]?\d+;[+-]?\d+;[+-]?\d+\](?:,\[[+-]?\d+;[+-]?\d+;[+-]?\d+\])*$")
        if nombre == "resolverSistema" and bool(VALID_SIST.fullmatch(argstr)):
            pattern = re.compile(r"\[([^\]]+)\]")
            args = [list(map(int, group.split(';'))) for group in pattern.findall(argstr)]
            return nombre, args
        else:
            raise mod.ArgumentError
    else:
        # Extrae todos los enteros de una pasada (tolerante a espacios y signos + / -)
        args = [int(x) for x in INT_RE.findall(argstr)]
        return nombre, args
    
def interactive_loop():
    while True:
        linea = input(">>> ").strip()
        if linea == "":
            break
        try:
            comando, args = extraer_comando(linea)
            res = check_function(comando, args)
            print(res)
        except (ZeroDivisionError, mod.IncompatibleEquationError) as e:
            print(f"NE: {e}")
        except mod.ArgumentError:
            print("NOP: comando o argumentos inválidos")
        except Exception as e:
            print(f"NOP: {e}")

def run_commands(fin: TextIO = None, fout: TextIO = None) -> None:
    """
    Lee comandos desde fin (una expresión por línea), los evalúa con check_function
    y escribe el resultado en fout.
    Termina al encontrar una línea vacía.
    """

    if fin is None:
        fin = sys.stdin
    if fout is None:
        fout = sys.stdout

    for linea in fin:
        s = linea.strip()
        if s == "":
            break
        try:
            comando, args = extraer_comando(s)
            res = check_function(comando, args)
            fout.write(str(res) + "\n")
        except (ZeroDivisionError, mod.IncompatibleEquationError):
            fout.write("NE\n")
        except mod.ArgumentError:
            fout.write("NOP\n")
        except Exception:
            fout.write("NOP\n")  # error inesperado → también NOP

def primo(a: int) -> str: 
    return "Sí" if mod.es_primo(a) else "No"

def primos(a: int, b: int):
    lista = mod.lista_primos(a, b)
    return "NE" if not lista else ", ".join(str(p) for p in lista)

def factorizar(n: int) -> str: #Hay que cambiarla
    """Devuelve la factorización de n en formato 'p1:e1, p2:e2,...'."""
    if n in {-1, 0, 1}:
        return n
    factores = mod.factorizar(n)  # dict {p:e}
    # Ordena por primo para que el string sea determinista
    pares = [f"{p}: {e}" for p, e in sorted(factores.items())]
    return ", ".join(pares)   

def mcd(*nums: int) -> int:

    if len(nums) == 0:
        raise mod.ArgumentError()

    elif len(nums) == 1: 
        return abs(nums[0])

    elif len(nums) == 2:
        a, b = nums
        return mod.mcd(a, b)
    else:
        return mod.mcd_n(list(nums))  # delega en la versión que acepta lista

def coprimos(a: int, b: int) -> str:
    return "Sí" if mod.coprimos(a, b) else "No"

def pow(base: int, exp: int, p: int) -> int:
    return mod.potencia_mod_p(base, exp, p)

def inv(n: int, p: int) -> int:
    return mod.inversa_mod_p(n, p)

def euler(n: int) -> int:
    return mod.euler(n)

def legendre(n: int, p: int):
    return mod.legendre(n, p)

def raiz(n: int, p: int) -> int:
    return mod.raiz_mod_p(n, p)

def resolverSistema(*listas:list[int]) -> tuple[int,int]:
    
    #return mod.resolver_sistema_congruencias(alist, blist, clist)
    alist = []
    blist = []
    clist = []
    for a, b, c in listas:
        alist.append(a)
        blist.append(b)
        clist.append(c)
    r,m = mod.resolver_sistema_congruencias(alist, blist, clist)
    return f"{r} (mod {m})"

FUNCTIONS = {
            "primo": primo,
            "primos": primos,
            "factorizar": factorizar,
            "mcd": mcd,
            "coprimos": coprimos,
            "pow": pow,
            "inv": inv,
            "euler": euler,
            "legendre": legendre,
            "resolverSistema": resolverSistema,
            "raiz": raiz
            }  

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input",  type=argparse.FileType("r", encoding="utf-8"), default=None)
    parser.add_argument("-o", "--output", type=argparse.FileType("w", encoding="utf-8"), default=None)
    args = parser.parse_args()

    # por ahora, solo mostramos qué llegó
    entrada  = args.input  or sys.stdin
    salida = args.output or sys.stdout

    # decidimos modo de la forma más simple posible:
    # interactivo SOLO si no nos han pasado -i/-o y además stdin y stdout son TTY
    interactive = (args.input is None and args.output is None
                   and sys.stdin.isatty() and sys.stdout.isatty())

    if interactive:
        print("Entrando en modo interactivo... (Presiona ENTER sin argumentos para salir) \n")
        interactive_loop()
    else:
        run_commands(fin=entrada, fout=salida)



if __name__ == "__main__":
    main()